argo-ams
===============================

version number: 0.0.1
author: GRNET

Description
-----------

Alera plugin for publishing alerts to AMS service


Installation
------------

In an alerta enviroment:
 
- Clone the repo and run `python setup.py install`
 
 *-- or --*
 
- Use pip and issue `pip install git+https://github.com/ARGOeu/argo-alert#subdirectory=argoams`
 
 
Configuration
-------------
 
In /etc/alertad.conf add the following *required* options
 
 ```
PLUGINS = ['ams'] 
AMS_HOST='ams-host'
AMS_TOPIC='alerta'
AMS_TOKEN='s3cr3t'
AMS_PROJECT=''
```

Note: if `AMS_PROJECT=''` (empty) the plugin will automatically use the alert's environment value as an ams destination project

Execution
---------
Restart alerta service (or webserver that hosts alerta service)



