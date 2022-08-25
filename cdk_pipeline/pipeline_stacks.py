from distutils import core
from aws_cdk import (
    CfnOutput,
    SecretValue,
    Stack,
    aws_codepipeline as codepipeline,
    pipelines,
    aws_codepipeline_actions as cpactions,
    SecretValue
)
import aws_cdk as cdk
from constructs import Construct
from .webserver_stages import WebserverStage
import os


class PipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.supported_regions = ["us-east-1", "us-east-2"]

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        self.pipeline = pipelines.CodePipeline(self, 'Pipeline',


                                               pipeline_name='WebinarPipeline',

                                               synth=pipelines.ShellStep("Synth",
                                                                         input=pipelines.CodePipelineSource.git_hub(
                                                                             "Bao-Truong/cdkpipeline", "master", authentication=SecretValue.secrets_manager('github-token'),
                                                                             trigger=cpactions.GitHubTrigger.POLL),
                                                                         commands=[
                                                                             "npm install -g aws-cdk", "python -m pip install -r requirements.txt", "cdk synth"]
                                                                         )
                                               )
        self.distribute_to_region()

    def distribute_to_region(self):
        wave = self.pipeline.add_wave("wave")
        for region in self.supported_regions:
            stage = wave.add_stage(WebserverStage(self, f"webserStage-{region}",
                                                        env=cdk.Environment(account=os.environ.get(
                                                            "CDK_DEFAULT_ACCOUNT"), region=region)
                                                  ))
            stage.add_pre(pipelines.ManualApprovalStep('approval'))
