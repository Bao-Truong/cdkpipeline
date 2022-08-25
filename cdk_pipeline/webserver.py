from os import path
from aws_cdk import (
    Stack,
    CfnOutput
)
from constructs import Construct
import aws_cdk.aws_lambda as lmb
import aws_cdk.aws_apigateway as apigw


class WebserverStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        thisPath = path.dirname(__file__)

        handler = lmb.Function(self, "Handler",
                               runtime=lmb.Runtime.PYTHON_3_9,
                               code=lmb.Code.from_asset(
                                   path.join(thisPath, "lambda")),
                               handler="handler.handler")

        gw = apigw.LambdaRestApi(self, 'Gateway',
                                 description="Endpoint for a simple Lambda-powered webserver",
                                 handler=handler.current_version)

        # self.url_output = CfnOutput(self, 'Url',
        #                             value=gw.url)
