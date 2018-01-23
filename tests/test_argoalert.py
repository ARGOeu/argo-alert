import json
import unittest
from argoalert import argoalert


class TestArgoAlertMethods(unittest.TestCase):

    # Test the transformation of argo endpoint group status event to alerta alert representation
    def test_endpoint_group_event(self):
        argo_str='{"status":"OK","endpoint_group":"SITEA","metric":"httpd.memory","service":"httpd","hostname":"webserver01","summary":"foo","type":"endpoint_group"}'
        exp_str = '{"environment": "devel", "event": "status", "resource": "SITEA", "service": ["endpoint_group"], "severity": "ok"}'
        argo_json = json.loads(argo_str)
        alerta_json = argoalert.transform(argo_json,"devel")
        alerta_str = json.dumps(alerta_json, sort_keys=True)

        self.assertEqual(alerta_str, exp_str)

    # Test the transformation of argo service status event to alerta alert representation
    def test_service_event(self):
        argo_str='{"status":"OK","endpoint_group":"SITEA","metric":"httpd.memory","service":"httpd","hostname":"webserver01","summary":"foo","type":"service"}'
        exp_str = '{"environment": "devel", "event": "status", "resource": "SITEA/httpd", "service": ["service"], "severity": "ok"}'
        argo_json = json.loads(argo_str)
        alerta_json = argoalert.transform(argo_json, "devel")
        alerta_str = json.dumps(alerta_json, sort_keys=True)

        self.assertEqual(alerta_str, exp_str)

    # Test the transformation of argo endpoint status event to alerta alert representation
    def test_endpoint_event(self):
        argo_str='{"status":"OK","endpoint_group":"SITEA","metric":"httpd.memory","service":"httpd","hostname":"webserver01","summary":"foo","type":"endpoint"}'
        exp_str = '{"environment": "devel", "event": "status", "resource": "SITEA/httpd/webserver01", "service": ["endpoint"], "severity": "ok"}'
        argo_json = json.loads(argo_str)
        alerta_json = argoalert.transform(argo_json, "devel")
        alerta_str = json.dumps(alerta_json, sort_keys=True)

        self.assertEqual(alerta_str, exp_str)

    # Test the transformation of argo metric status event to alerta alert representation
    def test_endpoint_metric_event(self):
        argo_str = '{"status":"OK","endpoint_group":"SITEA","metric":"httpd.memory","service":"httpd","hostname":"webserver01","summary":"foo","type":"metric"}'
        exp_str = '{"environment": "devel", "event": "status", "resource": "SITEA/httpd/webserver01/httpd.memory", "service": ["metric"], "severity": "ok"}'
        argo_json = json.loads(argo_str)
        alerta_json = argoalert.transform(argo_json, "devel")
        alerta_str = json.dumps(alerta_json, sort_keys=True)

        self.assertEqual(alerta_str, exp_str)

    # Test gocdb xml to contacts json transformation
    def test_gocdb_to_contacts(self):

        xml_fn = "./tests/files/gocdb-foo.xml"
        json_fn = "./tests/files/contacts.json"

        with open(json_fn,'r') as json_file:
            json_data = json_file.read().replace('\n', '')
            exp_json = json.loads(json_data)

            with open(xml_fn, 'r') as xml_file:
                xml_data = xml_file.read().replace('\n', '')
                contacts = argoalert.gocdb_to_contacts(xml_data)
                print contacts
                self.assertEqual(contacts, exp_json)

    # Test contacts to alerta transformation
    def test_contacts_to_alerta(self):

        cfn = "./tests/files/contacts.json"
        rfn = "./tests/files/rules.json"

        with open(rfn, 'r') as ruleJson:
            rule_data = ruleJson.read().replace('\n', '')
            exp_json = json.loads(rule_data)

            with open(cfn, 'r') as contactJson:
                contact_data = contactJson.read().replace('\n', '')
                contacts = json.loads(contact_data)
                rules = argoalert.contacts_to_alerta(contacts)
                rules_out = json.dumps(rules, sort_keys=True)
                exp_out = json.dumps(exp_json, sort_keys=True)
                self.assertEqual(rules_out, exp_out)


