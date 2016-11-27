#!/usr/bin/env python
'''
This utility node is meant to convert from a message (user-defined) 
to a Float32 message for use with the Pid package with ROS.
'''
import sys
import rospy

import functools

from std_msgs.msg import Float32

def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

sentinel = object()

def rgetattr(obj, attr, default=sentinel):
     if default is sentinel:
         _getattr = getattr
     else:
         def _getattr(obj, name):
             return getattr(obj, name, default)
     return functools.reduce(_getattr, [obj]+attr.split('.'))


class Node():
    def __init__(self,inmsg_fields,outmsg_fields):
        self.pubmsg = None
        self.pub = None
        self.inmsg_fields = inmsg_fields
        self.outmsg_fields = outmsg_fields
        
        
    def callback(self,msg):
        # Decode
        val = float(rgetattr(msg,inmsg_fields))
        #print 'val: '+str(val)
        #print "out: "+outmsg_fields
        # Encode
        rsetattr(self.pubmsg,outmsg_fields,val)
        #now = rospy.get_rostime()
        #print("%i %i"%(now.secs,now.nsecs))
        self.pub.publish(self.pubmsg)


if __name__ == '__main__':
    
    rospy.init_node('msg2msg', anonymous=True)
    
    # ROS Parameters
    in_topic = rospy.get_param('~input_topic','in_topic')
    inmsg_pkg = rospy.get_param('~input_msg_package','std_msgs')
    inmsg_type = rospy.get_param('~input_msg_type','Float32')
    inmsg_fields = rospy.get_param('~input_msg_fields','data')
    
    out_topic = rospy.get_param('~output_topic','out_topic')
    outmsg_pkg = rospy.get_param('~output_msg_package','std_msgs')
    outmsg_type = rospy.get_param('~output_msg_type','Float32')
    outmsg_fields = rospy.get_param('~output_msg_fields','data')

    # Import the proper messages
    inmod = __import__(inmsg_pkg+'.msg',fromlist=[inmsg_type])
    outmod = __import__(outmsg_pkg+'.msg',fromlist=[outmsg_type])

    # Initiate node object
    node=Node(inmsg_fields,outmsg_fields)
    
    # Setup outbound message
    outmsg = getattr(outmod,outmsg_type)
    node.pubmsg = outmsg()

    # Setup publisher
    rospy.loginfo("Subscribing to %s for %s messages and fields %s"%
                  (in_topic,inmsg_pkg+'.'+inmsg_type,inmsg_fields))
    rospy.loginfo("Publishing to %s with %s messages and fields %s"%
                  (out_topic,inmsg_pkg+'.'+outmsg_type,outmsg_fields))
    node.pub = rospy.Publisher(out_topic,outmsg,queue_size=10)

    # Setup subscriber
    inmsg = getattr(inmod,inmsg_type)
    rospy.Subscriber(in_topic,inmsg,node.callback)

    # Validate that fields are setup correctly
    try:
        testval = float(rgetattr(inmsg(),inmsg_fields))
        testmsg = outmsg()
        rsetattr(node.pubmsg,outmsg_fields,testval)
    except:
        rospy.logerr("Problem encodind/decoding messages "
                     "with specified types and fields!")
        sys.exit()
    
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
