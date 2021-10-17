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
	scale  = Vector3(2, 4, 0.69)
	p1     = Point(0, 0, 0)
	p2     = Point(3, 0, 0)
	cnt = 0
	while not rospy.is_shutdown() :
		marker.action = Marker.ADD
		marker.header.frame_id = 'map'
		marker.header.stamp    = rospy.Time.now()
		marker.type     = Marker.ARROW
		marker.pose.orientation.y = 0
		marker.pose.orientation.w = 1
		marker.scale = scale
		marker.color.r = 0.2
		marker.color.g = 0.5
		marker.color.b = 1.0
		marker.color.a = 0.3
		p1 = Point(0, 0, 0)
		p2 = Point(cnt, 0, 1)
		marker.points = [p1, p2]
		cnt += 1
		if cnt == 5 :
			cnt = 0
		pub.publish(marker)
		r.sleep()

if __name__=='__main__' :
	main()