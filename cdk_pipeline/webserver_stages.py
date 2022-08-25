import aws_cdk as cdk
from constructs import Construct
from .webserver import WebserverStack


class WebserverStage(cdk.Stage):
    def __init__(self, scope: constructs.Construct, id: builtins.str, *, env: typing.Optional[typing.Union[Environment, typing.Dict[str, typing.Any]]] = None, outdir: typing.Optional[builtins.str] = None) -> None:
        super().__init__(scope, id, env=env, outdir)
        
        webserverstack= WebserverStack(self,"WebserverStack")
