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

import plot_vrx_utils as pvu
reload(pvu)

data = {}
logdir = '/home/bsb/data/flat_seas_000'
for f in os.listdir(logdir):
    if f.endswith(".p"):
        print ("Loading <%s>"%f)
        data[f] = pickle.load(open(os.path.join(logdir,f),"r"))



figure(1)
clf()
for k in data.keys():
    a, p, l, r = pvu.parse_bagname(k)
    plot(data[k].wamv_position.x, data[k].wamv_position.y,
         label='port=%0.2f, stbd=%0.2f'%(l, r))
legend()
axis('equal')
grid('true')
xlabel('X [m]')
ylabel('Y [m]')

show()
