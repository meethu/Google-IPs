#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import requests
from netaddr import *

# IP ranges that Google makes available to users on the internet
google = requests.get("https://www.gstatic.com/ipranges/goog.json")
# Global and regional external IP address ranges for customers' Google Cloud resources
cloud = requests.get("https://www.gstatic.com/ipranges/cloud.json")

googleIP, cloudIP = google.json(), cloud.json()
googleList, cloudList = [], []

# Extract IPv4 or IPv6 according to your needs
for prefixes in googleIP["prefixes"]:
    if "ipv4Prefix" in prefixes:
        googleList.append(prefixes["ipv4Prefix"])

for prefixes in cloudIP["prefixes"]:
    if "ipv4Prefix" in prefixes:
        cloudList.append(prefixes["ipv4Prefix"])

# Subtract the usable ranges from the complete list
googleIPSet, cloudIPSet = IPSet(googleList), IPSet(cloudList)
googleUniqe = googleIPSet - cloudIPSet

gooogleCidr = cidr_merge(sorted(googleUniqe))
with open("./Google_IPs.txt", "w") as f:
    for ipaddr in gooogleCidr:
        f.write(str(ipaddr.ip)  + "/" + str(ipaddr.prefixlen) + "\n")