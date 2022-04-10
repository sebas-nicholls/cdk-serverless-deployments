import aws_cdk as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from cdk_pipeline.cdk_serverless_deployments_stage import CdkPipelineAppStage
from constructs import Construct

class CdkPipelineStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        nich_bucket = s3.Bucket.from_bucket_name(self, "NichPipeTestBucket", "nich-pipe-test-bucket")
        
        pipeline = CodePipeline(self, "Pipeline",
                        pipeline_name="MyPipeline",
                        synth=ShellStep("Synth",
                            input=CodePipelineSource.connection("sebas-nicholls/cdk-serverless-deployments", "main",
                                connection_arn="arn:aws:codestar-connections:us-east-1:382821043170:connection/fd3bf842-26a1-4e32-a6bf-6683f6938d2a"),
                            install_commands=["npm install -g aws-cdk"],
                            commands=["pip install -r requirements.txt", "cdk synth"]
                        )
                    )
        pipeline.add_stage(CdkPipelineAppStage(self, "ServerlessDeployments",
            env=cdk.Environment(account="382821043170", region="us-east-1")))
                    