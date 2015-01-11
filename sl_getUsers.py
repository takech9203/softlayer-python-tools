#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'takechika'

import sys
from prettytable import PrettyTable
import SoftLayer
import sluser

SL_USERNAME = sluser.SL_USERNAME
SL_API_KEY = sluser.SL_API_KEY

_userMask = '''
    id,
    accountId,
    parentId,
    firstName,
    lastName,
    email
    '''
_userTableHeader = [
    'ParentID',
    'ParentName',
    'UserID',
    'UserName',
    'EMail'
    ]

def getChildren(parent, users):
    """Get children of the parent from the user list / このユーザーが親となる子ユーザーをリストから取得する.

    parent: 親ユーザーのオブジェクト (User_Customer)
    users: 検索対象の子ユーザーのリスト (an array of User_Customer)
    """

    a = {}
    b = []

    for u in users:
        if u.get('parentId') == parent.get('id'):
            a = {
                "ParentID": u.get('parentId'),
                "ParentName": parent.get('lastName') + " " + parent.get('firstName'),
                "ChildID": u.get('id'),
                "ChildName": u.get('lastName') + " " + u.get('firstName'),
                "Email": u.get('email')
            }
            b.append(a)

    return(b)

client = SoftLayer.Client(username=SL_USERNAME, api_key=SL_API_KEY)
users = client['Account'].getUsers(mask=_userMask)


# Find the master user id
for u in users:
    if u.get('parentId') == '':
        masterUser = u
        print("Master user is \"%s %s\" (id: %s)" % (masterUser.get('lastName'), masterUser.get('firstName'), masterUser.get('id')))

# Table definition
table = PrettyTable(_userTableHeader)
table.padding_width = 1

# Get user list
count = 0
for parent in users:
#    print(getChildren(u, users))
    userList = getChildren(parent, users)
    for x in userList[0:]:
#        print(x)
        table.add_row(
            [
                x['ParentID'],
                x['ParentName'],
                x['ChildID'],
                x['ChildName'],
                x['Email']
            ]
        )
        count = count + 1

print(table)
print(count, "users")

exit()

