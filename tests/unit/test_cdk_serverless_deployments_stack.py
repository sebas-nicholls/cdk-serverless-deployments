import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_serverless_deployments.cdk_serverless_deployments_stack import CdkServerlessDeploymentsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_serverless_deployments/cdk_serverless_deployments_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkServerlessDeploymentsStack(app, "cdk-serverless-deployments")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
