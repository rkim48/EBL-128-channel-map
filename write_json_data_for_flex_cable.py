import numpy as np
from numpy import nan as nan
import json


def write_json_data_for_flex_cable():
    # from spreadsheet
    old_j4_ids = [nan, nan, nan, nan, nan, nan, nan, 3, 1, 5, 0, 7, 2, 9, 4, 11,
                  6, 13, 8, 15, 10, 16, 12, 18, 14, 20, 17, 22, 19, 24, 21, 26,
                  23, 28, 25, 30, 27, 32, 29, 33, 31, 35, 34, 37, 36, 39, 38, 41,
                  40, 43, 42, 45, 44, 47, 46, 48, 49, 50, 51, 52, 53, 54, 55, 56,
                  57, 58, 59, 60, 61, 62, 63]

    old_j3_ids = [nan, nan, nan, nan, nan, nan, nan, 124, 126, 122, 127, 120,
                  125, 118, 123, 116, 121, 114, 119, 112, 117, 111, 115, 109,
                  113, 107, 110, 105, 108, 103, 106, 101, 104, 99, 102, 97,
                  100, 96, 98, 94, 95, 92, 93, 90, 91, 88, 89, 86, 87, 84, 85,
                  82, 83, 80, 81, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69,
                  68, 67, 66, 65, 64]

    data = {
        "j3": old_j3_ids,
        "j4": old_j4_ids
    }

    with open('old_flex_cable_hardware_ids.json', 'w') as json_file:
        json.dump(data, json_file)


if __name__ == '__main__':
    write_json_data_for_flex_cable()
