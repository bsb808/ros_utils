import pickle
import numpy as np
import os
# Need to creat the same data time used to pickle the info
'''
class Object(object):
    pass
'''
# OR
from bag2p import *


def parse_bagname(fname):
    '''
    Extract numerical values from file names
    '''
    l = fname.split('_')
    amplitude = float(l[3])
    period = float(l[5])
    left = float(l[13])
    right = float(l[15])
    return (amplitude, period, left, right)


