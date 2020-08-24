import pickle
import numpy as np

# Need to creat the same data time used to pickle the info
'''
class Object(object):
    pass
'''
# OR
from bag2p import *

pfname = '/home/bsb/data/mono_world_a_0.0_p_10.00_x_1.00_y_0.00_Y_0.000.bag.p'
p = pickle.load(open(pfname,"r"))

figure(1)
clf()
plot(p.wamv_position.t0, p.wamv_position.z)
show()

