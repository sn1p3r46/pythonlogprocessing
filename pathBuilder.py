#  This Module is an helper to build paths useful to the application

import os

class PathBuilder():

    _root = "/home/andre/Documents/ELTE/TkPrj/Documentation/data"
    _archive_root = "/media/andre/HDD/TkData/sorted/filtered_null_and_empty"
    _my_file = 'motionl_MT_ngprs_T.out.20161001_sorted_4'
    _highways_towers_coordinates_name = '/highways_towers_coordinates.csv'
    _highways_towers_cells_name = '/highways_towers_cells.csv'
    _hack_cells_flatten_name = '/hack_cells_flatten.txt'
    _historical_prefix = 'daily_towers_slots.'
    _competence_name = '/competence_int_new.json'
    _historical_path = '/historical'
    _translator_name = '/translator.pkl'
    _historical_suffix = '_2_.pkl'
    _computed_path = '/computed'

    def __init__(self):
        pass

    def __str__(self):
        return "pathBuilder"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def get_relevant_towers_path(cls):
        return cls._root + cls._computed_path + cls._highways_towers_cells_name

    @classmethod
    def get_stream_file_path(cls):
        return cls._archive_root + '/' + cls._my_file

    @classmethod
    def get_stream_files_paths(cls):
        return sorted([f[0] + '/' + f1 for
                       f in os.walk(cls._archive_root)
                       for f1 in f[2]])

    @classmethod
    def build_past_data_file_name(cls, date_str):
        return cls._historical_prefix + date_str + cls._historical_suffix

    @classmethod
    def get_competence_path(cls):
        return cls._root + cls._computed_path + cls._competence_name

    @classmethod
    def get_translator_path(cls):
        return cls._root + cls._computed_path + cls._translator_name

    @classmethod
    def build_historical_path(cls, file_name):
        return cls._root + cls._computed_path + cls._historical_path + '/' + \
                file_name
