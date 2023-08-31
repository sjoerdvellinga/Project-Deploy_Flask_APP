# Deploying a Flask API

This is the project starter repo for the course Server Deployment, Containerization, and Testing.

The URL to access this app is: http://a2ad2651a34104216acec007c697b443-234112474.us-east-2.elb.amazonaws.com/

The Flask app that will be used for this project consists of a simple API with four endpoints:

- `GET '/'`: This is a simple health check, which returns the response 'Still Healthy!'. 
- `POST '/auth'`: This takes a email and password as json arguments and returns a JWT based on a custom secret.
- `GET '/contents'`: This requires a valid JWT, and returns the un-encrpyted contents of that token. 
- `GET '/me'`: This is a simple JSON code, which returns the response 'with the app name and it's age since it was pushed into the pipeline.

The app relies on a secret set as the environment variable `JWT_SECRET` to produce a JWT. The built-in Flask server is adequate for local development, but not production, so you will be using the production-ready [Gunicorn](https://gunicorn.org/) server when deploying the app.


## Prerequisites to boot the app
1.  Attach policy to IAM role
      $  aws iam put-role-policy --role-name projectCodeBuildRole --policy-name eks-describe --policy-document file://iam-role-policy.json
2.  Check Authorization
      $  kubectl get -n kube-system configmap/aws-auth -o yaml > /tmp/aws-auth-patch.yml
      Open in VS Code:
        $  code /System/Volumes/Data/private/tmp/aws-auth-patch.yml
        Result shall include:
          rolearn: arn:aws:iam::<ACCOUNT ID>:role/eksctl-projectDeployEKS-nodegroup-NodeInstanceRole-1LQA157O81MN2
        If this result is not included in the response, add a group in the aws-auth-patch and push it to AWS
          put command: $  aws iam put-role-policy --role-name UdacityFlaskDeployCBKubectlRole --policy-name eks-describe --policy-document file://iam-role-policy.json
3.  Save JWTsecret in AWS
      command: $  aws ssm put-parameter --name JWT_SECRET --overwrite --value "myjwtsecret" --type SecureString
      Verify command: aws ssm get-parameter --name JWT_SECRET

## Launch
1. Create an EKS Cluster
      command: $  eksctl create cluster --name projectDeployEKS --nodes=2 --version=1.27 --instance-types=t2.medium --region=us-east-2
2. Create a stack
      command: $  aws cloudformation create-stack  --stack-name deployEksCodeBuild --region us-east-1 --template-body file://ci-cd-codepipeline.cfn.yml --parameters ParameterKey=GitHubToken,ParameterValue=<GITHUB_TOKEN>
2. Health Check
    Check createed Cluster
      command: $  eksctl get cluster --name=projectDeployEKS --region=us-east-2 
      alternative command: $  eksctl utils describe-stacks --region=us-east-2 --cluster=projectDeployEKS 
    Check created stacks
      cmmand: $  aws cloudformation list-stacks
    Check pods 
      command: $  kubectl get nodes


## Termination after the project
1. Delete the cluster
      Command: $  eksctl delete cluster projectDeployEKS  --region=us-east-2
2. Stop local container
    Get running <container ID>
      Command: $  docker ps
    Stop Container
      Command: $  docker stop <container ID>
3.  Delete JWTsecret from AWS
      command: $  aws ssm delete-parameter --name JWT_SECRET




## Project Prerequisites given by Udacity

* Docker Desktop - Installation instructions for all OSes can be found <a href="https://docs.docker.com/install/" target="_blank">here</a>.
* Git: <a href="https://git-scm.com/downloads" target="_blank">Download and install Git</a> for your system. 
* Code editor: You can <a href="https://code.visualstudio.com/download" target="_blank">download and install VS code</a> here.
* AWS Account
* Python version between 3.7 and 3.9. Check the current version using:
```bash
#  Mac/Linux/Windows 
python --version
```
You can download a specific release version from <a href="https://www.python.org/downloads/" target="_blank">here</a>.

* Python package manager - PIP 19.x or higher. PIP is already installed in Python 3 >=3.4 downloaded from python.org . However, you can upgrade to a specific version, say 20.2.3, using the command:
```bash
#  Mac/Linux/Windows Check the current version
pip --version
# Mac/Linux
pip install --upgrade pip==20.2.3
# Windows
python -m pip install --upgrade pip==20.2.3
```
* Terminal
   * Mac/Linux users can use the default terminal.
   * Windows users can use either the GitBash terminal or WSL. 
* Command line utilities:
  * AWS CLI installed and configured using the `aws configure` command. Another important configuration is the region. Do not use the us-east-1 because the cluster creation may fails mostly in us-east-1. Let's change the default region to:
  ```bash
  aws configure set region us-east-2  
  ```
  Ensure to create all your resources in a single region. 
  * EKSCTL installed in your system. Follow the instructions [available here](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html#installing-eksctl) or <a href="https://eksctl.io/introduction/#installation" target="_blank">here</a> to download and install `eksctl` utility. 
  * The KUBECTL installed in your system. Installation instructions for kubectl can be found <a href="https://kubernetes.io/docs/tasks/tools/install-kubectl/" target="_blank">here</a>. 


## Initial setup

1. Fork the <a href="https://github.com/udacity/cd0157-Server-Deployment-and-Containerization" target="_blank">Server and Deployment Containerization Github repo</a> to your Github account.
1. Locally clone your forked version to begin working on the project.
```bash
git clone https://github.com/SudKul/cd0157-Server-Deployment-and-Containerization.git
cd cd0157-Server-Deployment-and-Containerization/
```
1. These are the files relevant for the current project:
```bash
.
├── Dockerfile 
├── README.md
├── aws-auth-patch.yml
├── buildspec.yml
├── ci-cd-codepipeline.cfn.yml
├── iam-role-policy.json
├── main.py
├── requirements.txt
├── simple_jwt_api.yml
├── test_main.py
└── trust.json 
```

     
## Project Steps

Completing the project involved the following steps:

1. Write a Dockerfile for a simple Flask API
2. Build and test the container locally
3. Create an EKS cluster
4. Store a secret using AWS Parameter Store
5. Create a CodePipeline pipeline triggered by GitHub checkins
6. Create a CodeBuild stage which will build, test, and deploy your code