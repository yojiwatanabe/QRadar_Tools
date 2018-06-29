#!/usr/bin/env python

'''
host.py
This is a class that represents a host. It doesn't have member
functions but has four attributes
'''
class Host:
	str ipAddress
	strmacAddress
	machineType = ''
	policyID = 0

	'''
	__init__()
	This is the constructor for the class. It has four optional
	parameters. Passing arguments will result in initialization
	of the attributes of this class
	'''
	def __init__(self, ip='', mac='', machine='', policy=0):
		self.ipAddress = ip
		self.macAddress = mac
		self.machineType = machine
		self.policyID = policy