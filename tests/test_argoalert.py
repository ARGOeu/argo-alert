import json
from argoalert import argoalert

# Test the transformation of argo endpoint group status event to alerta alert representation
def test_endpoint_group_event():
    argo_str='{"status":"ok","group":"SITEA","metric":"httpd.memory","service":"httpd","hostname":"webserver01","summary":"foo","type":"endpoint_group"}'
    exp_str = '{"resource": "SITEA", "severity": "ok", "service": ["endpoint_group"], "text": "foo", "environment": "devel", "event": "status"}'
    argo_json = json.loads(argo_str)
    alerta_json = argoalert.transform(argo_json,"devel")
    alerta_str = json.dumps(alerta_json)
    assert(alerta_str == exp_str)

# Test the transformation of argo service status event to alerta alert representation
def test_service_event():
    argo_str='{"status":"ok","group":"SITEA","metric":"httpd.memory","service":"httpd","hostname":"webserver01","summary":"foo","type":"service"}'
    exp_str = '{"resource": "SITEA/httpd", "severity": "ok", "service": ["service"], "text": "foo", "environment": "devel", "event": "status"}'
    argo_json = json.loads(argo_str)
    alerta_json = argoalert.transform(argo_json,"devel")
    alerta_str = json.dumps(alerta_json)
    assert(alerta_str == exp_str)

# Test the transformation of argo endpoint status event to alerta alert representation
def test_endpoint_event():
    argo_str='{"status":"ok","group":"SITEA","metric":"httpd.memory","service":"httpd","hostname":"webserver01","summary":"foo","type":"endpoint"}'
    exp_str = '{"resource": "SITEA/httpd/webserver01", "severity": "ok", "service": ["endpoint"], "text": "foo", "environment": "devel", "event": "status"}'
    argo_json = json.loads(argo_str)
    alerta_json = argoalert.transform(argo_json,"devel")
    alerta_str = json.dumps(alerta_json)
    assert(alerta_str == exp_str)

# Test the transformation of argo metric status event to alerta alert representation
def test_endpoint_metric_event():
    argo_str='{"status":"ok","group":"SITEA","metric":"httpd.memory","service":"httpd","hostname":"webserver01","summary":"foo","type":"metric"}'
    exp_str = '{"resource": "SITEA/httpd/webserver01/httpd.memory", "severity": "ok", "service": ["metric"], "text": "foo", "environment": "devel", "event": "status"}'
    argo_json = json.loads(argo_str)
    alerta_json = argoalert.transform(argo_json,"devel")
    alerta_str = json.dumps(alerta_json)
    assert(alerta_str == exp_str)


