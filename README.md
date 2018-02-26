argo-alert
===============================

version number: 0.0.1
author: GRNET

Overview
--------

Streaming Publisher of argo-streaming status events as alerts to an alerta service endpoint.
Alerta mail configuration rules from gocdb contact data.

Argo streaming-service produces status events with the following schema:
```
json
{
  "endpoint_group":"SITE-A"
  "service":"SERVICE-A",
  "hostname":"host-A.site-A.foo"
  "metric":"metric-A"
  "status":"warning"
  "summary":"a warning message"
  "type":"metric"
}
```

There are four types of status events: `[ "endpoint_group", "service", "endpoint", "metric"]`

Argo-alert connects to a kafka-topic and receives such status events. Each event is
then transformed to a compatible alerta schema and gets published to an alerta service endpoint.

Alerta-mailer rule generation
---------------------------
Argo-alert provides the ability to create alerta-mailer rules from gocdb contact data. Argo-alert
connects to a defined gocdb api endpoint and transforms the xml contact information to alerta-mailer
rule json format. The rules are saved to a defined output file. The parameter `use_notifications_flag`
(by default set to `True`) is used to select only the gocdb contacts that contain
`<NOTIFICATIONS>Y</NOTIFICATIONS>` xml element. If the gocdb instance doesn't support notifications flag
please set `use_notifications_flag=False`. 

The configuration file for argo-alert provides a `[gocdb]` section to configure the gocdb endpoint
and the required certificate parameters for access. The `mail-rules` parameter in `[alerta]` section
specifies the alerta-mailer rule filename for output.  


Installation / Usage
--------------------

To install use pip:

    $ pip install argoalert


Or clone the repo:

    $ git clone https://github.com/ARGOeu/argoalert.git
    $ python setup.py install


argoalert requires a configuration file with the following options:
```
[gocdb]
# Path to godcb endpoint
api=https://gocdb-url.example.foo
# Path to ca bundle folder
cabundle=/path/to/cabundle
# Path to host certificate file
hostcert=/path/to/hostcert
# Path to host key file
hostkey=/path/to/hostkey
# Verify https requests
verify=False
# Examine notification flag when selecting contacts
use_notifications_flag=True
# request path for gocdb to retrieve top-level items
top_request=/gocdbpi/public/?method=get_site
# request path for gocdb to retrieve sub-level items
sub_request=/gocdbpi/public/?method=get_service

[kafka]
# kafka endpoint
endpoint=localhost:9092
# kafka topic
topic=metrics

[alerta]
# alerta service endpoint
endpoint=http://localhost:8080
# alerta enviroment
environment=devel
# alerta token
token=s3cr3tt0ke3n
# path to store the generated mail rules
mail-rules=/home/root/alerta-rules-101

[logging]
# loggin level
level = INFO

```

To run argo-alert publisher:

    $ argo-alert-publisher -c /path/to/argo-alert.conf

To run argo-alert mail rule generator:

    $ argo-alert-rulegen -c /path/to/argo-alert.conf

Run tests
---------

To run argo-alert tests:

    $ pytest
