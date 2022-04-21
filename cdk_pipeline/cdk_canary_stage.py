import aws_cdk as cdk
from constructs import Construct

from cdk_serverless_deployments.cdk_canary_deployment_stack import CdkCanaryDeploymentStack

class CdkCanaryPipelineAppStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        application_stack = CdkCanaryDeploymentStack(self, "CdkCanaryDeploymentStack")