#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'takechika'

import SoftLayer
import sluser

SL_USERNAME = sluser.SL_USERNAME
SL_API_KEY = sluser.SL_API_KEY

client = SoftLayer.Client(username=SL_USERNAME, api_key=SL_API_KEY)


### Data Center

print("### Data Center and Region ###")
dataCenters = client['Location'].getDatacenters()
for dc in dataCenters:
#    print(dc)
    address = client['Location'].getLocationAddress(id=dc['id'])
    region = client['Location'].getRegions(id=dc['id'])
    print(dc, region, address)
print()

### PoP

print("### PoP ###")
pops = client['Location'].getpointOfPresence()
for pop in pops:
    print(pop)
print()

### Object Storage Datacenter

print("### Object Storage ###")
objectStorages = client['Location'].getAvailableObjectStorageDatacenters()
for os in objectStorages:
    print(os)
print()





exit()



### Data Center


_vg_mask = '''
    id,
    fullyQualifiedDomainName,
    location.pathString'''

virtualGuests = client['Account'].getVirtualGuests(mask=_vg_mask)
for vg in virtualGuests:
    print(vg['id'],
          vg['fullyQualifiedDomainName'],
          vg['location']['pathString'] )
exit()
