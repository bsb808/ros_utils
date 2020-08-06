#!/usr/bin/env python
'''
Node used in roslaunch to stop all nodes (e.g., simulation) at specified time

See the lander_ex.launch file for usage pattern.
'''

import rospy

if __name__ == '__main__':
    rospy.init_node('lander')

    if rospy.is_shutdown():
        rospy.ROSException('ROS master is not running!')

    timeout = 0.0
    if rospy.has_param('~timeout'):
        timeout = rospy.get_param('~timeout')
        if timeout <= 0:
            raise rospy.ROSException('Termination time must be a positive floating point value')

    print('Starting simulation timer - Timeout = %.2f s'%(timeout))
    rate = rospy.Rate(10)
    while rospy.get_time() < timeout:
        rate.sleep()

    print('Landing after %.2f s...'%timeout)
