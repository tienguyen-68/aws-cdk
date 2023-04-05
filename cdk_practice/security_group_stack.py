from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    Fn
)
from constructs import Construct
#from cdk_practice.vpc_stack import VpcStack
class SecurityGroupStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #create a security group
        self.webserver_sg = ec2.CfnSecurityGroup(self, "webserver_sg", 
                                                group_name="webserver_sg", 
                                                group_description='allow port 8443 and 22', 
                                                vpc_id=vpc)

        #allow access  outbound
        ec2.CfnSecurityGroupEgress(self, "outbound",
                                ip_protocol="-1",
                                cidr_ip="0.0.0.0/0",
                                from_port=None,
                                to_port=None,
                                group_id=self.webserver_sg.attr_group_id
        )
        #allow access  8443
        ec2.CfnSecurityGroupIngress(self, "allow-https",
                                ip_protocol="tcp",
                                cidr_ip="0.0.0.0/0",
                                group_id=self.webserver_sg.attr_group_id,
                                from_port=443,
                                to_port=443
        )
        #allow access 22       
        ec2.CfnSecurityGroupIngress(self,
                                "allow-ssh",
                                ip_protocol="tcp",
                                cidr_ip="0.0.0.0/0",
                                group_id=self.webserver_sg.attr_group_id,
                                from_port=22,
                                to_port=22
        )
        #allow access 80 
        ec2.CfnSecurityGroupIngress(self,
                                "allow-http",
                                ip_protocol="tcp",
                                cidr_ip="0.0.0.0/0",
                                group_id=self.webserver_sg.attr_group_id,
                                from_port=80,
                                to_port=80
        )