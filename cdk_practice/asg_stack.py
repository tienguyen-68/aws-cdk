from aws_cdk import (
    Fn,
    Stack,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
)
from constructs import Construct

class AsgStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, tg_arn, security_grp, subnet_01, subnet_02, image_id, instance_type, key_name, az1, az2, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        with open("cdk_practice/bootstrap_scripts/config_tomcat_asg.sh", mode="r") as file:
            user_data = file.read()
        #create template
        web_server_template = ec2.CfnLaunchTemplate(self, "web_server_template",
                                                launch_template_name="web_server_template",
                                                version_description="v1",
                                                launch_template_data=ec2.CfnLaunchTemplate.LaunchTemplateDataProperty(
                                                    instance_type=instance_type,
                                                    image_id=image_id, 
                                                    disable_api_termination=False,
                                                    user_data=Fn.base64(user_data),
                                                    security_group_ids=[security_grp],
                                                    key_name=key_name
                                                )                                            
        )
          
        #create asg
        self.web_server_asg = autoscaling.CfnAutoScalingGroup(self, "web_server_asg",
                                                    auto_scaling_group_name="web-server-asg",
                                                    launch_template=autoscaling.CfnAutoScalingGroup.LaunchTemplateSpecificationProperty(
                                                        version=web_server_template.attr_latest_version_number,
                                                        launch_template_name="web_server_template"
                                                    ),
                                                    new_instances_protected_from_scale_in=False,
                                                    availability_zones=[az1, az2],
                                                    vpc_zone_identifier=[subnet_01, subnet_02],
                                                    target_group_arns=[tg_arn],
                                                    max_size="3",
                                                    min_size="1",
                                                    desired_capacity="2"                                    
        )
        #Dynamic scaling: using target tracking policy to tracking the resources such as CPU, memory
        self.auto_scaling_action = autoscaling.CfnScalingPolicy(
            self, "MyAutoScalingPolicy",
            auto_scaling_group_name=self.web_server_asg.auto_scaling_group_name,
            policy_type="TargetTrackingScaling",
            target_tracking_configuration=autoscaling.CfnScalingPolicy.TargetTrackingConfigurationProperty(
                target_value=50,
                predefined_metric_specification=autoscaling.CfnScalingPolicy.PredefinedMetricSpecificationProperty(predefined_metric_type="ASGAverageCPUUtilization"),
                disable_scale_in=False
            ),

        )

        self.auto_scaling_action.node.add_dependency(self.web_server_asg)

        #Predictive scaling: scale in/out base on peak time

        #self.scale_out_scheduled_action = autoscaling.CfnScheduledAction(self, "MyScheduleActionScaleOut",
        #                                                        auto_scaling_group_name=self.web_server_asg.ref,
        #                                                        desired_capacity=2,
        #                                                        #end_time="2023-03-20T07:10:00Z",
        #                                                        max_size=3,
        #                                                        min_size=2,
        #                                                        recurrence="*/15 * * * *",
        #                                                        start_time="2023-03-26T12:15:00Z",
        #                                                        time_zone="UTC"
        #)
        #self.scale_in_scheduled_action = autoscaling.CfnScheduledAction(self, "MyScheduleActionScaleIn",
        #                                                        auto_scaling_group_name=self.web_server_asg.ref,
        #                                                        desired_capacity=1,
        #                                                        #end_time="endTime",
        #                                                        max_size=3,
        #                                                        min_size=1,
        #                                                        recurrence="*/5 * * * *",
        #                                                        start_time="2023-03-26T12:30:00Z",
        #                                                        time_zone="UTC"
        #)                                                     