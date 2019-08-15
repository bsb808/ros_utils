import pickle
import numpy as np

pfname = '/home/bsb/Documents/annie_control_aug2019/data/20190814_annie_blue_arrow_testing/operational_logs/stefan_tests/2019-08-14-14-32-21.bag.p'

# Need to creat the same data time used to pickle the info
class Object(object):
    pass
data = pickle.load(open(pfname,"r"))

# Convert N/E velocities to surge sway
annie_vel = Object()
annie_vel.t = data.jacm_gps_dynamics.t
annie_vel.surge = []
annie_vel.sway = []
annie_vel.yaw = []
for n, e, h, hr in zip(data.jacm_gps_dynamics.velocity_north_ms,
                       data.jacm_gps_dynamics.velocity_east_ms,
                       data.jacm_gps_dynamics.heading_deg,
                       data.jacm_gps_dynamics.rate_of_turn_deg_sec):
    hdg = h * math.pi/180.0
    annie_vel.surge.append(n*math.cos(hdg)+e*math.sin(hdg))
    annie_vel.sway.append(-1.0*n*math.sin(hdg)+e*math.cos(hdg))
    annie_vel.yaw.append(-1.0*hr*math.pi/180.0)

t0 = annie_vel.t[0]
annie_vel.t0 = np.array(annie_vel.t)-t0
data.cmd_vel.t0 = np.array(data.cmd_vel.t)-t0

# Correct for deadband
def cmd2vel(cp,deadband=40.0):
    if cp < -deadband/2:
        return (cp + deadband/2)*100.0/(100-deadband/2) 
    elif cp > deadband/2:
        return (cp - deadband/2)*100.0/(100-deadband/2) 
    else:
        return 0.0

max_surge = 2.0
surge_cmd_percent = array(data.cmd_vel.linear.x)/max_surge*100.0
surge_actual = []
for s in surge_cmd_percent:
    surge_actual.append(cmd2vel(s)/100.0*max_surge)

figure(1)
clf()
plot(annie_vel.t0,annie_vel.surge,label='Annie GPS')
plot(data.cmd_vel.t0,data.cmd_vel.linear.x,label='Cmd')
plot(data.cmd_vel.t0,surge_actual,label='Cmd_Deadband')
legend()
grid(True)
xlabel('Time [s]')
ylabel('Surge [m/s]')

max_sway = 0.56
sway_cmd_percent = array(data.cmd_vel.linear.y)/max_sway*100.0
sway_actual = []
for s in sway_cmd_percent:
    sway_actual.append(cmd2vel(s)/100.0*max_sway)


figure(2)
clf()
plot(annie_vel.t0,annie_vel.sway,label='Annie GPS')
plot(data.cmd_vel.t0,data.cmd_vel.linear.y,label='Cmd')
plot(data.cmd_vel.t0,sway_actual,label='Cmd_Deadband')

legend()
grid(True)
xlabel('Time [s]')
ylabel('Sway [m/s]')

figure(3)
clf()
plot(data.cmd_vel.t0,np.array(data.cmd_vel.angular.z)*180.0/math.pi,label='Cmd')
plot(annie_vel.t0,np.array(annie_vel.yaw)*180.0/math.pi,label='Annie')
legend()
grid(True)
xlabel('Time [s]')
ylabel('Yaw [deg/s]')

show()

