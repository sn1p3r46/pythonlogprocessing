# TkPrj 0.5 Alpha

## Technical Documentation

### File `const.py`:

```python
import numpy as np

USR = 0
DATE = 1
TWR = 2

cutpoints = {

    3: [-np.inf, -0.43, 0.43, np.inf],
    4: [-np.inf, -0.67, 0, 0.67, np.inf],
    5: [-np.inf, -0.84, -0.25, 0.25, 0.84, np.inf],
    6: [-np.inf, -0.97, -0.43, 0, 0.43, 0.97, np.inf],
    7: [-np.inf, -1.07, -0.57, -0.18, 0.18, 0.57, 1.07, np.inf],
    8: [-np.inf, -1.15, -0.67, -0.32, 0, 0.32, 0.67, 1.15, np.inf],
    9: [-np.inf, -1.22, -0.76, -0.43, -0.14, 0.14, 0.43, 0.76, 1.22, np.inf],
    10: [-np.inf, -1.28, -0.84, -0.52, -0.25, 0, 0.25, 0.52, 0.84, 1.28,
         np.inf]

}
```

The `const.py` file contains just some constant values useful for the core application.

Provided that the typical input log has the following characteristics:

```'USER_ID';DATE TIME;TOWER_ID```

`USR` stands for the index of the field containing the USER_ID.

`DATE` stands for the index of the field containing the DATE and TIME stamps of the log.

`TWR` stands for the index of the field containing the TOWER_ID.

The `cutpoints` variable contains a list-of-lists containing the statistical table describing the values that divide with an equal probability a
normal distribution.

---

### File `pathBuilder.py`:

```python
#  This Module is an helper to build paths useful to the application

class PathBuilder():

    _root = "/mnt/disk01/agalloni/telecom/data"
    _my_file = '/computed/minimal/sorted/motionl_MT_ngprs_T' + \
               '.out.20161001_sorted_4'
    _highways_towers_coordinates_name = '/highways_towers_coordinates.csv'
    _highways_towers_cells_name = '/highways_towers_cells.csv'
    _hack_cells_flatten_name = '/hack_cells_flatten.txt'
    _historical_prefix = 'daily_towers_slots.'
    _competence_name = '/competence_int_new.json'
    _historical_path = '/historical/newids'
    _translator_name = '/translator.pkl'
    _historical_suffix = '_1_.pkl'
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
        return cls._root + cls._my_file

    @classmethod
    def build_past_data_file_name(cls, date_str):
        return cls._historical_prefix + date_str + cls._historical_suffix

    @classmethod
    def build_historical_path(cls, file_name):
        return cls._root + cls._computed_path + cls._historical_path + '/' + \
                file_name

    @classmethod
    def get_competence_path(cls):
        return cls._root + cls._computed_path + cls._competence_name

    @classmethod
    def get_translator_path(cls):
        return cls._root + cls._computed_path + cls._translator_name

```

The `pathBuilder.py` file contains a class intended to be a helper to retrieve files given some constants fields. This class has several static methods useful to build or retrieve the paths of the requested files. This helper have been created to make the code more readable and tidy.

Follows the description of every method:

```python
PathBuilder.get_relevant_towers_path()
```

This function returns the the absolute path to the `highways_towers_cells.csv`; this file is a `csv` file containing three columns: `TID;LAT;LON`, namely the id of the tower and its latitude and longitude.

```
PathBuilder.build_past_data_file_name(date_str)
```

This function provided a string referring to a specific date with the following format: `%Y%m%d` returns the name of the file containing the records of the tower cells activity recorded on that specific day. The historical data is stored as python's pickles files, each file contains a Python dictionary whose key is the coordinate of the tower and whose values are lists representing the busyness of the tower in a specific period of the day.

```
PathBuilder.build_historical_path(file_name)
```

This function given the name of the file containing the historical data for a specific day it returns the absolute path of that file.

```
PathBuilder.get_competence_path()
```

This function returns the absolute path of the file containing a dictionary whose keys are the unique ids of the cells for the front-end and the unique ids of the `.geojson` file describing the highways' infrastructure, this file creates a correspondence between the towers and the highways' segments it is sent just once at the beginning of the communication, `{'FRONTEND_INT_ID':['way/25943247',...,'way/25943250']}`.


```
PathBuilder.get_translator_path()
```

This function returns the absolute path of the translator file, this file is a python's pickle file that stores a dictionary containing the coordinates of the towers as id and the id of the tower regarding the front-end `{'Coordinates':FRONTEND_INT_ID}`.

---

#### Short Data-Shape Recap:

```
Coordinates : String = 'LON;LAT'

relevant_towers_dic : {String : String } = {'TID':'Coordinates'}

competence : {String: [String]} = {'FRONTEND_INT_ID':['way/25943247',...,'way/25943250']}

translator {String : Int} : = {'Coordinates':FRONTEND_INT_ID}
```
