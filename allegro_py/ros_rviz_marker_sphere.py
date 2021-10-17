#!/usr/bin/env python
import rospy
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Pose, Vector3, Quaternion, Point
from std_msgs.msg import Header, ColorRGBA

def main() :
	pub = rospy.Publisher('markerTest', Marker, queue_size=10)
	rospy.init_node('testNode', anonymous=True)

	r = rospy.Rate(2)
	marker = Marker()
	marker = Marker(type=Marker.SPHERE, id=0, lifetime=rospy.Duration(10), pose=Pose(Point(1, 1, 1), Quaternion(0, 0, 0, 1)), scale = Vector3(0.05, 0.05, 0.05), header=Header(frame_id='map'), color=ColorRGBA(90.0, 2.0, 0.0, 0.8))
	cnt = 0
	while not rospy.is_shutdown() :
		marker = Marker(type=Marker.SPHERE, id=0, lifetime=rospy.Duration(10), pose=Pose(Point(cnt, 1, 1), Quaternion(0, 0, 0, 1)), scale = Vector3(0.05, 0.05, 0.05), header=Header(frame_id='map'), color=ColorRGBA(90.0, 2.0, 0.0, 0.8))
		cnt += 1
		if cnt == 5 :
			cnt = 0
		pub.publish(marker)
		r.sleep()

if __name__=='__main__' :
	main()