from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as api_gateway,
    aws_dynamodb as dynamodb
)
from constructs import Construct

class CdkServerlessDeploymentsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        dynamo_table = dynamodb.Table(self, "logicTable",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.NUMBER),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )
        
        lambda_function = lambda_.Function(self, "helloLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="hello_world.lambda_handler",
            code=lambda_.Code.from_asset("./lambdas/src")
        )

        lambda_function.add_environment("TABLE_NAME", dynamo_table.table_name)

        dynamo_table.grant_read_data(lambda_function)

        rest_api = api_gateway.RestApi(self, "deploymentsApi")

        hello_resource = rest_api.root.add_resource("hello")

        hello_resource.add_method("GET", api_gateway.LambdaIntegration(lambda_function))
        lambda_integration = api_gateway.LambdaIntegration(lambda_function)
