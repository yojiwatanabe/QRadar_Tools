#!/usr/bin/env python

"""
get_ip_from_mac.py

Script to find the most recent IP address assigned to a MAC address. Queries QRadar for IP values assigned to a MAC
address and processes the output, returning the most recently assigned IP.

"""

import sys
import json
import requests

QRADAR_URL = ''
AUTH_TOKEN = ''
GET_METHOD = 'GET'
POST_METHOD = 'POST'
ASSETS_ENDPOINT = '/api/asset_model/assets'
LOGOUT_ENDPOINT = '/api/auth/logout'
BASE_HEADER = {'Version': '9.0',
               'Accept': 'application/json',
               'Content-Type': 'application/json',
               'SEC': AUTH_TOKEN}


#       prepare_request()
#
# Prepares a request to be send to QRadar. Allows a user to craft an HTML request according to QRadar specifications.
# Also allows users to personalize requests to be more specific about the data to be returned.
# Input  - method: string, HTML method to be used (e.g. 'POST')
#          endpoint: string, REST API endpoint to connect to
#          header: dict, key:value pairs to be added to the header
#          params: params: dict, key:value pairs to be added to the parameters
def prepare_request(method, endpoint, header=None, params=None):
    new_header = BASE_HEADER
    if header:
        for field in header:
            new_header[field] = str(header[field])

    request = requests.Request(method, url=QRADAR_URL+endpoint, headers=new_header, params=params)
    return request.prepare()


#       query_by_mac()
#
# Queries QRadar for the IP address belonging to a specific MAC address. In the case of multiple IP addresses found,
# returns the most recent one as given by interfaces[ip_addresses[last_seen_profiler]]
# Input  - mac: string, MAC address to look up
#          session: requests session object, the current session
# Output - list containing integers representing the offense IDs
def query_by_mac(mac, session):
    request = prepare_request(GET_METHOD, ASSETS_ENDPOINT,
                              None, {'fields': 'interfaces(ip_addresses(last_seen_profiler, value))',
                                     'filter': 'interfaces contains mac_address=\"' + mac + '\"'})

    response = session.send(request)

    content = json.loads(response.content)[0]

    return content


def end_session(session):
    try:
        request = prepare_request(POST_METHOD, LOGOUT_ENDPOINT, None, None)
        session.send(request)
    except Exception as e:
        print e
        print 'Logout failed, exiting'
        exit(1)
    return


def get_ip(mac_address):
    s = requests.Session()
    ip_address = query_by_mac(mac_address, s)
    end_session(s)

    return ip_address


# # # # # # # # # # # # # # # # # # # # # # # # # ## #  ##
if __name__ == '__main__':
    get_ip(sys.argv[1])
