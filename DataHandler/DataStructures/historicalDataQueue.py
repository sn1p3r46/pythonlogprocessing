from collections import deque

import numpy as np


class HistoricalDataQueue(deque):

    def __init__(self, iterable=(), maxlen=None):
        if maxlen is None:
            raise ValueError()

        super().__init__(iterable, maxlen)

        self.sum, self.sqr_sum, self.NaNCounter = self.__counter_helper()

        if self.NaNCounter == len(self):
            self.mean = np.nan
            self.std = np.nan
            self.sum = np.nan
            self.sqr_sum = np.nan

        else:
            nonNaN = (len(self) - self.NaNCounter)
            self.mean = self.sum / nonNaN
            std_sum = nonNaN*(self.mean**2)-2*self.mean*self.sum + self.sqr_sum
            self.std = (std_sum / nonNaN)**(1/2)

    def __counter_helper(self):

        NaNCounter = 0
        my_sum = 0
        sqr_sum = 0

        for i in self:
            if np.isnan(i):
                NaNCounter += 1
            else:
                my_sum += i
                sqr_sum += i**2

        return my_sum, sqr_sum, NaNCounter

    def _update(self, new=np.nan, old=None):
        if np.isnan(self.mean):
            self.sum = new
            self.sqr_sum = new**2
            self.std = 0.0*new
            self.mean = new
            self.NaNCounter +=\
                + 1*np.isnan(new)\
                - 1*(old is not None and np.isnan(old))

        else:
            self.NaNCounter += \
                1*np.isnan(new) \
                - 1*(old is not None and np.isnan(old))

            nonNaN = (len(self) - self.NaNCounter)
            new = new if not np.isnan(new) else 0
            old = old if old is not None and not np.isnan(old) else 0
            self.sum += new - old
            self.sqr_sum += new**2 - old**2
            self.mean = self.sum/nonNaN
            std_sum = nonNaN*(self.mean**2)-2*self.mean*self.sum + self.sqr_sum
            self.std = (std_sum / nonNaN)**(1/2)

    def __repr__(self):
        return "HistoricalData(" + super().__repr__() + ", mean=" + \
                                str(self.mean) + ", std=" + str(self.std) + ")"

    def __str__(self):
        return "HistoricalData(" + super().__repr__() + ", mean=" + \
                                str(self.mean) + ", std=" + str(self.std) + ")"

    def append(self, x):
        old = self[0] if len(self) == self.maxlen else None
        super().append(x)
        self._update(x, old)

    def appendleft(self, x):
        old = self[-1] if len(self) == self.maxlen else None
        super().appendleft(x)
        self._update(x, old)

    def pop(self):
        res = super().pop()
        self.__short_update(old=res)
        return res

    def popleft(self):
        res = super().popleft()
        self.__short_update(old=res)
        return res

    def clear(self):
        # res = super().clear()
        super().clear()
        self.mean = np.nan
        self.std = np.nan
        self.sum = np.nan
        self.sqr_sum = np.nan
        self.NaNCounter = 0

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

    def remove(self, value):
        res = super().remove(value)
        self.__update()
        return res
