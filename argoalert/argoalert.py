from kafka import KafkaConsumer
import json
import requests
import logging


def transform(argo_event, environment):
    """Transform an argo status event to an alerta alert

    Args:
        argo_event: obj. Json representation of an argo status event
        environment: str. Alerta enviroment parameter to build the alert

    Return:
        obj: Json representation of an alerta alert
    """
    status = argo_event["status"]
    hostname = argo_event["hostname"]
    metric = argo_event["metric"]
    summary = argo_event["summary"]
    group = argo_event["group"]
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
              "service": alerta_service, "text": summary, "severity": status}

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
    headers = {'Authorization': 'Key ' + alerta_token}
    r = requests.post(alerta_url + "/alert", headers=headers,
                      data=json.dumps(alerta))
    if r.status_code == 201:
        logging.info("Alert send to alerta succesfully")
    else:
        logging.warning("Alert wasn't send to alerta")
        logging.warning(r.text)


def start_listening(environment, log_level, kafka_endpoint, kafka_topic,
                    alerta_endpoint, alerta_token):
    """Start listening to a kafka topic and send alerts to an alerta endpoint

    Args:
        environment: str. Alerta environment to be used (e.g. 'Devel')
        log_level: str. logging level (e.g. 'INFO', 'WARNING', 'ERROR')
        kafka_endpoint: str. kafka broker endpoint
        kafka_topic: str. kafka topic to listen t
        alerta_endpoint: str. Alerta api endpoint
        alerta_token: str. Alerta api access token

    """
    logging.basicConfig(level=log_level)

    # Initialize kafka
    consumer = KafkaConsumer(kafka_topic,
                             group_id='argo-group',
                             bootstrap_servers=[kafka_endpoint])
    for message in consumer:
        read_and_send(message, environment, alerta_endpoint, alerta_token)
