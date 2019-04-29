
from jupyterhub.services.auth import HubAuthenticated
from tornado import web


class TelemetryHandler(HubAuthenticated, web.RequestHandler):
    """Handler for storing event data."""

    #@web.authenticated
    def get(self):
        self.write('worked')


    #@web.authenticated
    def post(self):
        pass


endpoints = [
    ('test', TelemetryHandler)
] 