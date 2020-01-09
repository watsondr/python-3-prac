# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 22:54:38 2020

@author: campb
"""
 
import dateutil.parser
import csv
from data_claning_functions import parse_rows_with

data = []

with open("some_file_of_data.csv", "r") as file:
    reader = csv.reader(file)
    for line in parse_rows_with(reader, [dateutil.parser.parse, None, float, None]):
        data.append(line)