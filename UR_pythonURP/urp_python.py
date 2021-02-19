#!/usr/bin/env python
import urx

rob = urx.Robot("192.168.0.7")
def main() :
	while True :
		print(rob.getl())

if __name__=="__main__" :
	main()
