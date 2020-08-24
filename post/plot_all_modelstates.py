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

from plot_vrx_utils import parse_bagname

data = {}
logdir = '/home/bsb/data/head_seas_001'
logdir = '/home/bsb/data/beam_seas_000'
for f in os.listdir(logdir):
    if f.endswith(".p"):
        print ("Loading <%s>"%f)
        data[f] = pickle.load(open(os.path.join(logdir,f),"r"))

whattoplot = [('wamv_position','z'),
              ('wamv_euler','pitch'),
              ('wamv_euler','roll')]
# Amplitudes
N = 10000
amp = Object()
for wtp in whattoplot:
    setattr(amp,wtp[1],[])
setattr(amp,'file',[])
setattr(amp,'amplitude',[])
setattr(amp,'period',[])

for wtp in whattoplot:
    figure(wtp[1])
    clf()

for k in data.keys():
    getattr(amp,'file').append(k)
    a, p, l, r = parse_bagname(k)
    getattr(amp,'amplitude').append(a)
    getattr(amp,'period').append(p)
        
    
    for wtp in whattoplot:
        figure(wtp[1])
        t0 = getattr(getattr(data[k],wtp[0]),'t0')
        vals = getattr(getattr(data[k],wtp[0]),wtp[1])
        last_vals = vals[-N:]
        a = (max(last_vals) - min(last_vals)) / 2.0
        print "%s, %s, %.2f"%(k,wtp[1],a)
        getattr(amp,wtp[1]).append(a)

        plot(t0, vals, label=k)

    xlabel('Time [s]')
    ylabel(wtp[1])         
    legend()

figure('amp')
clf()
ax1 = subplot(1,1,1)
color = 'tab:blue'

ax1.plot(amp.amplitude, amp.pitch, 'o', label='Pitch')
ax1.plot(amp.amplitude, amp.roll, 'o', label='Roll')
legend()
xlabel('Wave Amplitude [m]')
ax1.set_ylabel('Euler angle [rad]', color=color)
grid(True)
ax1.set_ylim([0, ax1.get_ylim()[1]*1.0])
ax1.set_title(os.path.split(logdir)[1])



color = 'tab:red'
ax2 = ax1.twinx()
plot(amp.amplitude, amp.z, 'o', color=color, label='Heave')
legend(loc='center left')
ax2.set_ylabel('Heave [m]', color=color)
ax2.tick_params(axis='y', labelcolor=color)
# Tweak scaling
ax2.set_ylim([0, ax2.get_ylim()[1]*1.1])


show()

