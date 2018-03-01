from kafka import KafkaConsumer
from requests.auth import HTTPBasicAuth
import json
import requests
import logging
from defusedxml.minidom import parseString



def transform(argo_event, environment):
    """Transform an argo status event to an alerta alert

    Args:
        argo_event: obj. Json representation of an argo status event
        environment: str. Alerta enviroment parameter to build the alert

    Return:
        obj: Json representation of an alerta alert
    """
    status = argo_event["status"].lower()
    hostname = argo_event["hostname"]
    metric = argo_event["metric"]
    group = argo_event["endpoint_group"]
    etype = argo_event["type"]
    service = argo_event["service"]

    # alerta vars
    resource = ""
    event = "status"
    alerta_service = []

    if etype == "endpoint_group":
        alerta_service.append("endpoint_group")
        resource = group
    elif etype == "service":
        alerta_service.append("service")
        resource = group + "/" + service
    elif etype == "endpoint":
        alerta_service.append("endpoint")
        resource = group + "/" + service + "/" + hostname
    elif etype == "metric":
        alerta_service.append("metric")
        resource = group + "/" + service + "/" + hostname + "/" + metric
    # prepare alerta json
    alerta = {"environment": environment, "event": event, "resource": resource,
              "service": alerta_service, "severity": status}

    return alerta


def read_and_send(message, environment, alerta_url, alerta_token):
    """Read an argo status event from kafka and send it to alerta

    Args:
        message: str. Current message from kafka queue
        environment: str. Alerta environment to be used (e.g. 'Devel')
        alerta_url: str. Alerta api endpoint
        alerta_token: str. Alerta api access token

    """
    try:
        argo_event = json.loads(message.value)
    except ValueError:
        logging.warning("NOT JSON: " + message.value)
        return

    try:
        alerta = transform(argo_event, environment)
    except KeyError:
        logging.warning("WRONG JSON SCHEMA: " + message.value)
        return

    logging.info("Attempting to send alert:" + json.dumps(alerta))
    headers = {'Authorization': 'Key ' + alerta_token,
               'Content-Type': 'application/json'}

    r = requests.post(alerta_url + "/alert", headers=headers,
                      data=json.dumps(alerta))
    
    if r.status_code == 201:
        logging.info("Alert send to alerta successfully")
    else:
        logging.warning("Alert wasn't send to alerta")
        logging.warning(r.text)


def start_listening(environment, kafka_endpoints, kafka_topic,
                    alerta_endpoint, alerta_token):
    """Start listening to a kafka topic and send alerts to an alerta endpoint

    Args:
        environment: str. Alerta environment to be used (e.g. 'Devel')
        kafka_endpoints: str. kafka broker endpoint
        kafka_topic: str. kafka topic to listen t
        alerta_endpoint: str. Alerta api endpoint
        alerta_token: str. Alerta api access token

    """

    # Initialize kafka
    kafka_list = kafka_endpoints.split(',')

    consumer = KafkaConsumer(kafka_topic,
                             group_id='argo-alerta',
                             bootstrap_servers=kafka_list)
    for message in consumer:
        read_and_send(message, environment, alerta_endpoint, alerta_token)


def gocdb_to_contacts(gocdb_xml, use_notif_flag, test_emails):
    """Transform gocdb xml schema info on generic contacts json information

    Args:
        gocdb_xml: str. Data in gocdb xml format
        use_notif_flag: boolean. Examine or not notifications flag when gathering contacts

    Return:
        obj: Json representation of contact information
    """
    xmldoc = parseString(gocdb_xml)
    contacts = []
    clist = xmldoc.getElementsByTagName("CONTACT_EMAIL")

    indx = 0
    for item in clist:

        # By default accept all contacts
        notify_val = 'Y'
        # If flag on accept only contacts with notification flag
        if use_notif_flag:
            notify = item.parentNode.getElementsByTagName('NOTIFICATIONS')[0]
            # if notification flag is set to false skip
            notify_val = notify.firstChild.nodeValue

        if notify_val == 'TRUE' or notify_val == 'Y':
            c = dict()
            c["type"] = item.parentNode.tagName

            # Check if name tag exists
            name_tags = item.parentNode.getElementsByTagName("NAME")
            # if not check short name tag
            if len(name_tags) == 0:
                name_tags = item.parentNode.getElementsByTagName("SHORT_NAME")

            # if still no name related tag skip
            if len(name_tags) == 0:
                continue

            c["name"] = name_tags[0].firstChild.nodeValue

            if test_emails is None:
                c["email"] = item.firstChild.nodeValue
            else:
                c["email"] = test_emails[indx % len(test_emails)]
                indx = indx + 1

            contacts.append(c)

    return contacts


def contacts_to_alerta(contacts):
    """Transform a contacts json object to alerta's rule json object

    Args:
        contacts: obj. Json representation of contact information

    Return:
        obj: Json representation of alerta mailer rules
    """
    rules = []
    for c in contacts:

        rule_name = "rule_" + c["name"]
        rule_fields = [{u"field": u"resource", u"regex": c["name"]}]
        rule_contacts = [c["email"]]
        rule_exclude = True
        rule = {u"name": rule_name, u"fields": rule_fields, u"contacts": rule_contacts, u"exclude": rule_exclude}
        rules.append(rule)

    logging.info("Generated " + str(len(rules)) + " alerta rules from contact information")
    return rules


def get_gocdb(api_url, auth_info, ca_bundle):
    """Http Rest call to gocdb-api to get xml contact information

    Args:
        api_url: str. Gocdb url call
        auth_info: dict. Contains authorization information
        ca_bundle: str. CA bundle file


    Return:
        str: gocdb-api xml response
    """

    verify = False
    if ca_bundle is not None:
        verify = ca_bundle

    logging.info("Requesting data from gocdb api: " + api_url)
    if auth_info["method"]=="cert":
        r = requests.get(api_url, cert=(auth_info["cert"], auth_info["key"]), verify=verify)
    else:
        r = requests.get(api_url, auth=HTTPBasicAuth(auth_info["user"], auth_info["pass"]), verify=verify)

    if r.status_code == 200:
        logging.info("Gocdb data retrieval successful")
        return r.text.encode('utf-8').strip()

    return ""


def write_rules(rules, outfile):
    """Writes alerta email rules to a specific output file

    Args:
        rules: obj. json representation of alerta rules
        outfile: str. output filename path
    """

    json_str = json.dumps(rules, indent=4)
    logging.info("Saving rule to file: " + outfile)
    with open(outfile, "w") as output_file:
        output_file.write(json_str)
