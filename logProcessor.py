from collections import defaultdict
from dateutil.parser import parse
from datetime import timedelta

import kernelProcessor as kp
import numpy as np
import warnings
import pickle
import const


class LogProcessor:

    def load_rtd(self):
        print('>[load_relevant_towers(path)]\nLOADING RELEVANT TOWERS\n---')
        with open(self.pb.get_relevant_towers_path(), 'r') as tower_f:
            self.rtd = {l.strip().split(';')[0]:
                        ';'.join(l.strip().split(';')[-2:])
                        for l in tower_f.readlines()}

    def create_data_structure(self, past_data_list, n_days):
        print('>[create_data_structure(past_data_list, number_of_slices,' +
              ' number_of_days)]\nCREATING DATA STRUCTURE\n---')
        tower_past_data_structs = {}
        for tower_id in set(self.rtd.values()):
            matrix = np.zeros(shape=(1440, n_days + 3),
                              dtype=np.float)

            for idx, past_data in enumerate(past_data_list):
                my_list = np.full((1440), np.nan)

                if tower_id in past_data:
                    my_list = np.asarray(past_data[tower_id], np.float)

                matrix[:, idx] = my_list

            # eventually parallelize for loop
            # I expect to see RuntimeWarnings in this block
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                for idx, val in enumerate(matrix):
                    matrix[idx, -3] = np.nanmean(val[:-3])
                    matrix[idx, -2] = np.nanstd(val[:-3])

            tower_past_data_structs[tower_id] = matrix

        print('>[create_data_structure(past_data_list, number_of_slices,' +
              ' number_of_days)]\nDATA STRUCTURE CREATED\n---')
        return tower_past_data_structs

    def load_past_data(self, date_str, n_days):
        files_to_load = []
        my_date = parse(date_str)
        my_delta = timedelta(days=1)
        for i in range(n_days):
            my_date = my_date - my_delta
            files_to_load.append(
                self.pb.build_past_data_file_name(my_date.strftime('%Y%m%d')))

        past_data = []
        for filename in files_to_load:
            try:
                with open(self.pb.build_historical_path(filename), 'rb')\
                            as my_file:
                    past_data.append(pickle.load(my_file))
            except FileNotFoundError:
                print("File not found:" + self.pb.
                      build_historical_path(filename))

        print("Historical data loaded!")
        return self.create_data_structure(past_data, n_days)

    def log_digest(self, log):
        log_tid, log_datetime, log_uid = log.split(';')
        log_date, log_time = log_datetime.split(' ')
        h, m = log_time.split(':')[:2]

        if not self.last_date_seen:
            self.last_date_seen = log_date
            # TODO load past data in memory

        elif self.last_date_seen < log_date:
            # TODO: store function
            print(' === Store Function === ')
            print("last_date_seen: {}".format(self.last_date_seen))
            print("log_date: {}".format(log_date))
            print(self.KP.get_raw_snapshot())
            self.last_date_seen = log_date

        self.KP.log_digest(self.rtd.get(log_tid), int(h), int(m), log_uid)

    def load_translator(self):
        with open(self.pb.get_translator_path(), 'rb') as fobj:
            self.translator = pickle.load(fobj)

    def init_kernelProcessor(self):
        self.KP = kp.KernelProcessor(self.rtd.values())

    def __init__(self, pb, date=None, past_days=15):
        self.pb = pb
        self.load_rtd()
        self.init_kernelProcessor()
        self.last_date_seen = date
        self.load_translator()

        if date:
            self.tower_past_data = self.load_past_data(date, past_days)
        else:
            self.tower_past_data = None
            print('Date not provided, will be deducted while processing')
