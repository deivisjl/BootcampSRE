```
181.189.139.191
```

```
https://master.dacggukoi2967.amplifyapp.com/
```

```
https://bootcamp-institute-labs.awsapps.com/start/
```

```
export CODEARTIFACT_AUTH_TOKEN=`aws codeartifact get-authorization-token --domain lab-web-java --domain-owner 437257457257 --region us-east-2 --query authorizationToken --output text`
```
```
echo $'<settings>\n</settings>' > settings.xml
```
```
<servers>
  <server>
    <id>lab-web-java-lab-java-web</id>
    <username>aws</username>
    <password>${env.CODEARTIFACT_AUTH_TOKEN}</password>
  </server>
</servers>
```

```
<profiles>
  <profile>
    <id>lab-web-java-lab-java-web</id>
    <activation>
      <activeByDefault>true</activeByDefault>
    </activation>
    <repositories>
      <repository>
        <id>lab-web-java-lab-java-web</id>
        <url>https://lab-web-java-437257457257.d.codeartifact.us-east-2.amazonaws.com/maven/lab-java-web/</url>
      </repository>
    </repositories>
  </profile>
</profiles>
```

```
<mirrors>
  <mirror>
    <id>lab-web-java-lab-java-web</id>
    <name>lab-web-java-lab-java-web</name>
    <url>https://lab-web-java-437257457257.d.codeartifact.us-east-2.amazonaws.com/maven/lab-java-web/</url>
    <mirrorOf>*</mirrorOf>
  </mirror>
</mirrors>
```