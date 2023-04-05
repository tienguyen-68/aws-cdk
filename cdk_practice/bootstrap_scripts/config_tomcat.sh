#!/bin/bash
yum -y update
yum -y install java-1.8.0-openjdk
useradd -s /sbin/nologin tomcat
wget https://dlcdn.apache.org/tomcat/tomcat-8/v8.5.87/bin/apache-tomcat-8.5.87.tar.gz
tar -xvzf apache-tomcat-8.5.87.tar.gz
mv apache-tomcat-8.5.87 /opt/
cd /opt/apache-tomcat-8.5.87/conf/
mv server.xml server.xml.backup
cat <<EOF >> server.xml
<?xml version="1.0" encoding="UTF-8"?>

<Server port="8005" shutdown="SHUTDOWN">
  <Listener className="org.apache.catalina.startup.VersionLoggerListener" />
  <Listener className="org.apache.catalina.core.AprLifecycleListener" SSLEngine="on" />
  <Listener className="org.apache.catalina.core.JreMemoryLeakPreventionListener" />
  <Listener className="org.apache.catalina.mbeans.GlobalResourcesLifecycleListener" />
  <Listener className="org.apache.catalina.core.ThreadLocalLeakPreventionListener" />

  <GlobalNamingResources>
    <Resource name="UserDatabase" auth="Container"
              type="org.apache.catalina.UserDatabase"
              description="User database that can be updated and saved"
              factory="org.apache.catalina.users.MemoryUserDatabaseFactory"
              pathname="conf/tomcat-users.xml" />
  </GlobalNamingResources>

  <Service name="Catalina">

    <Connector port="80" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="443" />
     <Connector
           protocol="org.apache.coyote.http11.Http11NioProtocol"
           port="443" maxThreads="200"
           scheme="https" secure="true" SSLEnabled="true"
           keystoreFile="/opt/apache-tomcat-8.5.87/conf/keystore" keystorePass="changeit"
           clientAuth="false" sslProtocol="TLS"/>

    <Engine name="Catalina" defaultHost="localhost">
      <Realm className="org.apache.catalina.realm.LockOutRealm">
        <Realm className="org.apache.catalina.realm.UserDatabaseRealm"
               resourceName="UserDatabase"/>
      </Realm>

      <Host name="localhost"  appBase="webapps"
            unpackWARs="true" autoDeploy="true">

        <Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs"
               prefix="localhost_access_log" suffix=".txt"
               pattern="%h %l %u %t &quot;%r&quot; %s %b" />

      </Host>
    </Engine>
  </Service>
</Server>
EOF
echo -e "\nchangeit\nchangeit\ntest\ntest\ntest\ntest\ntest\ntest\nyes\n" | $JAVA_HOME/bin/keytool -genkey -alias tomcat -keyalg RSA -keystore keystore
cd ../webapps
mkdir helloworld
cat <<EOF >> helloworld/index.html
<html>
<body>
<div style="width: 100%; font-size: 40px; font-weight: bold; text-align: center;">
Test Page
</div>
</body>
</html>
EOF
chown -R tomcat:ec2-user /opt/apache-tomcat-8.5.87/
find /opt/ -type d -exec chmod 775 {} +
cd ../bin
./startup.sh

