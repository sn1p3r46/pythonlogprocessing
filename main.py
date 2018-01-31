#!/usr/bin/python3.6

from PathBuilder.pathBuilder import PathBuilder as PB
from MainProcessor.mainProcessor import MainProcessor as MP

import time

mp = MP(PB, '20161001')

mp.log_digest('58242954;2016-10-01 00:00:10;001600AA')

time.sleep(10)

mp.log_digest('58242954;2016-10-01 00:05:10;001600AA')

time.sleep(10)

mp.log_digest('58242954;2016-10-02 00:00:10;001600AA')

time.sleep(10)

mp.log_digest('58242954;2016-10-03 00:00:10;001600AA')
