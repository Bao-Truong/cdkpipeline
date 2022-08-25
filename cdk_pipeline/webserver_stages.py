import aws_cdk as cdk
from constructs import Construct
from .webserver import WebserverStack


class WebserverStage(cdk.Stage):
    def __init__(self, scope: Construct, id: str, **kwagrs) -> None:
        super().__init__(scope, id, **kwagrs)

        webserverstack = WebserverStack(self, "WebserverStack")
