from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    aws_elasticloadbalancingv2 as elbv2
)
from constructs import Construct

class AlbStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc, security_grp, webserver, subnet_01, subnet_02, certificate_arn, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.target_group = elbv2.CfnTargetGroup(self, "MyTg",
                                                target_type="instance",
                                                name="webserver-tg",
                                                protocol="HTTPS",
                                                port=443,
                                                vpc_id=vpc,
                                                health_check_protocol="HTTPS",
                                                health_check_path="/helloworld/",
                                                targets=[elbv2.CfnTargetGroup.TargetDescriptionProperty(id=webserver)]
        )

        self.alb = elbv2.CfnLoadBalancer(self, "webserver_alb",
                                        ip_address_type="ipv4",
                                        name="webserver-alb",
                                        type="application",
                                        security_groups=[security_grp],
                                        subnets=[subnet_01,subnet_02]
        )

        listener_https = elbv2.CfnListener(self, "MyListenerHTTPS",
            default_actions=[elbv2.CfnListener.ActionProperty(type="forward", target_group_arn=self.target_group.attr_target_group_arn)],
            load_balancer_arn=self.alb.ref,
            port=443,
            protocol="HTTPS",
            certificates=[elbv2.CfnListener.CertificateProperty(certificate_arn=certificate_arn)] #cert SSL vi co function ho tro import nen em dang import bang console
            )

        listener_rule = elbv2.CfnListenerRule(self, "ListenerRuleHttps",
                                            actions=[elbv2.CfnListenerRule.ActionProperty(type="forward", target_group_arn= self.target_group.attr_target_group_arn)],
                                            conditions=[elbv2.CfnListenerRule.RuleConditionProperty(field="path-pattern",
                                                path_pattern_config=elbv2.CfnListenerRule.PathPatternConfigProperty(
                                                    values=["/helloworld"]
                                                )
                                            )],
                                            listener_arn=listener_https.attr_listener_arn,
                                            priority=100
        )

        listener_http = elbv2.CfnListener(self, "MyListenerHTTP",
            default_actions=[elbv2.CfnListener.ActionProperty(type="redirect", redirect_config=elbv2.CfnListener.RedirectConfigProperty(
                                                status_code="HTTP_301",
                                                protocol="HTTPS",
                                                port="443",
                                                path="/helloworld"
                                                ))],
            load_balancer_arn=self.alb.ref,
            port=80,
            protocol="HTTP"
        )