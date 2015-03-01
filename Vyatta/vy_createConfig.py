#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'takechika'

import SoftLayer
import Vyatta
import vyuser


GRE_MY_ADDR = "192.168.10.1"
GRE_PEER_ADDR = "192.168.10.2"
IPSEC_MY_ADDR = ""
IPSEC_PEER_ADDR = ""
STATIC_ROUTE_DST = "192.168.1.0/24"
STATIC_ROUTE_GW = GRE_PEER_ADDR
IPSEC_INTERFACE = 'bond1'          # bond0 for private, bond1 for public

urlBase = 'https://161.202.96.5/'
user = vyuser.VYUSER
passwd = vyuser.VYPASSWD

vy = Vyatta.Vyatta(urlBase, user, passwd)


#vy.createEncodedUrl(vy.getConfId(), 'aa')
#vy.editConfigConf('vy_configuration.conf')

vy.editConfig('vy_setup_template.txt')


print(vy.getConfId())
#print(vy.urlOpBase)
#print(vy.deleteConfId(vy.getConfId()))

#    vy.commandOp('vy_op_command.conf')
#print(vy.editConfigConf('vy_configuration.conf'))

exit()

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




