from historicalDataQueue import HistoricalDataQueue as HDQ
from dateutil.parser import parse
from datetime import timedelta

import numpy as np
# import warnings
import logging
import pickle


class DataHandler:

    def __init__(self, pb):

        # create logger
        logger = logging.getLogger('DataHandler')
        logger.setLevel(logging.DEBUG)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter
        formatter = logging.Formatter('[%(asctime)s]:[%(levelname)s]:%(name)s\
                                      ::: \'%(message)s\'')
        ch.setFormatter(formatter)
        # add ch to logger
        logger.addHandler(ch)
        # 'application' code
        logger.debug(f'.__init__(pb:{pb}')

        self.logger = logger
        self.pb = pb
        self.rtd = self.load_rtd()
        self.translator = self.load_translator()
        self.tower_past_data = None
        self.last_date_loaded = None

    def load_rtd(self):
        self.logger.debug('.load_rtd()')
        with open(self.pb.get_relevant_towers_path(), 'r') as tower_f:
            return {l.strip().split(';')[0]:
                    ';'.join(l.strip().split(';')[-2:])
                    for l in tower_f.readlines()}

    def load_translator(self):
        self.logger.debug('.load_translator()')
        with open(self.pb.get_translator_path(), 'rb') as fobj:
            return pickle.load(fobj)

    def load_past_data(self, date_str, n_days):
        self.logger.debug(f'.load_past_data(date_str:{date_str},\
                          n_days: {n_days}')
        files_to_load = []
        date = parse(date_str)
        time_delta = timedelta(days=1)
        self.last_date_loaded = date
        for i in range(n_days):
            date = date - time_delta
            files_to_load.append(
                self.pb.build_past_data_file_name(date.strftime('%Y%m%d')))

        past_data = []
        for filename in files_to_load:
            self.logger.debug(f'loading file: "{filename}"')
            try:
                with open(self.pb.build_historical_path(filename), 'rb')\
                            as my_file:
                    past_data.append(pickle.load(my_file))
            except FileNotFoundError:
                print("File not found:" + self.pb.
                      build_historical_path(filename))

        self.logger.debug('.load_past_data() - COMPLETED')
        return self._create_data_structure(past_data, n_days)

    def update_past_data(self, date_str):
        self.logger.debug(f'update_past_data(date_str:"{date_str}")')
        self.logger.debug(f'last_date_loaded: "{self.last_date_loaded}"')
        date = parse(date_str)
        while(self.last_date_loaded < date):
            f_name = self.pb.build_past_data_file_name(
                       self.last_date_loaded.strftime('%Y%m%d'))
            self.logger.debug(f'loading file: "{f_name}"')
            with open(self.pb.build_historical_path(f_name), 'rb') as my_file:
                past_data = pickle.load(my_file)
                # for tower_id in set(self.rtd.values()):
                for tower_id in past_data.keys():
                    if tower_id in past_data:
                        for idx, val in enumerate(past_data[tower_id]):
                            self.tower_past_data[tower_id][idx].appendleft(val)
                    else:
                        for idx in range(1440):
                            self.tower_past_data[tower_id][idx].appendleft(
                                np.nan)

            self.last_date_loaded += timedelta(days=1)
        self.logger.debug('.update_past_data() - COMPLETED')

    def _create_data_structure(self, past_data_list, n_days):
        self.logger.debug(f"._create_data_structure(past_data_list:[...],\
         n_days:{n_days})")

        tower_past_data_structs = {}
        for tower_id in set(self.rtd.values()):
            tower_queues_list = [None] * 1440
            for ith_slot in range(1440):
                tower_historical = [np.nan] * n_days
                for idx, daily_data in enumerate(past_data_list):
                    if tower_id in daily_data:
                        tower_historical[idx] = daily_data[tower_id][ith_slot]
                tower_queues_list[ith_slot] = HDQ(tower_historical, maxlen=15)
                tower_queues_list[ith_slot]
            tower_past_data_structs[tower_id] = tower_queues_list

        self.logger.debug(f"_create_data_structure(...) - COMPLETED")

        self.tower_past_data = tower_past_data_structs
        return tower_past_data_structs

    def persist_historical_data(self, data):
        self.logger.debug(".persist_historical_data(data:[])")

        file_name = self.pb.build_past_data_file_name(
                        self.last_date_loaded.strftime('%Y%m%d') + "_test")
        with open(self.pb.build_historical_path(file_name), 'wb') as fd:
            pickle.dump(dict(data), fd)

        self.logger.debug(f".persist_historical_data(...) \
                          file_name:{file_name} - COMPLETED")
