from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    CfnOutput
)
from constructs import Construct

class VpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, az1, az2, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create a vpc

        self.vpc = ec2.CfnVPC(self, "MyVPC",
                    cidr_block="10.0.0.0/16",
                    enable_dns_hostnames=True,
                    enable_dns_support=True
        )

        self.public_subnet_01 = ec2.CfnSubnet(self, "public_subnet_01",  
                                            vpc_id=self.vpc.attr_vpc_id, 
                                            cidr_block="10.0.0.0/17", 
                                            availability_zone=az1,
                                            map_public_ip_on_launch=True
        )

        self.public_subnet_02 = ec2.CfnSubnet(self, "public_subnet_02", 
                                            vpc_id=self.vpc.attr_vpc_id,
                                            cidr_block="10.0.128.0/18",
                                            availability_zone=az2,
                                            map_public_ip_on_launch=True,                                            
        )

        igw = ec2.CfnInternetGateway(self, 'My_Internet_Gateway')

        vpc_gw_attachment = ec2.CfnVPCGatewayAttachment(self, 'VPC Gateway Attachment',
                                                        vpc_id=self.vpc.attr_vpc_id,
                                                        internet_gateway_id=igw.attr_internet_gateway_id
        )

        public_route_table = ec2.CfnRouteTable(
            self,
            'My Public Route Table',
            vpc_id = self.vpc.attr_vpc_id
        )

        public_route = ec2.CfnRoute(
            self,
            'My Public Route',
            destination_cidr_block = '0.0.0.0/0',
            route_table_id = public_route_table.attr_route_table_id,
            gateway_id = igw.attr_internet_gateway_id
        )

        associate_public_subnet1 = ec2.CfnSubnetRouteTableAssociation(
            self, 
            'PublicSubnet1RouteTableAssociation',
            route_table_id = public_route_table.attr_route_table_id, 
            subnet_id = self.public_subnet_01.attr_subnet_id
        )

        associate_public_subnet2 = ec2.CfnSubnetRouteTableAssociation(
            self, 
            'PublicSubnet2RouteTableAssociation',
            route_table_id = public_route_table.attr_route_table_id, 
            subnet_id = self.public_subnet_02.attr_subnet_id
        )
            


