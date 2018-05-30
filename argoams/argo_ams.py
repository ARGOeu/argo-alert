from argo_ams_library import ArgoMessagingService, AmsMessage, AmsException
import logging
import json
import datetime
from alerta.plugins import PluginBase

try:
    from alerta.plugins import app  # alerta >= 5.0
except ImportError:
    from alerta.app import app  # alerta < 5.0

LOG = logging.getLogger('alerta.plugins.ams')


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.strftime('%Y-%m-%dT%H:%m:%SZ')
    raise TypeError("Unknown type")


class AmsPub(PluginBase):

    def __init__(self, name=None):

        # Get the required AMS host configuration parameter
        self.ams_host = app.config["AMS_HOST"]
        # Get the required AMS project parameter
        self.ams_project = app.config["AMS_PROJECT"]
        # Get the required AMS topic parameter
        self.ams_topic = app.config["AMS_TOPIC"]
        # Get the required AMS token parameter
        self.ams_token = app.config["AMS_TOKEN"]
        # If AMS_PROJECT empty then automatically use alert.enviroment value as ams project destination
        self.envproject = app.config["AMS_PROJECT"] is ''

        # Create an ams client
        self.ams = ArgoMessagingService(self.ams_host, self.ams_token, self.ams_project)

        super(AmsPub, self).__init__(name)

    def pre_receive(self, alert):
        return alert

    # After receiving the event publish it ot AMS
    def post_receive(self, alert):
        body = alert.get_body()
        try:
            # Construct json string from the alert object
            ams_msg = AmsMessage(data=json.dumps(body, default=datetime_handler))
            # Use environment as a project namespace in AMS
            if self.envproject:
                self.ams.project = body["environment"]

            LOG.info("ams pub to %s/project/%s/topic/%s" % (self.ams_host, self.ams.project, self.ams_topic))
            # Attempt to publish the alert to AMS
            self.ams.publish(self.ams_topic, ams_msg.dict())
        except Exception as exp:
            LOG.exception(exp)
            raise RuntimeError("ams exception: %s - %s" % (exp, body))

    def status_change(self, alert, status, text):
        return
