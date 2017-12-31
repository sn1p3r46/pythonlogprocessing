from collections import deque
import warnings

import numpy as np

class HistoricalDataQueue(deque):

    def __init__(self, iterable=(), maxlen=None):
        super().__init__(iterable, maxlen)
        self.__update()

    def __update(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            self.mean = np.nanmean(self)
            self.std = np.nanstd(self)
            self.sum = np.nansum(self)

    def __short_update(self, new=np.nan, old=np.nan):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            self.sum = np.nansum((self.sum, - old, new))
            self.mean = self.sum / len(self)
            self.std = np.nanstd(self)

    def __repr__(self):
        return "HistoricalData(" + super().__repr__() + ", mean=" + \
                                str(self.mean) + ", std=" + str(self.std) + ")"

    def __str__(self):
        return self.__repr__()

    def append(self,x):
        old = np.nan
        if len(self) == self.maxlen:
            old = self[0]

        super().append(x)
        self.__short_update(x, old)

    def appendleft(self, x):
        old = np.nan
        if len(self) == self.maxlen:
            old = self[-1]

        super().appendleft(x)
        self.__short_update(x, old)

    def pop(self):
        res = super().pop()
        self.__short_update(old=res)
        return res

    def popleft(self):
        res = super().popleft()
        self.__short_update(old=res)
        return res

    def clear(self):
        res = super().clear()
        self.mean, self.std, self.sum = 0,0,0

    def extend(self, iterable):
        res = super().extend(iterable)
        self.__update()
        return res

    def extendleft(self, iterable):
        res = super().extendleft(iterable)
        self.__update()
        return res

    def index(self, x, start=None, stop=None):
        res = super().index(x, start, stop)
        self.__update()
        return res

    def insert(self, i, x):
        res = super().insert(i, x)
        self.__update()
        return res

    def remove(self, value):
        res = super().remove(value)
        self.__update()
        return res
