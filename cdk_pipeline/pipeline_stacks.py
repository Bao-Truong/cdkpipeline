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


class PipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        pipeline = pipelines.CodePipeline(self, 'Pipeline',


                                          pipeline_name='WebinarPipeline',

                                          synth=pipelines.ShellStep("Synth",
                                                                    input=pipelines.CodePipelineSource.git_hub(
                                                                        "Bao-Truong/cdkpipeline", "master", authentication=SecretValue.secrets_manager("github_token"),
                                                                        trigger=cpactions.GitHubTrigger.POLL),
                                                                    commands=[
                                                                        "npm install -g aws-cdk", "python -m pip install -r requirements.txt", "cdk synth"]
                                                                    )
                                          )
