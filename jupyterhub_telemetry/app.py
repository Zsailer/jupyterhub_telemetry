import os
from tornado import web, ioloop

from .handlers import endpoints
from jupyterhub.utils import url_path_join

from jupyter_core.application import JupyterApp
from traitlets import (
    default,
    Unicode,
    Integer
)


class JupyterHubTelemetry(JupyterApp):
    name = "jupyterhub-telemetry"
    
    description = """
    A server for collecting telemetry data from a JupyterHub deployment.
    """
    
    port = Integer(
        9090,
        help="""
        Port on which to run this service.
        """ 
    ).tag(config=True)

    base_url = Unicode(
        help="""
        Base url for this service. Defaults to /services/telemetry 
        """
    ).tag(config=True)
    
    @default('base_url')
    def _default_base_url(self):
        return os.environ['JUPYTERHUB_SERVICE_PREFIX']

    address = Unicode(
        help="""127.0.0.1"""
    ).tag(config=True)

    @default('address')
    def _default_address(self):
        return os.environ['JUPYTERHUB_SERVICE_URL']

    def init_handlers(self):
        self.handlers = []
        # Prepend the hub 
        for endpoint, handler in endpoints:
            url = url_path_join(self.base_url, endpoint)
            self.handlers.append(
                (url, handler)
            )

    def init_webapp(self):
        self.webapp = web.Application(self.handlers)

    def initialize(self, *args, **kwargs):
        # Initialize.
        super(JupyterHubTelemetry, self).initialize(*args, **kwargs)

        # Initialize the pieces.
        self.init_handlers()
        self.init_webapp()

    def start(self):
        super(JupyterHubTelemetry, self).start()
        
        # Start listening to web application.
        self.webapp.listen(
            port=self.port,
            address=self.address
        )
        ioloop.IOLoop.current().start()
        

main = JupyterHubTelemetry.launch_instance

if __name__ == '__main__': 
    main()