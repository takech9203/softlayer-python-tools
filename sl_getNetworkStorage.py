#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'takechika'

from prettytable import PrettyTable
import SoftLayer
import sluser

SL_USERNAME = sluser.SL_USERNAME
SL_API_KEY = sluser.SL_API_KEY

_maskNetworkStorage = '''
    hardware,
    iops,
    iscsiLuns,
    iscsiLunCount,
    osTypeId,
    serviceResource,
    serviceResource.datacenter,
    serviceResourceName,
    serviceResourceBackendIpAddress,
    storageGroups,
    vendorName
    '''

_tableHeader = [
    'id',
    'nasType',
    'datacenter',
    'username',
    'gb',
    'iops',
    'serviceResourceName',
    'serviceResourceBackendIpAddress',
    'serviceResourceType',
    'hardware',
    'vendorName',
    'osTypeId'
    ]

def lookup(dic, key, *keys):
    """A generic dictionary access helper.

    This helps simplify code that uses heavily nested dictionaries. It will
    return None if any of the keys in *keys do not exist.

        > lookup({'this': {'is': 'nested'}}, 'this', 'is')
        nested

        > lookup({}, 'this', 'is')
        None

    """
    if keys:
        return lookup(dic.get(key, {}), *keys)
    return dic.get(key)


client = SoftLayer.Client(username=SL_USERNAME, api_key=SL_API_KEY)
networkStorage = client['Account'].getNetworkStorage(mask=_maskNetworkStorage)
#networkStorage = client['Account'].getIscsiNetworkStorage(mask=_maskNetworkStorage)


# Table definition
table = PrettyTable(_tableHeader)
table.padding_width = 1


for ns in networkStorage:
    table.add_row(
        [
            ns['id'],
            ns['nasType'],
            lookup(ns, 'serviceResource', 'datacenter', 'name') or '-',
            ns['username'],
            ns['capacityGb'],
            lookup(ns, 'iops') or '-' ,
            ns['serviceResourceName'],
            ns['serviceResourceBackendIpAddress'],
            lookup(ns, 'serviceResource', 'type', 'type') or '-',
            lookup(ns, 'hardware') or '-',
            lookup(ns, 'vendorName') or '-',
            lookup(ns, 'osTypeId') or '-',
        ]
    )

print(table)



