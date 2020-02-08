#!/usr/bin/env python

from __future__ import print_function

import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy

from barc.msg import ECU

import sys, select, termios, tty

msg = """
Reading from the keyboard  and Publishing to ECU

w/s : forward/backward
a/d : rotate left/right
q/e : increase/decrease linear velocity
r/f : increase/decrease angular velocity
CTRL-C to quit
"""

moveBindings = {
        'w':(1,0),
        's':(-1,0),
        'a':(0,1),
        'd':(0,-1),
    }

speedBindings={
        'q':(1.1,1),
        'e':(.9,1),
        'r':(1,1.1),
        'f':(1,.9),
    }

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)

    pub = rospy.Publisher('ecu', ECU, queue_size = 1)
    rospy.init_node('teleop_keyboard')

    speed = rospy.get_param("speed")
    turn = rospy.get_param("turn")
    motor = 0
    servo = 0
    status = 0

    try:
        print(msg)
        while(1):
            key = getKey()
            if key in moveBindings.keys():
                motor = moveBindings[key][0]
                servo = moveBindings[key][1]
            elif key in speedBindings.keys():
                speed = speed * speedBindings[key][0]
                turn = turn * speedBindings[key][1]
                if (status == 14):
                    print(msg)
                status = (status + 1) % 15
            else:
                motor = 0
                servo = 0
                if (key == '\x03'):
                    break

            ecu = ECU()
            ecu.motor = motor*speed;
            ecu.servo = servo*turn; 
            pub.publish(ecu)

    except Exception as e:
        print(e)

    finally:
        ecu = ECU()
        ecu.motor = 0;
        ecu.servo = 0; 
        pub.publish(ecu)

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
