#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'takechika'

import SoftLayer
import sluser

SL_USERNAME = sluser.SL_USERNAME
SL_API_KEY = sluser.SL_API_KEY

_mask = '''
    id,
    fullyQualifiedDomainName,
    location.pathString'''

client = SoftLayer.Client(username=SL_USERNAME, api_key=SL_API_KEY)
virtualGuests = client['Account'].getVirtualGuests(mask=_mask)
for vg in virtualGuests:
    print(vg['id'],
          vg['fullyQualifiedDomainName'],
          vg['location']['pathString'] )
exit()
