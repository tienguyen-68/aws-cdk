from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_iam as iam,
    aws_s3_deployment as s3deploy
)
from aws_cdk.aws_lambda_event_sources import S3EventSource
from constructs import Construct

class LambdaStack(Stack):

    #def __init__(self, scope: Construct, construct_id: str, vpc, subnet_01, subnet_02, security_grp, **kwargs) -> None:
    def __init__(self, scope: Construct, construct_id: str, bucket_name, source_s3deploymnt, lambda_source, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        bucket = s3.Bucket(self, "lambda-bucket1",
                            bucket_name=bucket_name
                            #bucket_encryption=s3.CfnBucket.BucketEncryptionProperty(server_side_encryption_configuration=[s3.CfnBucket.ServerSideEncryptionRuleProperty(server_side_encryption_by_default=(s3.CfnBucket.ServerSideEncryptionByDefaultProperty(kms_master_key_id="050355d3-7623-48c6-8235-3b7b73feb891", sse_algorithm="aws:kms")))]),
                            
        )
        
        code = s3deploy.BucketDeployment(
            self, "s3-deployment",
            destination_bucket=bucket,
            sources=[s3deploy.Source.asset(source_s3deploymnt)]
        )

        
        self.lbd_function = _lambda.Function(
            self, "MyLambdaFunction",
            function_name="myfunction",
            handler='lambda_function.lambda_handler',
            runtime=_lambda.Runtime.PYTHON_3_8,
            timeout=Duration.seconds(30),
            code=_lambda.Code.from_asset(lambda_source),
            role=iam.Role(self, "role-lambda-python",
                        assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
                        managed_policies=[
                            iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                            iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSSMFullAccess'),
                            iam.ManagedPolicy.from_aws_managed_policy_name('AmazonEC2FullAccess'),
                            iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess'),
                        ],
                        role_name="role-lambda-python"
            )
            
        )
        
        self.lbd_function.add_event_source(S3EventSource(bucket, events=[s3.EventType.OBJECT_CREATED]))

