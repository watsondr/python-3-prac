# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 22:56:01 2020

@author: campb
"""

def parse_rows_with(reader, parsers):
    """
    Use the reader to parse the rows with the perscribed expected format.
    
    Yield means the reader can do something with one item, then move on
    without escaping the function process.
    """
    
    for row in reader:
        yield parse_row(row, parsers)
        
def parse_row(input_row, parsers):
    """
    Using the list of parsers (which can be None for do nothing)
    Apply the appropriate format to each item in the input_row
    """
    
    return [parser(value) if parser is not None else value
                        for value, parser in zip(input_row, parsers)]