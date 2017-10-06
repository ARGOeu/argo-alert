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

# Test gocdb xml to contacts json transformation
def test_gocdb_to_contacts():

    xmlfn = "./tests/files/gocdb-foo.xml"
    jsonfn = "./tests/files/contacts.json"


    with open(jsonfn,'r') as jsonfile:
        jsondata = jsonfile.read().replace('\n', '')
        expJson = json.loads(jsondata)

        with open(xmlfn, 'r') as xmlfile:
            xmldata = xmlfile.read().replace('\n', '')
            contacts = argoalert.gocdb_to_contacts(xmldata)
            assert (contacts == expJson)

# Test contacts to alerta transformation
def test_contacts_to_alerta():

    cfn = "./tests/files/contacts.json"
    rfn = "./tests/files/rules.json"


    with open(rfn,'r') as ruleJson:
        ruleData = ruleJson.read().replace('\n', '')
        expJson = json.loads(ruleData)

        with open(cfn, 'r') as contactJson:
            contactData = contactJson.read().replace('\n', '')
            contacts = json.loads(contactData)
            rules = argoalert.contacts_to_alerta(contacts)
            rulesOut = json.dumps(rules,sort_keys=True)
            expOut = json.dumps(expJson,sort_keys=True)
            assert(rulesOut == expOut)


