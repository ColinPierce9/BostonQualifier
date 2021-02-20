import pandas as pd
import numpy as np
import numpy
import requests
import io
from loadextract import *

def extract_clean_data(table):
    '''
    Extract a table from the clean database
    Returns a dataframe
    The valid tables to enter: runner, crosstrain, speed, program
    '''
    data = extract_data(table)
    return data
