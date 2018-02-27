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

    # Test service group gocdb xml to contacts json transformation
    def test_sg_gocdb_to_contacts_notify_flag(self):
        xml_fn = "./tests/files/sg_gocdb.xml"
        notify_json_fn = "./tests/files/sg_contacts_notify.json"
        all_json_fn = "./tests/files/sg_contacts_all.json"

        with open(xml_fn, 'r') as xml_file:
            xml_data = xml_file.read().replace('\n', '')

            # Select contacts using notification flag on
            with open(notify_json_fn, 'r') as json_file:
                json_data = json_file.read().replace('\n', '')
                exp_json = json.loads(json_data)

                use_notif_flag = True
                contacts = argoalert.gocdb_to_contacts(xml_data, use_notif_flag)

                self.assertEqual(contacts, exp_json)

            # Select all contacts
            with open(all_json_fn, 'r') as json_file:
                json_data = json_file.read().replace('\n', '')
                exp_json = json.loads(json_data)

                use_notif_flag = False
                contacts = argoalert.gocdb_to_contacts(xml_data, use_notif_flag)

                self.assertEqual(contacts, exp_json)

    # Test gocdb xml to contacts json transformation
    def test_site_gocdb_to_contacts_notify_flag(self):

        xml_fn = "./tests/files/site_gocdb.xml"
        notify_json_fn = "./tests/files/site_contacts_notify.json"
        all_json_fn = "./tests/files/site_contacts_all.json"

        with open(xml_fn, 'r') as xml_file:
            xml_data = xml_file.read().replace('\n', '')

            # Select contacts using notification flag on
            with open(notify_json_fn, 'r') as json_file:
                json_data = json_file.read().replace('\n', '')
                exp_json = json.loads(json_data)

                use_notif_flag = True
                contacts = argoalert.gocdb_to_contacts(xml_data, use_notif_flag)

                self.assertEqual(contacts, exp_json)

            # Select all contacts
            with open(all_json_fn, 'r') as json_file:
                json_data = json_file.read().replace('\n', '')
                exp_json = json.loads(json_data)

                use_notif_flag = False
                contacts = argoalert.gocdb_to_contacts(xml_data, use_notif_flag)

                self.assertEqual(contacts, exp_json)

    # Test servicegroup contacts to alerta transformation
    def test_sg_contacts_to_alerta(self):

        cfn = "./tests/files/sg_contacts_notify.json"
        rfn = "./tests/files/sg_rules.json"

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

     # Test site contacts to alerta transformation
    def test_site_contacts_to_alerta(self):
        cfn = "./tests/files/site_contacts_notify.json"
        rfn = "./tests/files/site_rules.json"

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


