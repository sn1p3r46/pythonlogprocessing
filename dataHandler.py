from historicalDataQueue import HistoricalDataQueue as HDQ
from dateutil.parser import parse
from datetime import timedelta

import numpy as np
import warnings
import pickle


class DataHandler:

    def __init__(self, path_builder,):
        self.pb = path_builder
        self.rtd = self.load_rtd()
        self.translator = self.load_translator()
        self.tower_past_data = None
        self.last_date_loaded = None

    def load_rtd(self):
        print('>[load_relevant_towers(path)]\nLOADING RELEVANT TOWERS\n---')
        with open(self.pb.get_relevant_towers_path(), 'r') as tower_f:
            return {l.strip().split(';')[0]:
                        ';'.join(l.strip().split(';')[-2:])
                        for l in tower_f.readlines()}

    def load_translator(self):
        with open(self.pb.get_translator_path(), 'rb') as fobj:
            return pickle.load(fobj)

    def load_past_data(self, date_str, n_days):
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
            try:
                with open(self.pb.build_historical_path(filename), 'rb')\
                            as my_file:
                    past_data.append(pickle.load(my_file))
            except FileNotFoundError:
                print("File not found:" + self.pb.
                      build_historical_path(filename))

        print("Historical data loaded!")
        return _create_data_structure(past_data, n_days)

    def update_past_data(self, date_str):
        date = parse(date_str)
        while(self.last_date_loaded < date):
            filename = self.pb.build_past_data_file_name(
                                        self.last_date_loaded.strftime('%Y%m%d'))

            with open(self.pb.build_historical_path(filename), 'rb') as my_file:
                print(self.pb.build_historical_path(filename))
                past_data = pickle.load(my_file)
                # for tower_id in set(self.rtd.values()):
                for tower_id in past_data.keys():
                    if tower_id in past_data:
                        for idx, val in enumerate(past_data[tower_id]):
                            self.tower_past_data[tower_id][idx].appendleft(val)
                    else:
                        for idx in range(1440):
                            self.tower_past_data[tower_id][idx].appendleft(np.nan)

            self.last_date_loaded += timedelta(days=1)

    def _create_data_structure(self, past_data_list, n_days):
        print('>[create_data_structure(past_data_list, number_of_slices,' +
              ' number_of_days)]\nCREATING DATA STRUCTURE\n---')

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


        print('>[create_data_structure(past_data_list, number_of_slices,' +
              ' number_of_days)]\nDATA STRUCTURE CREATED\n---')
        self.tower_past_data = tower_past_data_structs
        return tower_past_data_structs

    def persist_historical_data(self, data):
        file_name = self.pb.build_past_data_file_name(
                                        self.last_date_loaded + "_test")
        with open(self.pb.build_historical_path(file_name), 'wb') as fd:
            pickle.dump(dict(data), fd)
