#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
@Time : 2020/10/14 13:25
@Author : Nieeka
@Version：V 1.0
@File : DataCash.py
@Desciption :
"""
from collections import deque
from re import X
import matplotlib.pyplot as plt
import math
from scipy import signal
import sys
sys.path.append('..')
sys.path.append('.')
import threading
import uuid
import numpy as np

from CommonSystem.Exceptions.CommunicationModuleExceptions import TopicNotAvailableException
from CommonSystem.MessageReceiver.EEGPlatformCommunicationModule.implement.CommunicationConsumer import CommunicationConsumer

MaxValue = 40480
confPath = 'CommonSystem/MessageReceiver/EEGPlatformCommunicationModule/usage/config/consumer-config.json'

class DataCash(threading.Thread):
    def __init__(self, threadName='NeuroScan', topic='NeuroScanEEG'):
        threading.Thread.__init__(self)
        self.name = threadName
        self.topic = topic  # 实例所面对的topic
        self.messageQueue = deque(maxlen=MaxValue)  # 缓冲的数据队列
        self.lock = threading.RLock()
        self.stop_flag = False
        # event start point
        self.eventPoint = deque(maxlen=600)
        self.eventExist = None
        self.consumer = CommunicationConsumer(confPath, str(uuid.uuid1()), self.topic)

        self.filters = self._initFilter()

        self.send = []

    def connect(self):
        self.start()

    def run(self):
        try:
            # 循环接收消息
            while True:

                consumeMsg = self.consumer.receive()

                if type(consumeMsg) == bytes:
                    # neuroscan
                    # 每次收到的数据包长度 0.1s
                    data = np.frombuffer(consumeMsg, dtype=np.single)

                    chn = 10
                    data = data.reshape(chn, -1)

                    self.lock.acquire()
                    # messageQueue 存放了每个接收到的数据包
                    self.messageQueue.append(data)

                    self._findEvent(data)

                    self.lock.release()
                else:
                    pass
                if self.stop_flag:
                    break
        except TopicNotAvailableException as e:
            print(e)

    def _findEvent(self,data):
        
        events = data[-1,:].flatten()

        if np.any(events != 0) and max(events)<50:
            # event 从哪个数据包开始
            packageInx  =  self.getMessageQueueSize()-1
            # 在该数据包的哪个位置
            point = int(np.argwhere(events))

            self.eventPoint.appendleft([point,packageInx])
            self.packetSize = data.shape[-1]
            self.eventExist =True
            print('Recieved Event,ready to start processing')
            return self

    def readData(self, startPoint, endPoint):
        if 0 <= startPoint < endPoint <= self.getMessageQueueSize():
            # 如果消息队列中有足够的数据，就读取数据
            tmp = []
            self.lock.acquire()
            for i in range(startPoint, endPoint):
                tmp.append(self.messageQueue[i])
            self.lock.release()

            return tmp

        else:
            # 否则等待数据继续添加
            return None


    def readNewData(self, pointCount):
        return self.readData(self.getMessageQueueSize() - pointCount, self.getMessageQueueSize())

    def readRecentData(self,startPoint,length):

        # 降采样之前
        # realLen = int(4*length)
        srate = 1000
        startPoint, realLen = int(startPoint*srate), int(length*srate)
        realLen = startPoint+realLen
        startPoint = 0

        point, packageInx = 0,len(self.messageQueue)
        self.packetSize = self.messageQueue[-1].shape[-1]
        # 要读多少个数据包
        pacNUM = math.ceil((realLen+startPoint)/self.packetSize)

        data = None
        while data is None:
            data = self.readData(packageInx, packageInx+pacNUM+1)

        data = np.hstack(data)
        data = data[:, (startPoint+point):(startPoint+point+realLen)]

        data = data[:-1, :]

        # 降采样
        data = self._resample(data)

        # 滤波
        data = self.filterNotch(data)

        # 归一化
        data = self._normalization(data)

        return data

    def readFixedData(self,startPoint,length):
        
        # 降采样之前
        # realLen = int(4*length)
        srate = 1000
        startPoint, realLen = int(startPoint*srate), int(length*srate)
        realLen = startPoint+realLen
        startPoint = 0

        while self.eventExist is True:
        
            events = self.eventPoint.pop()
            point,packageInx = events
            
            # 要读多少个数据包
            pacNUM = math.ceil((realLen+startPoint)/self.packetSize)

            data = None
            while data is None:
                data = self.readData(packageInx,packageInx+pacNUM+1)
            
            data = np.hstack(data)
            data = data[:, (startPoint+point):(startPoint+point+realLen)]
            self.eventExist = False

            data = data[:-1, :]

            plt.figure()
            # 降采样
            data = self._resample(data)
            
            # 滤波
            data = self.filterNotch(data)

            # 归一化
            data = self._normalization(data)

            return data
        else:
            return None


    def getMessageQueueSize(self):
        self.lock.acquire()
        queue_len = len(self.messageQueue)
        self.lock.release()
        return queue_len

    def _resample(self,x):
        
        x = x[:, ::4]  # 降采样至1/4
        
        return x

    def _normalization(self, xs, scale=[-1, 1]):
        
        normed = np.zeros(xs.shape)

        for chINX, chn in enumerate(xs):
            # 去除基线
            chn = chn - chn.mean()

            normed[chINX] = chn

        return self.minMax(normed)

    def minMax(self, x, scale=[0, 1]):

        # x:n_chn * times
        n_chn = x.shape[0]
        nmin, nmax = scale

        x = np.hstack(x)
        x = (x-min(x))/(max(x)-min(x))*(nmax-nmin)+nmin
        x = np.reshape(x, (n_chn, -1))

        return x

    def filterNotch(self,s):
        
        notchFilter, bpFilter = self.filters
        
        b_notch, a_notch = notchFilter
        b_bp, a_bp = bpFilter

        sNotched = np.zeros_like(s)

        for i,c in enumerate(s):

            # notch filter
            x = signal.filtfilt(b_notch, a_notch, c)
            # band pass filter [0.5,200]
            x = signal.filtfilt(b_bp, a_bp,x)

            sNotched[i] = x

        return sNotched

    def _initFilter(self):
        
        # notch 
        fs = 250.0  # Sample frequency (Hz)
        f0 = 50.0  # Frequency to be removed from signal (Hz)
        Q = 10.0  # Quality factor

        b, a = signal.iirnotch(f0, Q, fs)
        notch = [b, a]

        # band pass
        b, a = signal.butter(N=3, Wn=100, fs=fs, btype='lowpass')
        bp = [b, a]

        return notch, bp





