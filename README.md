SoftLayer API Python Client tools
=================================

Miscellaneous tools developed using SoftLayer Python API.

- **sl_getAutoScaleGroup.py** - shows the list of SoftLayer auto scale groups.
- **sl_getInstances.py** - shows the list of SoftLayer VSIs and bare metal servers and their attributes.
- **sl_getInventory.py** - shows the list of SoftLayer VSIs and bare metal servers.
- **sl_getLocation** - shows the list of VSIs and hosts they are running on.
- **sl_getNetworkStorage.py** - shows the list of SoftLayer network storage including iSCSI, CPS, NAS, Object Storage and EVault.
- **sl_getUsers** - shows the list of SoftLayer users.
- **NetScaler/sl_lbNetScaler.py** - integrates SoftLayer auto scale and NetScaler load balancing.


System Requirements
-------------------

- [SoftLayer Python API 3.3.1] (https://pypi.python.org/pypi/SoftLayer)
- [nsnitro 1.0.3] (https://pypi.python.org/pypi/nsnitro) for NetScaler/sl_lbNetScaler.py


Installation
------------

- Simply copy and paste the scripts to a directory you like
- Create the file "sluser.py" in the same directory with the scripts and put SoftLayer username and API key.

```
SL_USERNAME = "SoftLayer_username"
SL_API_KEY = "SoftLayer_API_Key"
```


Usage
-----

```
python <script file>
```

Example

```
python sl_getAutoScaleGroup.py
```


License 
-------
Copyright &copy; 2015 takechika
Distributed under the [MIT License][mit].

[MIT]: http://www.opensource.org/licenses/mit-license.php

Have fun !
