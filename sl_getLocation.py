#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'takechika'

from prettytable import PrettyTable
import SoftLayer
import sluser

SL_USERNAME = sluser.SL_USERNAME
SL_API_KEY = sluser.SL_API_KEY

_mask = '''
    id,
    fullyQualifiedDomainName,
    datacenter,
    location.pathString
    '''

_TableHeader = [
    'VM ID',
    'FQDN',
    'Datacenter',
    'Location'
    ]


client = SoftLayer.Client(username=SL_USERNAME, api_key=SL_API_KEY)
virtualGuests = client['Account'].getVirtualGuests(mask=_mask)

# Table definition
table = PrettyTable(_TableHeader)
table.padding_width = 1

# Get list
count = 0
#for vg in sorted(virtualGuests):
for vg in virtualGuests:
#    print(vg)
    table.add_row(
        [
            vg['id'],
            vg['fullyQualifiedDomainName'],
            vg['datacenter']['longName'],
            vg['location']['pathString']
        ]
    )
    count = count + 1


print(table)
print(count, "VMs")


print(virtualGuests)

exit()

