from aws_cdk import (
    CfnTag,
    Fn,
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam
)
from constructs import Construct

class EC2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, security_grp, subnet, instance_type, image_id, key_name, az1, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        with open("cdk_practice/bootstrap_scripts/config_tomcat.sh", mode="r") as file:
            user_data = file.read()

        role = iam.Role(self, "ec2-role",
                        assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                        managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSSMFullAccess'),
                                        iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSSMManagedInstanceCore'),
                                        iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AmazonEC2RoleforSSM')
                                        ],
                        role_name="ec2-role"
        )

        iam_Ins_profile = iam.CfnInstanceProfile(self, "MyInstanceProfile",
                                                roles=[role.role_name],
                                                instance_profile_name="SSMToEC2"
        )

        self.web_server = ec2.CfnInstance(self, "webserver01",
                                availability_zone=az1,
                                instance_type=(instance_type),
                                image_id=image_id,
                                subnet_id=subnet,
                                security_group_ids=[security_grp],
                                disable_api_termination=False,
                                key_name=key_name,
                                user_data=Fn.base64(user_data),
                                private_ip_address="10.0.0.34",
                                iam_instance_profile=iam_Ins_profile.instance_profile_name,
                                tags=[CfnTag(key="Name", value="webserver-01")]
        )