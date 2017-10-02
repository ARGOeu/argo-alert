argo-alert
===============================

version number: 0.0.1
author: GRNET

Overview
--------

Publisher of argo-streaming status events as alerts to an alerta service endpoint.

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


Installation / Usage
--------------------

To install use pip:

    $ pip install argoalert


Or clone the repo:

    $ git clone https://github.com/ARGOeu/argoalert.git
    $ python setup.py install


argoalert requires a configuration file with the following options:
```
[kafka]
endpoint=localhost:9092
topic=metrics

[alerta]
endpoint=http://localhost:8080
environment=devel
token=s3cr3tt0ke3n

[logging]
level = INFO

```

To run argo-alert:

    $ argo-alert -c /path/to/argo-alert.conf

Run tests
---------

To run argo-alert tests:

    $ pytest

