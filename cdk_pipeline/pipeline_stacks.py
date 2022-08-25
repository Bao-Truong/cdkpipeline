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

from constructs import Construct
from .webserver_stages import WebserverStage


class PipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        pipeline = pipelines.CodePipeline(self, 'Pipeline',


                                          pipeline_name='WebinarPipeline',

                                          synth=pipelines.ShellStep("Synth",
                                                                    input=pipelines.CodePipelineSource.git_hub(
                                                                        "Bao-Truong/cdkpipeline", "master", authentication=SecretValue.secretsManager("github-token"),
                                                                        trigger=cpactions.GitHubTrigger.POLL),
                                                                    commands=[
                                                                        "npm install -g aws-cdk", "python -m pip install -r requirements.txt", "cdk synth"]
                                                                    )
                                          )

        wave = pipeline.add_wave("wave")

        useast1_stage = wave.add_stage(WebserverStage(self, "webserStage",
                                                      env=cdk.Environment(account=os.environ.get(
                                                          "CDK_DEFAULT_ACCOUNT"), region="us-east-2")
                                                      ))
        useastr2_stage = wave.add_stage(WebserverStage(self, "webserStage",
                                                       env=cdk.Environment(account=os.environ.get(
                                                           "CDK_DEFAULT_ACCOUNT"), region="us-east-1")
                                                       ))
        # testing_stage = pipeline.add_stage(WebserverStage(self, "webserStage",
        #                                                   env=cdk.Environment(account=os.environ.get(
        #                                                       "CDK_DEFAULT_ACCOUNT"), region=os.environ.get("CDK_DEFAULT_ACCOUNT"))
        #                                                   ))
        # testing_stage.add_post(ManualApprovalStep('approval'))

        useast1_stage.add_post(cpactions.ManualApprovalAction('approval'))
        useast2_stage.add_post(cpactions.ManualApprovalAction('approval'))
