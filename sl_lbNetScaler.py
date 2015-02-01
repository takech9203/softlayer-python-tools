#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'takechika'


from prettytable import PrettyTable
import SoftLayer
import sluser

# import the necessary libraries for netscaler nitro
import json
import urllib
import httplib2
import time
from nsnitro import *

SL_USERNAME = sluser.SL_USERNAME
SL_API_KEY = sluser.SL_API_KEY

# NetScaler constant
nsAutoScaleGroup = "TK-as-group"    # SoftLayer auto scale group name
nsHost = "192.168.1.141"            # NetScaler's IP address
nsApiUser = "nsroot"                # NetScaler login user
nsApiPass = "nsroot"                # NetScaler login password
nsLBVServer = "vserver01_http"      # NetScaler Load Balancing Virtual Server
nsIpType = "public"                 # IP type used for NetScaler server ip. "public" or "private"

def getASMembers(autoScaleGroups, nsAutoScaleGroup):
    """
    Get array of dictionaries of all auto scale members of nsAutoScaleGroup

    :param autoScaleGroups: SoftLayer auto scale groups objects retrieved by getScaleGroups()
    :param nsAutoScaleGroup: SoftLayer auto scale group name which the script looks at to add/delete servers
    :return: Array of dictionaries of all auto scale members
    """
    for asg in autoScaleGroups:

        if asg['name'] == nsAutoScaleGroup:
            asMembers = []
            for a in asg['virtualGuestMembers'][0:]:
                memberId = a['virtualGuest']['id']
                asMember = {
                    "id": a['virtualGuest']['id'],
                    "name": a['virtualGuest']['hostname'],
                    "publicPrimaryIP" : client['Virtual_Guest'].getPrimaryIpAddress(id=memberId),
                    "privatePrimaryIP" : client['Virtual_Guest'].getPrimaryBackendIpAddress(id=memberId),
                }
                asMembers.append(asMember)
    return(asMembers)

def addNSServer(nsServerName, nsServerIp, nsServiceName, nsLBVServer):
    """
    Add SoftLayer virtual servers to NetScaler servers,
    create new services and bind the services to LB virtual server.
    Must be logged in to NetScaler with API beforehand.

    :param nsServerName: The name of NetScaler server to be created.
    :param nsServerIp: The IP address of NetScaler server to be created.
    :param nsServiceName: The name of NetScaler service to be created.
    :param nsLBVServer: The name of NetScaler LB virtual server to be binded with the service.
    :return:
    """

    # add server test
    addserver = NSServer()
    addserver.set_name(nsServerName)
    addserver.set_ipaddress(nsServerIp)
    NSServer.add(nitro, addserver)

    # get state
    server = NSServer()
    server.set_name(nsServerName)
    server = server.get(nitro, server)
    # print(server.get_name() + ": " + server.get_state())

    # add service
    addservice = NSService()
    addservice.set_name(nsServiceName)
    addservice.set_servername(nsServerName)
    addservice.set_servicetype("HTTP")
    addservice.set_port(80)
    NSService.add(nitro, addservice)

    # bind service to lbvserver
    lbbinding = NSLBVServerServiceBinding()
    lbbinding.set_name(nsLBVServer)
    lbbinding.set_servicename(nsServiceName)
    lbbinding.set_weight(40)
    NSLBVServerServiceBinding.add(nitro, lbbinding)

    # get binding info
    lbbinding = NSLBVServerServiceBinding()
    lbbinding.set_name(nsLBVServer)
    lbbindings = NSLBVServerServiceBinding.get(nitro, lbbinding)
#    for lbb in lbbindings:
#        print("sgn: " + lbb.get_servicegroupname())
    return

def delNSServer(nsServerName):
    """
    Delete NetScaler server.
    Must be logged in to NetScaler with API beforehand.

    :param nsServerName: The name of NetScaler server to be deleted.
    :return:
    """

    # delete server
    delserver = NSServer()
    delserver.set_name(nsServerName)
    NSServer.delete(nitro, delserver)
    # print("Server deleted.")

    """
    try:
        server = NSServer()
        server.set_name(nsServerName)
        server = server.get(nitro, server)
        print server.get_name() + ": " + server.get_state()
    except NSNitroError, e:
        print e.message
    """
    return

def getNsServersList(nitro):
    """
    Get the list of NetScaler servers

    :param nitro: nitro connection
    :return: Array of NetScaler servers
    """
    nsServers = []
    server = NSServer()
    for n in NSServer.get_all(nitro):
        nsServers.append(n.get_name())
    return nsServers


# Connect to SoftLayer API
client = SoftLayer.Client(username=SL_USERNAME, api_key=SL_API_KEY)
autoScaleGroups = client['Account'].getScaleGroups()
asMembers = getASMembers(autoScaleGroups, nsAutoScaleGroup)

# get auto scale hostname prefix
for asg in autoScaleGroups:
    if asg['name'] == nsAutoScaleGroup:
        nsAutoScalePrefix = asg['virtualGuestMemberTemplate']['hostname']
        break

# Login to NetScaler with API
nitro = NSNitro(nsHost, nsApiUser, nsApiPass)
nitro.login()

# Get the list of NetScaler servers
nsServers = getNsServersList(nitro)

# If an auto scale member is not in NetScaler severs,
# add the member to NetScaler server
asMemberNames = []
addedServers = []
for asm in asMembers:
    # NetScaler parameters
    nsServerName = asm['name']
    nsPublicPrimaryIp = asm['publicPrimaryIP']
    nsPrivatePrimaryIp = asm['privatePrimaryIP']
    if nsIpType == "public":
        nsServerIp = nsPublicPrimaryIp
    else:
        nsServerIp = nsPrivatePrimaryIp
    nsServiceName = "service_http_" + nsServerIp.split(".")[-1]   # NetScaler Service Name for the server. "service_http_<IP's 4th octet>"

    if not asm['name'] in nsServers:
        addNSServer(nsServerName, nsServerIp, nsServiceName, nsLBVServer)
        addedServers.append(asm['name'])
        # print("Server \"%s\" created." % asm['name'])

    # make array of asm['name']
    asMemberNames.append(asm['name'])


# If a NetScaler server with nsAutoPrefix prefix exists while not in auto scale member,
# delete the server from NetScaler servers
deletedServers = []
for nss in nsServers:
#    print(nss, nss[:-5], nsAutoScalePrefix)
    if nss[:-5] == nsAutoScalePrefix:
        if not nss in asMemberNames:
            delNSServer(nss)
            deletedServers.append(nss)
            # print("Server \"%s\" deleted." % nss)

# Logout from NetScaler
nitro.logout()

# Print results
if len(addedServers) == 0:
    print("No servers created.")
else:
    print("Created: %s" % addedServers)

if len(deletedServers) == 0:
    print("No servers deleted.")
else:
    print("Deleted: %s" % deletedServers)

exit()