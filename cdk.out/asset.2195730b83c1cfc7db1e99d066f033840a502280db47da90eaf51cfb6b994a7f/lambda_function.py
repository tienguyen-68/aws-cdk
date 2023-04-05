import boto3
import botocore
import json
import time
import urllib

def lambda_handler(event, context):
    ssm = boto3.client('ssm')
    ec2 = boto3.client('ec2')
    s3 = boto3.client('s3')

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    Myec2 = ec2.describe_instances(
        Filters = [{
            'Name': 'tag:Name',
            'Values': ['webserver-01']
        }]
    )
    InstanceId = []

    for i in Myec2["Reservations"]:
        for instance in i["Instances"]:
            if instance["State"]["Name"] == "running":
                InstanceId.append(instance["InstanceId"])
    
    command =  "sudo -s; mv /opt/apache-tomcat-8.5.87/webapps/lambda_function.zip /opt/apache-tomcat-8.5.87/webapps/lambda_function.zip.bak; aws s3 cp s3://demo-bucket-123456789-bee0c5402c5/lambda_function.zip /opt/apache-tomcat-8.5.87/webapps/; unzip -d /opt/apache-tomcat-8.5.87/webapps/ /opt/apache-tomcat-8.5.87/webapps/lambda_function.zip /opt/apache-tomcat-8.5.87/webapps/; ls -l /opt/apache-tomcat-8.5.87/webapps/lambda_function*"
    for instanceid in InstanceId:            
        response = ssm.send_command(
                    InstanceIds=[instanceid],
                    DocumentName='AWS-RunShellScript',
                    Parameters={
                        'commands': [command]
                    }
        )
        
        command_id = response["Command"]["CommandId"]
        
        time.sleep(3)
        #test lambda
        output = ssm.get_command_invocation(CommandId=command_id, InstanceId=instanceid)
        print(output)