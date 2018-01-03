# from collections import defaultdict
from dateutil.parser import parse
from datetime import timedelta

import numpy as np
import warnings
import pickle
# import const

from dataHandler import DataHandler as DH
from kernelProcessor import kernelProcessor as KP


class MainProcessor:

    def __init__(self, pb, date_str=None, past_days=15):
        self.pb = pb
        self.dh = DH(pb)
        self.kp = KP(rtl=dh.rtd.values())
        self.last_date_seen = date_str
        self.past_days = past_days

        if date:
            self.dh.load_past_data(date, past_days)
        else:
            print('Date not provided, will be deducted while processing')


    def log_digest(self, log):
        log_uid, log_datetime, log_tid = log.split(';')
        log_date, log_time = log_datetime.split(' ')
        h, m = log_time.split(':')[:2]
        log_date.replace('-','')

        if log_uid == 'NULL' or log_tid == '':
            return

        if self.last_date_seen is None:
            self.last_date_seen = log_date
            self.dh.load_past_data(log_date, self.past_days)

        if log_date < self.last_date_seen:
            raise ValueError('Unordered Logs')

        elif self.last_date_seen < log_date:
            self.dh.persist_historical_data(self.KP.get_raw_snapshot())
            self.kp.reset()



        self.KP.log_digest(self.dh.rtd.get(log_tid), int(h), int(m), log_uid)

    def load_translator(self):
        with open(self.pb.get_translator_path(), 'rb') as fobj:
            self.translator = pickle.load(fobj)
