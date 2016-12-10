#!/usr/bin/env python

import rospy
from ros_utils.msg import Keyvalue
from ros_utils.msg import Keyvaluearray
from random import random
kv = Keyvalue()
kva = Keyvaluearray()

kvp = Keyvalue()
kvp.name='P'

kvi = Keyvalue()
kvi.name = 'I'

kva.data.append(kvp)
kva.data.append(kvi)

def talker():
    pub = rospy.Publisher('keyvaluetest',Keyvaluearray, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        #kva.data[0].value = random()
        #kva.data[1].value = random()
        kvp.value=random()
        kvi.value=random()
        pub.publish(kva)
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
