# pre-build
Note:
import SSL to ALB: import by manual because of there is no module support.

keypair: create by manual because of there is no module support.

Setup
I'm using python 3.11

To manualy create a virtualenv on MacOS and Linux:
```
$ git clone git@github.com:tienguyen-68/aws-cdk.git
$ cd aws-cdk
$ python3 -m venv .env
```
After the init process completes and the virtualenv is created, you can use the following step to activate your virtualenv.
```
$ source .env/bin/activate
```
If you are a Windows platform, you would activate the virtualenv like this:
```
% .env\Scripts\activate.bat
```
Once the virtualenv is activated, you can install the required dependencies.
```
$ pip install -r requirements.txt
```
Install the latest version of the AWS CDK CLI:
```
$ npm i -g aws-cdk
```
# Build


Step 1: Before deploy stack, we need to create keypair after then attach to ec2 and import self-cert into ACM to configure ALB https listener.

Step 2:


replace keyname value that have just created in cdk.json

replace private key in bootstrap_script/config_tomcat_asg.sh

replace certificate_arn value in cdk.json


Step 3: Deploy VPC stack, Security Group Stack, EC2 stack
```
cdk ls
cdk bootstrap
cdk diff MyEC2Stack MyVpcStack MySgStack 
cdk synth
cdk deploy MyEC2Stack MyVpcStack MySgStack
```
Step 4: try access Public IPv4 DNS with https/http to confirm the webserver work correctly
```
ec2-x-x-x-x.ap-southeast-1.compute.amazonaws.com/helloworld

https://ec2-x-x-x-x.ap-southeast-1.compute.amazonaws.com/helloworld
```
Step 5: Deploy AutoScaling Stack, ALB Stack. 
2. Deploy AutoScaling Stack, ALB Stack.
```
cdk ls
cdk diff MyAsgStack MyAlbStack 
cdk synth
cdk deploy MyAsgStack MyAlbStack
```
Step 6: try access DNS name of ALB with https/http to confirm the webserver work correctly
```
webserver-alb-xxx.ap-southeast-1.elb.amazonaws.com/helloworld
```
Step 7: Deploy Lambda Function
```
cdk ls
cdk diff MyLambdaStack
cdk deploy MyLambdaStack
```
Step 8: Test lambda function 
```
#upload zip file to s3
cd cdk_practice/lambda
vi lambda_function.py
-> add any comment
zip lambda_function.zip lambda_function.py
cd -
cdk deploy MyLambdaStack

#check file zip in the /opt/apache-tomcat-8.5.87/webapps directory
ls -l /opt/apache-tomcat-8.5.87/webapps/lambda_function*

OR

#check log run_command history in SSM
```
