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
logdir = '/home/bsb/data/2020_08_25_manuevering_000'
for f in os.listdir(logdir):
    if f.endswith(".p"):
        print ("Loading <%s>"%f)
        data[f] = pickle.load(open(os.path.join(logdir,f),"r"))



# Sort the keys based on thrust magnitude
# make list of tuples
key_mag = []
for k in data.keys():
    a, p, l, r = pvu.parse_bagname(k)
    perc = r/l
    key_mag.append((perc,k))
# Sort by first element in the tuple
key_mag.sort(key=lambda tup: tup[0], reverse=True)

    
figure(1)
clf()
#for k in data.keys():
for km in key_mag: 
    k = km[1]
    a, p, l, r = pvu.parse_bagname(k)
    perc = r/l
    print perc
    plot(data[k].wamv_position.x, data[k].wamv_position.y,
         label='stbd= %0.2f%% port'%perc)
legend()
axis('equal')
grid('true')
xlabel('X [m]')
ylabel('Y [m]')

show()


#savefig(os.path.split(logdir)[1])
