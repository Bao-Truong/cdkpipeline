#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_pipeline.cdk_pipeline_stack import CdkPipelineStack
from cdk_pipeline.pipeline_stacks import PipelineStack

app = cdk.App()
CdkPipelineStack(app, "CdkPipelineStack",
                 env=cdk.Environment(account='956722820961', region='us-east-2'),
                 )
                

PipelineStack(app, 'PipelineStack',
              env=cdk.Environment(account='956722820961', region='us-east-2'),
              )


app.synth()
