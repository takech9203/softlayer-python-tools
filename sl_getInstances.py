#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'takechika'

import sys
from prettytable import PrettyTable
import SoftLayer
import sluser

SL_USERNAME = sluser.SL_USERNAME
SL_API_KEY = sluser.SL_API_KEY

_maskVirtualGuest = '''
    id,
    fullyQualifiedDomainName,
    primaryIpAddress,
    primaryBackendIpAddress,
    datacenter,
    location.pathString,
    billingItem.orderItem.order.userRecord.username,
    frontendRouters.hostname,
    backendRouters.hostname,
    billingItem.orderItem.recurringFee,
    billingItem.orderItem.hourlyRecurringFee,
    outboundPublicBandwidthUsage,
    networkVlans,
    networkVlanCount
    '''

_maskHardware = '''
    id,
    bareMetalInstanceFlag,
    fullyQualifiedDomainName,
    primaryIpAddress,
    primaryBackendIpAddress,
    datacenter,
    location.pathString,
    billingItem.orderItem.order.userRecord.username,
    frontendRouters.hostname,
    backendRouters.hostname,
    billingItem.orderItem.recurringFee,
    billingItem.orderItem.hourlyRecurringFee,
    outboundPublicBandwidthUsage,
    networkVlans,
    networkVlanCount
    '''

_tableHeader = [
    'id',
    'bm?',
    'fqdn',
    'public_ip',
    'backend_ip',
    'dc',
    'location',
    'owner',
    'fcr',
    'bcr',
    'mfee$',
    'hfee$',
    'out_bw',
    'vlan'
    ]

def lookup(dic, key, *keys):
    """A generic dictionary access helper.

    This helps simplify code that uses heavily nested dictionaries. It will
    return None if any of the keys in *keys do not exist.

    ::

        >>> lookup({'this': {'is': 'nested'}}, 'this', 'is')
        nested

        >>> lookup({}, 'this', 'is')
        None

    """
    if keys:
        return lookup(dic.get(key, {}), *keys)
    return dic.get(key)



client = SoftLayer.Client(username=SL_USERNAME, api_key=SL_API_KEY)

virtualGuests = client['Account'].getVirtualGuests(mask=_maskVirtualGuest)
hardwares = client['Account'].getHardware(mask=_maskHardware)

# for v in virtualGuests:
#     print(v)
#exit()

instances = hardwares + virtualGuests
#instances = virtualGuests

# Table definition
table = PrettyTable(_tableHeader)
table.padding_width = 1

# Get virtualGuests
count = 0
for inst in instances:
    table.add_row(
        [
            inst['id'],
            inst.get('bareMetalInstanceFlag','-'),
            inst['fullyQualifiedDomainName'],
            inst.get('primaryIpAddress', '--'),
            inst['primaryBackendIpAddress'],
            inst['datacenter']['name'],
            inst['location']['pathString'],
            lookup(inst, 'billingItem', 'orderItem', 'order', 'userRecord','username') or '--',
            inst['frontendRouters']['hostname'].split('.')[0] if not isinstance(inst['frontendRouters'],list) else inst['frontendRouters'][0]['hostname'].split('.')[0],
            inst['backendRouters'][0]['hostname'].split('.')[0],
            lookup(inst, 'billingItem', 'orderItem', 'recurringFee') or '-',
            lookup(inst, 'billingItem', 'orderItem', 'hourlyRecurringFee') or '-',
            round(float(inst['outboundPublicBandwidthUsage']),1),
            inst['networkVlanCount']
#            inst['networkVlans'][0]['vlanNumber'] or '-'
        ]
    )
    count = count + 1

print(table)
print(count, "instances")

exit()