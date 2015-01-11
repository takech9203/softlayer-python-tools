#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'takechika'

# You can pass in your username and api_key when creating a SoftLayer client instance.
# However, you can set these in the environmental variables 'SL_USERNAME' and 'SL_API_KEY'

import sys
import SoftLayer
from datetime import tzinfo, timedelta, datetime, date
from dateutil.relativedelta import relativedelta
import sluser

SL_USERNAME = sluser.SL_USERNAME
SL_API_KEY = sluser.SL_API_KEY

client = SoftLayer.Client(username=SL_USERNAME, api_key=SL_API_KEY)


print("### Billing Items")

BillingItems = client['Account'].getAllBillingItems()
#BillingItems = client['Account'].getAllBillingItems(mask='recurringFee, description, hostName, id, lastBillDate')

# Get billing items within past 1 month
[print(k) for k in BillingItems if datetime.strptime(k['lastBillDate'][0:10],"%Y-%m-%d") > datetime.today() - relativedelta(months=1)]


#for k in BillingItems:
#    if datetime.strptime(k["lastBillDate"][0:10],"%Y-%m-%d") > datetime.today() - relativedelta(months=1) :
#        print(datetime.strptime(k["lastBillDate"][0:10] ,"%Y-%m-%d"),k["recurringFee"],k["id"], "within-1-month")
#    print(k)



print("### Billing_Invoice")

AllInvoices = client['Account'].getInvoices()
#AllInvoices = client['Account'].getInvoices(mask='id, closedDate, statusCode, startingBalance, endingBalance')

for k in AllInvoices:
    print(k)

exit()



#    BillingInfo = client['Billing_Item'].getItem(id=k["id"])
#    print(BillingInfo)


AllInvoices = client['Account'].getInvoices(mask='id')

#for i in AllInvoices:
#    print(i)
#    Billing_Invoices = client['Billing'].getObject(id=i['id'])
Billing_Invoices = client['BillingInvoice'].getObject(id=3135420)


exit()


print ("Your city is", AccountInfo['city'])
#print "Your city is", AccountInfo[1]



for i, k in enumerate(AccountInfo):
    print(i, ":", k)

## getVirtualGuest()

print()
print("### getVirtualGuests()")

vHosts = client['Account'].getVirtualGuests()   # it returns the lists of CCIs

print(vHosts[0])
print("---------------------------------")
i = 0
for i in range(len(vHosts)):
    for k,v in vHosts[i].items():
        print(k, ":",  v)
    print("---------------------------------")


## getVirtualDiskImage


print()


## getOrders()

print()
print("### getOrders()")

orders = client["Account"].getOrders()
# print order

i = 0
for i in range(len(orders)):
    for k,v in orders[i].items():
        print(k, ":",  v)


## getAllBillingItems()

print()
print("### getAllBillingItems()")

"""
billings = client["Account"].getAllBillingItems()
print("billings")

print("---------------------------------")
i = 0
for i in range(len(billings)):
    for k,v in billings[i].items():
        print(k, ":",  v)
    print("---------------------------------")
"""



