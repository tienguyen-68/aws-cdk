#!/bin/bash
yum -y update
yum -y install java-1.8.0-openjdk
useradd tomcat
wget https://dlcdn.apache.org/tomcat/tomcat-8/v8.5.87/bin/apache-tomcat-8.5.87.tar.gz
tar -xvzf apache-tomcat-8.5.87.tar.gz
mv apache-tomcat-8.5.87 /opt/
cd /opt/apache-tomcat-8.5.87/conf/
mv server.xml server.xml.backup
mkdir /home/tomcat/.ssh/
chmod 700 /home/tomcat/.ssh/
cat <<EOF >> /home/tomcat/.ssh/webserver.pem
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAlyauZBS4T/eYLcgn+ajrq4+e4DyP4veRJClQZnDZy+HwEwkh
dRZkaNrktPgWpGarwR5yKP4RRXVK2vCk/+yFR5j8sLvW9PqJQUib1mhGKH+rXvd3
DYz6J4YEIzsx68Yoas8BD81/Vn+ssxMa7thlI9vcz19MRA0S3wtiiKagUk0YkhA8
1b1jcFblUadgbR4+m94Vzy5IJ3Smq8SNxIjgwd/TNvtnegiNyy+JMYcipJHc4kdz
nee4gJfCN2MpjbgA1xtZHfnO9IQSogvOh7ZhNycqVuQaDTvBCnbOasn+FcGvO4YY
wLtKXD//Z+9p24UTyzNK4I5Ev7R1drKyOEA1gQIDAQABAoIBABewQT6AHM6zkA8E
wncXKTAvBwg/lZFNmVqgevBDGW8hjr18/dha1Qu12ogeJXZIfPx8KAoSn2RSWJPt
iP5u9AhfiqKsHakxJperqHi2yOAJ+jKc9/SQtpfBIh7fZRh9atIqdREj9KP6yHcc
NGlgUqGHEJkTZ2F25xE7uIqQCqo7GfiTsMpKkxHXj7jW8RsJeDn25PU3mbhCnGc7
Ea0fO3zN5AvrOmbPQujst33VQrCccs57fBem+FPGg1FUrZBd5UnrTQLZwzTGI2/b
W8yyZm6gmsqNjVwGzVdNr9v9R4/v8y8vvha88kAO/N43wgNm2K/eICQI1EhYoZqm
m6VHAQECgYEA8cChwJoPubVz/UQa9V6t3hO3OB6NoYwaxrnJ4MA9RBvVBLeyMQiw
rr8g9vjpn4vcUZMTyBUp+JT4YEo0Cd8erF/PnpK5Sg+9Q3MfvJ+um1lQ3PU607+L
MpYHuRtttEWAPUgDn1BlRYBubkScLo36RzvuklwQj5VO+8O6DFyRXtECgYEAoA8g
1g/G89IAJ2BObqVkgaVPfrMhiYX7hNM15h044N29OGGk08pbcUZW/dTl+smR/cof
V5wbJHjsfyq5Dw5lvqYwacJ9jtM+/X5DFxB6WQuZAJwmjC1u68UKCPr8yeU0VO+G
CB6urQZCWjL8sBhoE7OQMSxbzWmulI+MV+Wi97ECgYBIZ1UKhhmnmPzAIaGhU1Xn
aSg6mov4kimC0ynvMiQnPd6ypwGrRdsEuyF4VlxB+HVnyRDnn88OMC+jRxYGztg0
8A0ShQcRc11P0i7zIy/8PufFBX005e0enWh6vAhDMX2S3PqYwE9UXX61b78HAmau
5vgwxXoARst9A8W45hBzwQKBgDEdM0g8QyJiGCX9CVQucC7QGRqZwPrAIDPb07gu
01s872kznS5X88NIgD0XbRKNc7zans91WWbRrFBBPdP+6P2dZVGumnSPIc8LRW74
YXKdem+Tesic0GKMbc3fpl4VdP9zGD+5moQBXa7r4lnuw1D4UpCkOe9INIflnH0E
PAOhAoGBAMjpYVjJiLm7ajhs3tem18OsKXQIFbA+sWSqXvIWmeQJwAvJo+PBlGrw
Rm3kUaKjMHWb0hGPus0PagIvAvHGgYBvgklFOhG729S8pV0FfJLvXwGFlHux2/sw
tHa2ao+qra7ZPE1lH3L7i3+OWcOI6FfaEvDHazS3SAnEx4ZbXXFD
-----END RSA PRIVATE KEY-----
EOF
cat <<EOF >> /home/tomcat/.ssh/config
Host *
    StrictHostKeyChecking no
EOF
chmod 600 /home/tomcat/.ssh/webserver.pem
rsync -e "ssh -i /home/tomcat/.ssh/webserver.pem -o StrictHostKeyChecking=no" -avP ec2-user@10.0.0.34:/opt/apache-tomcat-8.5.87/ /opt/apache-tomcat-8.5.87/
chown -R tomcat:tomcat /opt/apache-tomcat-8.5.87/webapps/
cd /opt/apache-tomcat-8.5.87/bin
./startup.sh