# from collections import defaultdict
import logging
import pickle
# import const

# from DataHandler.dataHandler import DataHandler as DH
from KernelProcessor.kernelProcessor import KernelProcessor as KP
from DataHandler.dataHandler import DataHandler as DH
from Evaluator.evaluator import standardize, evaluate


class MainProcessor:

    def __init__(self, pb, date_str=None,
                 past_days=15, evaluation_time_delta=15):

        # create logger
        logger = logging.getLogger('MainProcessor')
        logger.setLevel(logging.DEBUG)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter
        formatter = logging.Formatter('[%(asctime)s]:[%(levelname)s]:%(name)s'
                                      + ' ::: \'%(message)s\'')
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        logger.addHandler(ch)
        # 'application' code
        logger.debug(f'__init__(pb:{pb}, date_str:"{date_str}", past_days:'
                     f'{past_days}, evaluation_time_delta:'
                     f'{evaluation_time_delta})')

        self.logger = logger
        self.pb = pb
        self.dh = DH(pb)
        self.kp = KP(rtl=self.dh.rtd.values())
        self.last_date_seen = date_str
        self.past_days = past_days
        self.evaluation_time_delta = evaluation_time_delta
        self.evaluation_time_slot = evaluation_time_delta
        self.load_translator()

        if date_str:
            self.dh.load_past_data(date_str, past_days)
        else:
            print('Date not provided, will be deducted while processing')
            logger.debug(f'__init__(pb:{pb}, date_str:"{date_str}" --> Date'
                         ' not provided, will be deducted while processing')

    # Function to be called whenever a new log comes

    def log_digest(self, log):
        self.logger.debug(f'Digesting new log: "{log}"')
        # get USER_ID, datetime, and TOWER_ID from the log
        log_uid, log_datetime, log_tid = log.split(';')
        # get date and time from datetime string
        log_date, log_time = log_datetime.split(' ')
        # removes the delimiter of the date string
        log_date = log_date.replace('-', '')
        # splits date and time and cast them into integers
        h, m = log_time.split(':')[:2]
        h, m = int(h), int(m)
        # get the slot from h and m, a day contains 1440slots (1 each minute)
        log_slot = h*60 + m

        self.logger.debug(f'LOG DATE: "{log_date}" | '
                          f'LAST DATE SEEN: "{self.last_date_seen}" | '
                          f'LOG SLOT: "{log_slot}" | '
                          'EVALUATION SLOT TIME: '
                          f'"{self.evaluation_time_slot}"')

        # If the log has missing information then we just discard it
        if log_uid == 'NULL' or log_tid == '':
            return

        # In case the date was not provided by the constructor we infer the
        # date from the first log and we load the relative historical data
        if self.last_date_seen is None:
            self.logger.debug('self.last_date_seen is None,' +
                              'getting it from log')
            self.last_date_seen = log_date
            self.dh.load_past_data(log_date, self.past_days)

        # In case the time goes backwards we raise an error.
        if log_date < self.last_date_seen:
            raise ValueError('[ERROR] Unordered Logs')

        # Case when is time to evaluate the processed data
        #           >= ? >
        if log_slot >= self.evaluation_time_slot:
            self.logger.debug('SLOT CHANGE: log_slot >= '
                              'self.evaluation_time_slot')
            # relevant towers seen in the logs
            rtl_seen = self.kp._rtl_count.keys()
            # prepares the payload for the evaluation
            payload = [None] * len(rtl_seen)
            # for each relevant tower location seen in the logs
            for idx, rtl in enumerate(rtl_seen):
                # compute the mean
                mean = self.dh.get_tower_mean(rtl, self.evaluation_time_slot-1)
                # compute the standard deviation
                stdv = self.dh.get_tower_std(rtl, self.evaluation_time_slot-1)
                # evaluates the standardized value
                val = evaluate(
                              standardize(self.kp.get_status(rtl), mean, stdv),
                              10)

                print(rtl, self.kp.get_status(rtl))

                payload[idx] = {'id': self.translator[rtl],
                                'value': val, 'anomaly': False}

            # update evaluation time slot
            self.evaluation_time_slot += self.evaluation_time_delta

            self.logger.debug('PAYLOAD COMPUTED')
            self.logger.debug(f'PAYLOAD:{payload}')
            input()

            # TODO: insert data in asynchronous queue for async consumer
            # await websocket.send(json.dumps(payload))

        if self.last_date_seen < log_date:
            self.logger.debug('DAY HAS CHANGED:')
            # self.dh.persist_historical_data(self.kp.get_raw_snapshot())
            self.dh.update_past_data(log_date)
            self.kp.reset()
            self.last_date_seen = log_date
            self.evaluation_time_slot = self.evaluation_time_delta

        # TODO plug evaluator and websocket

        self.kp.log_digest(self.dh.rtd.get(log_tid), h, m, log_uid)

    def load_translator(self):
        with open(self.pb.get_translator_path(), 'rb') as file_handler:
            self.translator = pickle.load(file_handler)
