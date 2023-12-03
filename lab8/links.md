
```
https://master.d1gwcaa5r1vc49.amplifyapp.com/tarea-4/
```

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install 
. ~/.bashrc
```

```
AWS_REGION="us-east-1"
aws configure set default.region ${AWS_REGION}
```
```
aws configure get default.region
```
```
aws sts get-caller-identity
```
```
curl -L "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
```
```
eksctl version
```
```
sudo curl -L -o /usr/local/bin/kubectl https://s3.us-west-2.amazonaws.com/amazon-eks/1.24.9/2023-01-11/bin/linux/amd64/kubectl
sudo chmod +x /usr/local/bin/kubectl
```
```
kubectl version --short --client
```
```
AWS_REGION=$(aws configure get default.region)
eksctl create cluster \
  --name=ekshandson \
  --version 1.24 \
  --nodes=3 --managed \
  --region ${AWS_REGION} --zones ${AWS_REGION}a,${AWS_REGION}c
```
```
sudo yum -y install jq bash-completion
```
```
sudo curl -L -o /etc/bash_completion.d/docker https://raw.githubusercontent.com/docker/cli/master/contrib/completion/bash/docker
```
```
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
```
```
kubectl completion bash > kubectl_completion
sudo mv kubectl_completion /etc/bash_completion.d/kubectl
```
```
eksctl completion bash > eksctl_completion
sudo mv eksctl_completion /etc/bash_completion.d/eksctl
```
```
cat <<"EOT" >> ${HOME}/.bashrc
```
```
alias k="kubectl"
complete -o default -F __start_kubectl k
EOT
```
```
git clone https://github.com/jonmosco/kube-ps1.git ~/.kube-ps1
cat <<"EOT" >> ~/.bashrc
```
```
source ~/.kube-ps1/kube-ps1.sh
function get_cluster_short() {
  echo "$1" | cut -d . -f1
}
KUBE_PS1_CLUSTER_FUNCTION=get_cluster_short
KUBE_PS1_SUFFIX=') '
PS1='$(kube_ps1)'$PS1
EOT
```
```
git clone https://github.com/ahmetb/kubectx.git ~/.kubectx
sudo ln -sf ~/.kubectx/completion/kubens.bash /etc/bash_completion.d/kubens
sudo ln -sf ~/.kubectx/completion/kubectx.bash /etc/bash_completion.d/kubectx
cat <<"EOT" >> ~/.bashrc
```
```
export PATH=~/.kubectx:$PATH
EOT
```
```
curl -L "https://github.com/stern/stern/releases/download/v1.22.0/stern_1.22.0_linux_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/stern /usr/local/bin
```
```
. ~/.bashrc
. /etc/profile.d/bash_completion.sh
. /etc/bash_completion.d/kubectl
. /etc/bash_completion.d/eksctl
```
```
eksctl get cluster
```
```
kubectl cluster-info
```
```
kubectl get node
```
```
kubectl describe node
```
```
kubectl get namespace
```
```
kubectl get pod -n kube-system
```
```
kubens kube-system
```
```
kubectl get pod -A
```
```
kubectl get pod -n kube-system -o wide
```
```
POD_NAME=aws-node-5h5tw
```
```
echo $POD_NAME
```
```
kubectl describe pod -n kube-system ${POD_NAME}
```
```
kubectl get pod -n kube-system ${POD_NAME} -o yaml
```
```
kubectl get pod -n kube-system ${POD_NAME} -o json | jq
```
```
jmespath
```
```
kubectl get pod -n kube-system ${POD_NAME} -o jsonpath='{.metadata.name}'
```
```
kubectl get service -A
kubectl get deployment -A
kubectl get daemonset -A
```
```
kubectl get all -A
```
```
frontend_repo=$(aws ecr describe-repositories --repository-names frontend-eks --query 'repositories[0].repositoryUri' --output text)
```
```
aws ecr create-repository --repository-name backend
```
```
backend_repo=$(aws ecr describe-repositories --repository-names backend --query 'repositories[0].repositoryUri' --output text)
```
```
docker tag frontend:latest ${frontend_repo}:latest
```
```
docker push ${frontend_repo}:latest
```
```
mkdir -p ~/environment/manifests/
cd ~/environment/manifests/
```
```
kubens frontend
```
```
eksctl utils associate-iam-oidc-provider \
    --cluster ekshandson \
    --approve
```
```
kubectl delete pod --all -n backend
```

