```
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-imageid
```

```
https://us-east-2.console.aws.amazon.com/cloudformation/home?region=us-east-2#/
```

```
https://master.d3ocjyrujmx34n.amplifyapp.com/
```

```
wget https://s3.amazonaws.com/labs.bootcamp.institute/bootcamp-sre-aws/archivos-laboratorios/templates.zip
```
```
https://docs.aws.amazon.com/es_es/vpc/
```
```
aws cloudformation create-stack --stack-name Lab1 --parameters ParameterKey=InstanceType,ParameterValue=t2.micro --template-body file://lab1.yaml
```
```
cfn-lint
```
aws cloudformation describe-stack-resource-drifts --stack-name Lab1 --stack-resource-drift-status-filters MODIFIED DELETED
```
### Enviar las modificaciones del yml
```
aws cloudformation create-change-set --stack-name Lab1 --change-set-name Lab1ChangeSet --parameters ParameterKey=InstanceType,ParameterValue=t2.micro --template-body file://lab1.yaml

## Realizar rollback
```
aws cloudformation create-change-set --stack-name Lab1 --change-set-name Lab2ChangeSet --parameters ParameterKey=InstanceType,ParameterValue=t2.micro --template-body file://lab1.yaml
```
```
https://docs.aws.amazon.com/cli/latest/reference/cloudformation/
```

```
https://docs.aws.amazon.com/cli/latest/reference/cloudformation/execute-change-set.html
```
```
aws cloudformation delete-stack --stack-name Lab1
```
```
aws cloudformation describe-stacks --stack-name Lab1
```
### NAMING SE
```
https://docs.aws.amazon.com/es_es/AmazonS3/latest/userguide/bucketnamingrules.html
```
### CREATE STACK
```
aws cloudformation create-stack --stack-name Lab1S3 --template-body file://s3.yaml
```

```
aws cloudformation create-stack --stack-name Lab1S3 --template-body file://s3.yaml --parameters ParameterKey=Environment,ParameterValue=test
```
### UPDATE STACK
```
aws cloudformation update-stack --stack-name Lab1S3 --template-body file://s3.yaml
```
### DESCRIBE STACK
```
aws cloudformation describe-stacks --stack-name Lab1S3
```

```
aws cloudformation describe-stack-events --stack-name Lab1S3
```
### DESTROY STACK
```
aws cloudformation delete-stack --stack-name Lab1S3
```
### TAREA
```
Tarea:Crear una plantilla de Cloudformation parar crear un Bucket de S3
```

```https://grabaciones-bootcamp-institute.s3.amazonaws.com/+231007-CLOUD-SRE-AWS/+231007-CLOUD-SRE-AWS-14-OCT.mp4

```
