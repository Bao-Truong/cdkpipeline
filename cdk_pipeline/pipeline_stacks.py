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

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        pipeline = pipelines.CodePipeline(self, 'Pipeline',


                                          pipeline_name='WebinarPipeline',

                                          synth=pipelines.ShellStep("Synth",
                                                                    input=pipelines.CodePipelineSource.git_hub(
                                                                        "Bao-Truong/cdkpipeline", "master", authentication=SecretValue.secrets_manager('github-token'),
                                                                        trigger=cpactions.GitHubTrigger.POLL),
                                                                    commands=[
                                                                        "npm install -g aws-cdk", "python -m pip install -r requirements.txt", "cdk synth"]
                                                                    )
                                          )

        wave = pipeline.add_wave("wave")

        useast2_stage = wave.add_stage(WebserverStage(self, "webserStage-useast-2",
                                                      env=cdk.Environment(account=os.environ.get(
                                                          "CDK_DEFAULT_ACCOUNT"), region="us-east-2")
                                                      ))
        useast1_stage = wave.add_stage(WebserverStage(self, "webserStage-useast-1",
                                                       env=cdk.Environment(account=os.environ.get(
                                                           "CDK_DEFAULT_ACCOUNT"), region="us-east-1")
                                                       ))
        # testing_stage = pipeline.add_stage(WebserverStage(self, "webserStage",
        #                                                   env=cdk.Environment(account=os.environ.get(
        #                                                       "CDK_DEFAULT_ACCOUNT"), region=os.environ.get("CDK_DEFAULT_ACCOUNT"))
        #                                                   ))
        # testing_stage.add_post(ManualApprovalStep('approval'))

        useast1_stage.add_post(pipelines.ManualApprovalStep('approval'))
        useast2_stage.add_post(pipelines.ManualApprovalStep('approval'))
