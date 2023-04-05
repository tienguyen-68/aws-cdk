#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_practice.vpc_stack import VpcStack
from cdk_practice.security_group_stack import SecurityGroupStack
from cdk_practice.ec2_stack import EC2Stack
from cdk_practice.alb_stack import AlbStack
from cdk_practice.asg_stack import AsgStack
from cdk_practice.lambda_stack import LambdaStack

app = cdk.App()

account = app.node.try_get_context("account")
region = app.node.try_get_context("region")
image_id = app.node.try_get_context("image_id")
key_name = app.node.try_get_context("key_name")
instance_type = app.node.try_get_context("instance_type")
az1 = app.node.try_get_context("az1")
az2 = app.node.try_get_context("az2")
bucket_name = app.node.try_get_context("bucket")
source_s3deploymnt = app.node.try_get_context("source_s3deploymnt")
lambda_source = app.node.try_get_context("lambda_source")
certificate_arn = app.node.try_get_context("certificate_arn")

env = cdk.Environment(account=account, region=region)

vpc_stack = VpcStack(app, "MyVpcStack", az1=az1, az2=az2)

sg_stack = SecurityGroupStack(app, "MySgStack", 
                    vpc=vpc_stack.vpc.attr_vpc_id
                    )

ec2_stack = EC2Stack(app, "MyEC2Stack", 
                    security_grp=sg_stack.webserver_sg.attr_group_id, 
                    subnet=vpc_stack.public_subnet_01.attr_subnet_id,
                    instance_type=instance_type,
                    image_id=image_id,
                    key_name=key_name,
                    az1=az1
                    )

alb_stack = AlbStack(app, "MyAlbStack", 
                    vpc=vpc_stack.vpc.attr_vpc_id, 
                    security_grp=sg_stack.webserver_sg.attr_group_id, 
                    webserver=ec2_stack.web_server.ref, 
                    subnet_01=vpc_stack.public_subnet_01.attr_subnet_id, 
                    subnet_02=vpc_stack.public_subnet_02.attr_subnet_id,
                    certificate_arn=certificate_arn
                    ) 

asg_stack = AsgStack(app, "MyAsgStack", 
                    tg_arn=alb_stack.target_group.attr_target_group_arn, 
                    security_grp=sg_stack.webserver_sg.attr_group_id, 
                    subnet_01=vpc_stack.public_subnet_01.attr_subnet_id, 
                    subnet_02=vpc_stack.public_subnet_02.attr_subnet_id,
                    az1=az1,
                    az2=az2,
                    instance_type=instance_type,
                    image_id=image_id,
                    key_name=key_name
                    )

lambda_stack = LambdaStack(app, "MyLambdaStack", 
                    bucket_name=bucket_name, 
                    source_s3deploymnt=source_s3deploymnt, 
                    lambda_source=lambda_source
                    )
app.synth()
