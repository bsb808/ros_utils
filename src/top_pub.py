#!/usr/bin/env python
'''
Node to convert from quaternions to rpy
'''

import rospy
from std_msgs.msg import Float32MultiArray

from subprocess import Popen, PIPE

def talker():
    procname = 'gzserver'
    pub = rospy.Publisher('top_pub_%s'%procname, Float32MultiArray, queue_size=10)
    rospy.init_node('top_pub', anonymous=True)
    rate = rospy.Rate(2) # 2hz
    msg = Float32MultiArray()
    cpu = -1.0
    mem = -1.0
    while not rospy.is_shutdown():
        

        cmd='ps -C gzserver -o "%cpu" --sort=-pcpu --no-headers | head -n 1'
        process = Popen(cmd, shell=True, stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        try:
            cpu=float(output)
        except ValueError:
            rospy.logwarn("Can't read cpu - is process running")
            cpu = -1.0
        cmd='ps -C gzserver -o "%mem" --sort=-pcpu --no-headers | head -n 1'
        process = Popen(cmd, shell=True, stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        try:
            mem=float(output)
        except ValueError:
            rospy.logwarn("Can't read mem - is process running")
            mem = -1.0
        
        msg.data = [cpu,mem]
        rospy.loginfo(str(msg.data))
        if mem > 0 and cpu > 0:
            pub.publish(msg)
        else:
            rospy.logwarn("Not publishing")
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
