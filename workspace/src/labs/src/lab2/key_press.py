import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
import math

class Relay:

  def __init__(self, dt=.05):
    rospy.init_node('serial_node_parser');
    self.pub = rospy.Publisher('ecu', ECU, queue_size=10)
    rate = rospy.Rate(1.0/dt)

  def start_subscribe(self):
    rospy.Subscriber("keyboard/keyup", Key, self.callback)

  def callback(self, key):
    

  def start_publish(self):
    while not rospy.is_shutdown():
      self.pub.publish(self.joint_state)
      rate.sleep()

if __name__ == '__main__':
  node_parser = SerialNodeParser()
  node_parser.start_subscribe()
  node_parser.start_publish()