# from collections import defaultdict
from dateutil.parser import parse
from datetime import timedelta

import numpy as np
import warnings
import logging
import pickle
# import const

from dataHandler import DataHandler as DH
from kernelProcessor import KernelProcessor as KP
from evaluator import standardize, evaluate

class MainProcessor:

    def __init__(self, pb, date_str=None, past_days=15, time_delta=5):

        # create logger
        logger = logging.getLogger('MainProcesr')
        logger.setLevel(logging.DEBUG)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter
        formatter = logging.Formatter('[%(asctime)s]:[%(levelname)s]:%(name)s ::: \'%(message)s\'')
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        logger.addHandler(ch)
        # 'application' code
        logger.debug(f'__init__(pb:{pb}, date_str:"{date_str}", past_days:{past_days}, time_delta:{time_delta})')

        self.logger = logger
        self.pb = pb
        self.dh = DH(pb)
        self.kp = KP(rtl=self.dh.rtd.values())
        self.last_date_seen = date_str
        self.past_days = past_days
        self.time_delta = time_delta
        self.slot_time = time_delta

        if date_str:
            self.dh.load_past_data(date_str, past_days)
        else:
            print('Date not provided, will be deducted while processing')
            logger.debug(f'__init__(pb:{pb}, date_str:"{date_str}" --> Date not provided, will be deducted while processing')


    def log_digest(self, log):
        self.logger.debug(f'Digesting new log: "{log}"')

        log_uid, log_datetime, log_tid = log.split(';')
        log_date, log_time = log_datetime.split(' ')
        log_date = log_date.replace('-','')
        h, m = log_time.split(':')[:2]
        h, m = int(h), int(m)

        log_slot = h*60 + m

        self.logger.debug(f'LOG DATE: "{log_date}" | LAST DATE SEEN: "{self.last_date_seen}" | LOG SLOT: "{log_slot}" | SLOT TIME: "{self.slot_time}"')

        if log_uid == 'NULL' or log_tid == '':
            return

        if self.last_date_seen is None:
            self.logger.debug('self.last_date_seen is None, getting it from log')
            self.last_date_seen = log_date
            self.dh.load_past_data(log_date, self.past_days)

        if log_date < self.last_date_seen:
            raise ValueError('Unordered Logs')

        if log_slot >= self.slot_time:
            self.logger.debug('SLOT CHANGE: log_slot >= self.slot_time')
            rtl_seen = self.kp._rtl_count.keys()
            payload = [None] * len(rtl_seen)
            for idx, rtl in enumerate(rtl_seen):
                mean = dh.tower_past_data[rtl][self.slot_time - 1].mean
                stdv = dh.tower_past_data[rtl][self.slot_time - 1].std
                val = evaluate(standardize(kp.get_status(rtl), mean, stdv), 10)

                playload[idx] = {'id': self.translator[tower_id],
                                 'value': val, 'anomaly': False}

            self.logger.debug('PAYLOAD COMPUTED')
            self.logger.debug(f'PAYLOAD:{payload}')

            # TODO:insert data in asynchronous queue for async consumer
            # await websocket.send(json.dumps(payload))

        if self.last_date_seen < log_date:
            self.logger.debug('DAY HAS CHANGED:')
            self.dh.persist_historical_data(self.kp.get_raw_snapshot())
            self.dh.update_past_data(log_date)
            self.kp.reset()
            self.last_date_seen = log_date
            self.slot_time = self.time_delta

        # TODO plug evaluator and websocket


        self.kp.log_digest(self.dh.rtd.get(log_tid), h, m, log_uid)

    def load_translator(self):
        with open(self.pb.get_translator_path(), 'rb') as fobj:
            self.translator = pickle.load(fobj)
