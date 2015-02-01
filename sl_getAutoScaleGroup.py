#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'takechika'

from prettytable import PrettyTable
import SoftLayer
import sluser

SL_USERNAME = sluser.SL_USERNAME
SL_API_KEY = sluser.SL_API_KEY

_maskAutoScaleGroup = '''
    virtualGuestMemberCount
    '''

client = SoftLayer.Client(username=SL_USERNAME, api_key=SL_API_KEY)
autoScaleGroups = client['Account'].getScaleGroups(mask=_maskAutoScaleGroup)

_tableHeader = [
    'id',
    'asg name',
    'dc',
    'status',
    'min',
    'max',
    'now',
    'member prefix',
    'members',
    ]

# Table definition
table = PrettyTable(_tableHeader)
table.padding_width = 1

for asg in autoScaleGroups:

    m = ""
    ms = ""
    for a in asg['virtualGuestMembers'][0:]:
#        m =  str(a['virtualGuest']['id']) + ":" + a['virtualGuest']['hostname'][-4:]
        m =  a['virtualGuest']['hostname'][-4:]
        ms = m + ' ' + ms

    table.add_row(
        [
            asg['id'],
            asg['name'],
            asg['virtualGuestMemberTemplate']['datacenter']['name'],
            asg['status']['keyName'],
            asg['minimumMemberCount'],
            asg['maximumMemberCount'],
            asg['virtualGuestMemberCount'],
            asg['virtualGuestMemberTemplate']['hostname'],
            ms,
        ]
    )

print(table)

exit()
