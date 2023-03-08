import json
import unittest
from argoalert import argoalert
import os




# establish path for the resource
def get_resource_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)

class TestArgoAlertMethods(unittest.TestCase):



    # Test the transformation of argo endpoint group status event to alerta alert representation
    def test_endpoint_group_event(self):
        argo_str='{"status":"OK","endpoint_group":"SITEA","metric":"httpd.memory","service":"httpd",' \
                 '"hostname":"webserver01","summary":"foo","type":"endpoint_group", "repeat": "false", ' \
                 '"ts_monitored":"2018-04-24T13:35:33Z", "ts_processed":"", "message":"", "summary":""} '
        exp_str = '{"attributes": {"_alert_url": "https://ui.argo.foo/devel/report-status/Critical/PROJECTS/SITEA?start=2018-04-21&end=2018-04-24", '\
                  '"_endpoint": "webserver01", "_group": "SITEA", "_group_endpoints": "", "_group_services": "", "_group_statuses": "", "_group_type": "Project", "_metric": "httpd.memory", ' \
                  '"_metric_names": "", "_metric_statuses": "", "_mon_message": "", "_mon_summary": "", ' \
                  '"_repeat": "false", "_service": "httpd", "_status_egroup": "", "_status_endpoint": "", "_status_metric": "", "_status_service": "", "_ts_monitored": "2018-04-24T13:35:33Z", "_ts_processed": ""}, "environment": ' \
                  '"devel", "event": "endpoint_group_status", "resource": "SITEA", "service": ["endpoint_group"], ' \
                  '"severity": "ok", "text": "[ DEVEL ] - Project SITEA is OK", "timeout": 20}'

        argo_json = json.loads(argo_str)
        alerta_json = argoalert.transform(argo_json, "devel", "Project", 20,"ui.argo.foo", "Critical")
        alerta_str = json.dumps(alerta_json, sort_keys=True)


        self.assertEqual(alerta_str, exp_str)

    # Test the transformation of argo service status event to alerta alert representation
    def test_service_event(self):
        argo_str = '{"status":"OK","endpoint_group":"SITEA","metric":"httpd.memory","service":"httpd",' \
                   '"hostname":"webserver01","summary":"foo","type":"service", "repeat": "false", "ts_monitored":"2018-04-24T13:35:33Z", ' \
                   '"ts_processed":"", "message":"", "summary":""} '
        exp_str = '{"attributes": {' \
                   '"_endpoint": "webserver01", "_group": "SITEA", "_group_endpoints": "", "_group_services": "", "_group_statuses": "", "_group_type": "", "_metric": "httpd.memory", ' \
                   '"_metric_names": "", "_metric_statuses": "", "_mon_message": "", "_mon_summary": "", "_repeat": "false", ' \
                   '"_service": "httpd", "_status_egroup": "", "_status_endpoint": "", "_status_metric": "", "_status_service": "", "_ts_monitored": "2018-04-24T13:35:33Z", "_ts_processed": ""}, ' \
                   '"environment": "devel", "event": "service_status", "resource": "SITEA/httpd", "service": ["service"], ' \
                   '"severity": "ok", "text": "[ DEVEL ] - Service httpd is OK", "timeout": 32}'

        argo_json = json.loads(argo_str)
        alerta_json = argoalert.transform(argo_json, "devel", "", 32, "ui.argo.foo", "Critical")
        alerta_str = json.dumps(alerta_json, sort_keys=True)

        self.assertEqual(alerta_str, exp_str)

    # # Test the transformation of argo endpoint status event to alerta alert representation
    def test_endpoint_event(self):
        argo_str='{"status":"OK", "endpoint_group":"SITEA","metric":"httpd.memory","service":"httpd",' \
                 '"hostname":"webserver01","summary":"foo","type":"endpoint", "repeat": "false", "ts_monitored":"2018-04-24T13:35:33Z", ' \
                 '"ts_processed":"", "message":"", "summary":""} '
        exp_str = '{"attributes": {"_alert_url": "http://ui.argo.foo/devel/report-status/Critical/SITES/SITEA/httpd/webserver01?start=2018-04-21&end=2018-04-24", '\
                  '"_endpoint": "webserver01", "_group": "SITEA", "_group_endpoints": "", "_group_services": "", "_group_statuses": "", "_group_type": "Site", "_metric": "httpd.memory", ' \
                  '"_metric_names": "", "_metric_statuses": "", "_mon_message": "", "_mon_summary": "", ' \
                  '"_repeat": "false", "_service": "httpd", "_status_egroup": "", "_status_endpoint": "", "_status_metric": "", "_status_service": "", "_ts_monitored": "2018-04-24T13:35:33Z", "_ts_processed": ""}, "environment": ' \
                  '"devel", "event": "endpoint_status", "resource": "httpd/webserver01", "service": [' \
                  '"endpoint"], "severity": "ok", "text": "[ DEVEL ] - Endpoint webserver01/httpd is OK", "timeout": ' \
                  '122}'

        argo_json = json.loads(argo_str)
        alerta_json = argoalert.transform(argo_json, "devel", "Site", 122,"ui.argo.foo","Critical")
        alerta_str = json.dumps(alerta_json, sort_keys=True)

        self.assertEqual(alerta_str, exp_str)

    # # Test the transformation of argo metric status event to alerta alert representation
    def test_endpoint_metric_event(self):
        argo_str = '{"status":"OK","endpoint_group":"SITEA","metric":"httpd.memory","service":"httpd","hostname":"webserver01","summary":"foo","type":"metric", "repeat": "false", "ts_monitored":"2018-04-24T13:35:33Z", "ts_processed":"", "message":"", "summary":""}'
        exp_str = '{"attributes": {' \
                  '"_endpoint": "webserver01", "_group": "SITEA", "_group_endpoints": "", "_group_services": "", "_group_statuses": "", "_group_type": "", "_metric": "httpd.memory", ' \
                  '"_metric_names": "", "_metric_statuses": "", "_mon_message": "", "_mon_summary": "", ' \
                  '"_repeat": "false", "_service": "httpd", "_status_egroup": "", "_status_endpoint": "", "_status_metric": "", "_status_service": "", "_ts_monitored": "2018-04-24T13:35:33Z", "_ts_processed": ""}, "environment": ' \
                  '"devel", "event": "metric_status", "resource": "SITEA/httpd/webserver01/httpd.memory", "service": [' \
                  '"metric"], "severity": "ok", "text": "[ DEVEL ] - Metric httpd.memory@(webserver01:httpd) is OK", ' \
                  '"timeout": 42}'

        argo_json = json.loads(argo_str)
        alerta_json = argoalert.transform(argo_json, "devel", "", 42,"ui.argo.foo","Critical")
        alerta_str = json.dumps(alerta_json, sort_keys=True)

        self.assertEqual(alerta_str, exp_str)

    # Test service group gocdb xml to contacts json transformation
    def test_sg_gocdb_to_contacts_notify_flag(self):
        xml_fn = get_resource_path("./files/sg_gocdb.xml")
        notify_json_fn = get_resource_path("./files/sg_contacts_notify.json")
        all_json_fn = get_resource_path("./files/sg_contacts_all.json")

        with open(xml_fn, 'r') as xml_file:
            xml_data = xml_file.read().replace('\n', '')

            # Select contacts using notification flag on
            with open(notify_json_fn, 'r') as json_file:
                json_data = json_file.read().replace('\n', '')
                exp_json = json.loads(json_data)

                use_notif_flag = True
                contacts = argoalert.gocdb_to_contacts(xml_data, use_notif_flag, None)
                self.assertEqual(contacts, exp_json)

            # Select all contacts
            with open(all_json_fn, 'r') as json_file:
                json_data = json_file.read().replace('\n', '')
                exp_json = json.loads(json_data)

                use_notif_flag = False
                contacts = argoalert.gocdb_to_contacts(xml_data, use_notif_flag, None)

                self.assertEqual(contacts, exp_json)


     # Test gocdb xml to contacts json transformation
    def test_json_feed_to_contacts_notify_flag(self):

        json_fn = get_resource_path("./files/sg_feed.json")
        notify_json_fn = get_resource_path("./files/sg_feed_contacts.json")
        all_json_fn = get_resource_path("./files/sg_feed_contacts_all.json")

        with open(json_fn, 'r') as json_file:
            json_og_data = json.load(json_file)
            
            
            # Select contacts using notification flag on
            with open(notify_json_fn, 'r') as json_file:
                json_data = json_file.read().replace('\n', '')
                exp_json = json.loads(json_data)

                use_notif_flag = True
                contacts = argoalert.json_feed_to_contacts(json.dumps(json_og_data), use_notif_flag, None, "SERVICE_GROUP")

                self.assertEqual(contacts, exp_json)

            # Select all contacts
            with open(all_json_fn, 'r') as json_file:
                json_data = json_file.read().replace('\n', '')
                exp_json = json.loads(json_data)

                use_notif_flag = False
                contacts = argoalert.json_feed_to_contacts(json.dumps(json_og_data), use_notif_flag, None, "SERVICE_GROUP")

                self.assertEqual(contacts, exp_json)


    # Test gocdb xml to contacts json transformation
    def test_site_gocdb_to_contacts_notify_flag(self):

        xml_fn = get_resource_path("./files/site_gocdb.xml")
        notify_json_fn = get_resource_path("./files/site_contacts_notify.json")
        all_json_fn = get_resource_path("./files/site_contacts_all.json")

        with open(xml_fn, 'r') as xml_file:
            xml_data = xml_file.read().replace('\n', '')

            # Select contacts using notification flag on
            with open(notify_json_fn, 'r') as json_file:
                json_data = json_file.read().replace('\n', '')
                exp_json = json.loads(json_data)

                use_notif_flag = True
                contacts = argoalert.gocdb_to_contacts(xml_data, use_notif_flag, None)

                self.assertEqual(contacts, exp_json)

            # Select all contacts
            with open(all_json_fn, 'r') as json_file:
                json_data = json_file.read().replace('\n', '')
                exp_json = json.loads(json_data)

                use_notif_flag = False
                contacts = argoalert.gocdb_to_contacts(xml_data, use_notif_flag, None)

                self.assertEqual(contacts, exp_json)

    # Test api contacts to alerta transformation
    def test_api_contacts_to_alerta(self):

        apifn = get_resource_path("./files/api_contacts.json")
        rfn = get_resource_path("./files/api_rules.json")

        with open(rfn, 'r') as rule_json:
            rule_data = rule_json.read().replace('\n', '')
            exp_json = json.loads(rule_data)

            with open(apifn, 'r') as contact_json:
                contact_data = contact_json.read().replace('\n', '')
                contacts = json.loads(contact_data)
                rules = argoalert.contacts_to_alerta(contacts, [])
                rules_out = json.dumps(rules, sort_keys=True)
                exp_out = json.dumps(exp_json, sort_keys=True)
                print(json.dumps(rules,indent=4))
                self.assertEqual(rules_out, exp_out)


    # Test servicegroup contacts to alerta transformation
    def test_sg_contacts_to_alerta(self):

        cfn = get_resource_path("./files/sg_contacts_notify.json")
        rfn = get_resource_path("./files/sg_rules.json")

        with open(rfn, 'r') as ruleJson:
            rule_data = ruleJson.read().replace('\n', '')
            exp_json = json.loads(rule_data)

            with open(cfn, 'r') as contactJson:
                contact_data = contactJson.read().replace('\n', '')
                contacts = json.loads(contact_data)
                rules = argoalert.contacts_to_alerta(contacts, [])
                rules_out = json.dumps(rules, sort_keys=True)
                exp_out = json.dumps(exp_json, sort_keys=True)
                self.assertEqual(rules_out, exp_out)
               
    # Test site contacts to alerta transformation
    def test_site_contacts_to_alerta(self):
        cfn = get_resource_path("./files/site_contacts_notify.json")
        rfn = get_resource_path("./files/site_rules.json")

        with open(rfn, 'r') as ruleJson:
            rule_data = ruleJson.read().replace('\n', '')
            exp_json = json.loads(rule_data)

            with open(cfn, 'r') as contactJson:
                contact_data = contactJson.read().replace('\n', '')
                contacts = json.loads(contact_data)
                rules = argoalert.contacts_to_alerta(contacts, [])
                rules_out = json.dumps(rules, sort_keys=True)
                exp_out = json.dumps(exp_json, sort_keys=True)
                self.assertEqual(rules_out, exp_out)

    # Test gocdb xml with test emails to final rules
    def test_site_gocdb_test_mails(self):
        xml_fn = get_resource_path("./files/site_gocdb.xml")
        site_rules_fn = get_resource_path("./files/site_rules_test_emails.json")

        with open(xml_fn, 'r') as xml_file:
            xml_data = xml_file.read().replace('\n', '')

            # Select contacts using notification flag on
            with open(site_rules_fn, 'r') as json_file:
                json_data = json_file.read().replace('\n', '')
                exp_json = json.loads(json_data)

                use_notif_flag = True
                test_emails = ["test1@email.foo", "test2@email.foo", "test3@email.foo"]
                contacts = argoalert.gocdb_to_contacts(xml_data, use_notif_flag, test_emails)

                rules = argoalert.contacts_to_alerta(contacts, [])

                self.assertEqual(exp_json, rules)

    # Test gocdb xml with test emails to final rules
    def test_sg_gocdb_test_mails(self):
        xml_fn = get_resource_path("./files/sg_gocdb.xml")
        site_rules_fn = get_resource_path("./files/sg_rules_test_emails.json")

        with open(xml_fn, 'r') as xml_file:
            xml_data = xml_file.read().replace('\n', '')

            # Select contacts using notification flag on
            with open(site_rules_fn, 'r') as json_file:
                json_data = json_file.read().replace('\n', '')
                exp_json = json.loads(json_data)

                use_notif_flag = True
                test_emails = ["test1@email.foo", "test2@email.foo"]
                contacts = argoalert.gocdb_to_contacts(xml_data, use_notif_flag, test_emails)

                rules = argoalert.contacts_to_alerta(contacts, [])

                self.assertEqual(exp_json, rules)

    # Test gocdb xml with test emails and extra emails to final rules
    def test_site_extras_mails(self):
        xml_fn = get_resource_path("./files/site_gocdb.xml")
        site_rules_fn = get_resource_path("./files/site_rules_extras.json")

        with open(xml_fn, 'r') as xml_file:
            xml_data = xml_file.read().replace('\n', '')

            # Select contacts using notification flag on
            with open(site_rules_fn, 'r') as json_file:
                json_data = json_file.read().replace('\n', '')
                exp_json = json.loads(json_data)

                use_notif_flag = True
                test_emails = ["test1@email.foo", "test2@email.foo", "test3@email.foo"]
                extra_emails = ["extra01@email.foo", "extra02@email.foo"]
                contacts = argoalert.gocdb_to_contacts(xml_data, use_notif_flag, test_emails)

                rules = argoalert.contacts_to_alerta(contacts, extra_emails)

                self.assertEqual(exp_json, rules)

    # Test argowebapi contacts
    def test_argo_web_api(self):
        endpoint_data_fn = get_resource_path("./files/argowebapi_endpoint_data.json")
        group_data_fn = get_resource_path("./files/argowebapi_group_data.json")
        api_contacts_fn = get_resource_path("./files/api_contacts.json")

        with open(endpoint_data_fn, 'r') as endpoint_txt:
            endpoint_clean = endpoint_txt.read().replace('\n', '')
            endpoint_data = json.loads(endpoint_clean)

            with open(group_data_fn, 'r') as group_txt:
                group_clean = group_txt.read().replace('\n', '')
                group_data = json.loads(group_clean)

                with open(api_contacts_fn, 'r') as api_contacts_txt:
                    api_contacts_clean = api_contacts_txt.read().replace('\n', '')
                    api_contacts_data = json.loads(api_contacts_clean)

                    contacts = argoalert.argo_web_api_to_contacts(endpoint_data,group_data,True)
                    print(json.dumps(contacts, indent=4))
                    print(json.dumps(api_contacts_data, indent=4))
                    self.assertEqual(contacts,api_contacts_data)


    def test_gen_group_contacts(self):
        endpoint_data_fn = get_resource_path("./files/argowebapi_endpoint_data.json")
        group_data_fn = get_resource_path("./files/argowebapi_group_data.json")
        gen_contacts_fn = get_resource_path("./files/gen_endpoint_contacts.json")

        with open(endpoint_data_fn, 'r') as endpoint_txt:
            endpoint_clean = endpoint_txt.read().replace('\n', '')
            endpoint_data = json.loads(endpoint_clean)

            with open(group_data_fn, 'r') as group_txt:
                group_clean = group_txt.read().replace('\n', '')
                group_data = json.loads(group_clean)

                with open(gen_contacts_fn, 'r') as gen_contacts_txt:
                    gen_contacts_clean = gen_contacts_txt.read().replace('\n', '')
                    gen_contacts_data = json.loads(gen_contacts_clean)

                    gen_contacts = argoalert.gen_endpoint_contacts_from_groups(group_data, endpoint_data)
                    self.assertEqual(gen_contacts,gen_contacts_data)

    def test_gen_group_contacts_filter(self):
        endpoint_data_fn = get_resource_path("./files/argowebapi_endpoint_data.json")
        group_data_fn = get_resource_path("./files/argowebapi_group_data.json")
        gen_contacts_fn = get_resource_path("./files/gen_endpoint_contacts_filter.json")

        with open(endpoint_data_fn, 'r') as endpoint_txt:
            endpoint_clean = endpoint_txt.read().replace('\n', '')
            endpoint_data = json.loads(endpoint_clean)

            with open(group_data_fn, 'r') as group_txt:
                group_clean = group_txt.read().replace('\n', '')
                group_data = json.loads(group_clean)

                with open(gen_contacts_fn, 'r') as gen_contacts_txt:
                    gen_contacts_clean = gen_contacts_txt.read().replace('\n', '')
                    gen_contacts_data = json.loads(gen_contacts_clean)

                    gen_contacts = argoalert.gen_endpoint_contacts_from_groups(group_data, endpoint_data, "SERVICEGROUPS")
                    print(json.dumps(gen_contacts, indent=4))
                    print(json.dumps(gen_contacts_data, indent=4))
                    self.assertEqual(gen_contacts,gen_contacts_data)


