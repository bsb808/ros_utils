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
pfname = '/home/bsb/data/leanis_resonance/2020-09-14-16-49-22.bag.p'
p = pickle.load(open(pfname,"r"))


figure(1)
clf()
plot(p.cusv_position.t0, p.cusv_position.z)
grid(True)
xlabel('Time [s]')
ylabel('Heave [m]')

figure(2)
clf()
plot(p.cusv_euler.t0, p.cusv_euler.pitch)
grid(True)
xlabel('Time [s]')
ylabel('Pitch [rad]')

figure(3)
clf()
plot(p.cusv_euler.t0, p.cusv_euler.roll)
grid(True)
xlabel('Time [s]')
ylabel('Roll [rad]')

show()

