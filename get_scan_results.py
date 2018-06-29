#!/usr/bin/env python
# -*- coding: utf-8 -*-

from securitycenter import SecurityCenter5
from getpass import getpass
import json

HOST = 'sec-center-prod-01.uit.tufts.edu'
OUTPUT_FILE = 'out.txt'

# 		login_sc()
#
# Function to open a connection with the specified Security Center 5 host. Asks user for their login information and
# then proceeds to try to establish an authenticated connection.
# Input  - none
# Output - authenticated SecurityCenter5 object
def login_sc():
    user = raw_input("Username: ")
    pw = getpass()
    sc = SecurityCenter5(HOST)

    sc.login(user, pw)
    return sc


def getScanResults(ipAddress):
	sc = login_sc()
	output = sc.analysis(('ip', '=', ipAddress), tool='vulndetails')
	f = open(OUTPUT_FILE, 'w')
	f.write(json.dumps(output))
	f.close()

if __name__ == '__main__':
	getScanResults('10.242.110.1')