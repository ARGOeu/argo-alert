#!/usr/bin/env python
from argparse import ArgumentParser
from ConfigParser import SafeConfigParser
import sys
from kafka import KafkaConsumer
import json
import requests

def read_and_send(message,environment,alerta_url,alerta_token):
    argo_event = json.loads(message.key)
    status = argo_event.status
    hostname = argo_event.hostname
    metric = argo_event.metric
    summary = argo_event.summary
    group = argo_event.group
    type = argo_event.type

    # alerta vars
    resource = ""
    event = "status"
    service = ""

    if type == "endpoint_group":
        service ="endpoint_group"
        resource = group
    elif type == "service":
        service = "service"
        resource = group+"/"+service
    elif type == "endpoint":
        service = "endpoint"
        resource = group+"/"+service+"/"+hostname
    elif type == "metric":
        service = "metric"
        resource = group+"/"+service+"/"+hostname+"/"+metric

    alerta = {}
    ## prepare alerta json
    alerta["environment"] = environment
    alerta["event"] = event
    alerta["resource"] = resource
    alerta["service"] = service
    alerta["text"] = summary
    alerta["severity"] = status


    headers = {'Authorization': 'Key '+ alerta_token}
    r = requests.post(alerta_url+"/alerts",headers=headers, data=alerta)
    print r






def main(args=None):

    # default config
    fn_cfg = "/etc/argo-alert.conf"
    arcomp_conf = "/etc/ar-compute/"
    # Init configuration
    parser = SafeConfigParser()
    parser.read(args.config)

    kafka_endpoint = parser.get("kafka","endpoint")
    kafka_topic = parser.get("kafka","topic")
    alerta_endpoint = parser.get("alerta","endpoint")
    environment = parser.get("alerta","environment")
    alerta_token = parser.get("alerta","token")


    # Initialize kafka
    consumer = KafkaConsumer(kafka_topic,
                             group_id='argo-group',
                             bootstrap_servers=[kafka_endpoint])
    for message in consumer:
       read_and_send(message,environment,alerta_endpoint,alerta_token)




if __name__ == "__main__":

    # Feed Argument parser with the description of the 3 arguments we need
    # (input_file,output_file,schema_file)
    arg_parser = ArgumentParser(
        description="ingest argo status data to alerta system")
    arg_parser.add_argument(
        "-c", "--config", help="config", dest="config", metavar="string", required="TRUE")

    # Parse the command line arguments accordingly and introduce them to
    # main...
    sys.exit(main(arg_parser.parse_args()))