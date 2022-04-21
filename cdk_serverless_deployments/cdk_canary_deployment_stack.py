from ast import alias
from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as api_gateway,
    aws_dynamodb as dynamodb, 
    aws_cloudwatch as cloudwatch,
    aws_codedeploy as codedeploy
)
from constructs import Construct

class CdkCanaryDeploymentStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        dynamo_table = dynamodb.Table(self, "canaryTable",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.NUMBER),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )
        
        lambda_function = lambda_.Function(self, "canaryLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="hello_world.lambda_handler",
            code=lambda_.Code.from_asset("./lambdas/src")
        )

        stage = lambda_.Alias(self, "canaryLambdaStage", alias_name="stage", version=lambda_function.current_version)

        lambda_function.add_environment("TABLE_NAME", dynamo_table.table_name)

        dynamo_table.grant_read_data(lambda_function)

        rest_api = api_gateway.LambdaRestApi(self, "canaryApi", handler=stage, deploy_options=api_gateway.StageOptions(stage_name="staging"))

        hello_resource = rest_api.root.add_resource("hello")

        hello_resource.add_method("GET", api_gateway.LambdaIntegration(stage))
        lambda_integration = api_gateway.LambdaIntegration(stage)

        failure_alarm = cloudwatch.Alarm(self, "canaryLambdaFalure",
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            alarm_description="Lastest deployment errors > 0",
            metric=stage.metric_errors(),
            threshold=1,
            evaluation_periods=1
        )
        deployment_group = codedeploy.LambdaDeploymentGroup(self, "CanaryDeployment",
            alias=stage,
            deployment_config=codedeploy.LambdaDeploymentConfig.CANARY_10_PERCENT_5_MINUTES,
            alarms=[failure_alarm]
        )

