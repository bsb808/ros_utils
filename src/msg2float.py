#!/usr/bin/env python
'''
This utility node is meant to convert from a message (user-defined) 
to a Float32 message for use with the Pid package with ROS.
'''

import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
from kingfisher_msgs.msg import Drive

class Node():
    def __init__(self):

        rospy.Subscriber("cmd_vel", Twist, self.callback)
        self.pub = rospy.Publisher("cmd_drive",Drive,queue_size=10)
        self.driveMsg = Drive()
        rospy.loginfo("Listening for Twist messages on topic=cmd_vel") 
        rospy.spin()
        
    def callback(self,data):
        rospy.loginfo("RX: Twist "+rospy.get_caller_id())
        rospy.loginfo("\tlinear:")
        rospy.loginfo("\t\tx:%f,y:%f,z:%f"%(data.linear.x,
                                            data.linear.y,
                                            data.linear.z))
        rospy.loginfo("\tangular:")
        rospy.loginfo("\t\tx:%f,y:%f,z:%f"%(data.angular.x,
                                            data.angular.y,
                                            data.angular.z))
        # scaling factors
        linfac = 0.2
        angfac = 0.05
        self.driveMsg.left = linfac*data.linear.x - angfac*data.angular.z
        self.driveMsg.right = linfac*data.linear.x + angfac*data.angular.z
        
        rospy.loginfo("TX: Drive ")
        rospy.loginfo("\tleft:%f, right:%f"%(self.driveMsg.left,
                                             self.driveMsg.right))
        self.pub.publish(self.driveMsg)


            

if __name__ == '__main__':
    rospy.init_node('msg2float', anonymous=True)
    
    # ROS Parameters
    in_topic = rospy.get_param('~input_topic','in_topic')
    inmsg_pkg = rospy.get_param('~input_msg_package','std_msgs')
    inmsg_type = rospy.get_param('~input_msg_type','Float32')
    inmsg_fields = rospy.get_param('~input_msg_fields','data')
    
    out_topic = rospy.get_param('~input_topic','out_topic')
    outmsg_pkg = rospy.get_param('~output_msg_package','std_msgs')
    outmsg_type = rospy.get_param('~output_msg_type','Float32')

    
    try:
        node=Node()
    except rospy.ROSInterruptException:
        pass
