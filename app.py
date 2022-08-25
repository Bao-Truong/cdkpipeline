#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_pipeline.webserver import WebserverStack
from cdk_pipeline.pipeline_stacks import PipelineStack
from dotenv import load_dotenv

load_dotenv()

app = cdk.App()
WebserverStack(app, "WebserverStack",
               env=cdk.Environment(account=os.environ.get(
                   "CDK_DEFAULT_ACCOUNT"), region=os.environ.get("CDK_DEFAULT_ACCOUNT")),
               )


PipelineStack(app, 'PipelineStack',
              env=cdk.Environment(account=os.environ.get(
                  "CDK_DEFAULT_ACCOUNT"), region=os.environ.get("CDK_DEFAULT_ACCOUNT")),
              )


app.synth()
