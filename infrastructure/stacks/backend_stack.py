from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    CfnOutput,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_logs as logs,
)
from constructs import Construct


class BackendStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB Table
        events_table = dynamodb.Table(
            self,
            "EventsTable",
            partition_key=dynamodb.Attribute(
                name="eventId", type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,  # Change to RETAIN for production
            point_in_time_recovery=True,
            table_name="events-table",
        )

        # Lambda Function with bundled dependencies
        api_lambda = _lambda.Function(
            self,
            "EventsApiFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="main.handler",
            code=_lambda.Code.from_asset(
                "../backend",
                bundling={
                    "image": _lambda.Runtime.PYTHON_3_11.bundling_image,
                    "command": [
                        "bash",
                        "-c",
                        "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output",
                    ],
                },
            ),
            timeout=Duration.seconds(30),
            memory_size=512,
            environment={
                "DYNAMODB_TABLE_NAME": events_table.table_name,
                "AWS_REGION": self.region,
                "CORS_ORIGINS": "*",
                "CORS_ALLOW_CREDENTIALS": "false",
                "DEBUG": "false",
            },
            log_retention=logs.RetentionDays.ONE_WEEK,
        )

        # Grant DynamoDB permissions
        events_table.grant_read_write_data(api_lambda)

        # Lambda Function URL (simpler and faster than API Gateway)
        function_url = api_lambda.add_function_url(
            auth_type=_lambda.FunctionUrlAuthType.NONE,
            cors=_lambda.FunctionUrlCorsOptions(
                allowed_origins=["*"],
                allowed_methods=[_lambda.HttpMethod.ALL],
                allowed_headers=["*"],
                max_age=Duration.seconds(3600),
            ),
        )

        # Outputs
        CfnOutput(
            self,
            "ApiUrl",
            value=function_url.url,
            description="Lambda Function URL (Public API endpoint)",
            export_name="EventsApiUrl",
        )

        CfnOutput(
            self,
            "ApiDocsUrl",
            value=f"{function_url.url}docs",
            description="API Documentation URL",
        )

        CfnOutput(
            self,
            "TableName",
            value=events_table.table_name,
            description="DynamoDB table name",
            export_name="EventsTableName",
        )

        CfnOutput(
            self,
            "LambdaFunctionName",
            value=api_lambda.function_name,
            description="Lambda function name",
            export_name="EventsLambdaFunction",
        )
