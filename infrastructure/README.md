# Infrastructure

CDK Infrastructure as Code for deploying the backend application.

## Setup

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Useful Commands

* `cdk ls` - List all stacks
* `cdk synth` - Synthesize CloudFormation template
* `cdk deploy` - Deploy stack to AWS
* `cdk diff` - Compare deployed stack with current state
* `cdk destroy` - Remove stack from AWS

## First Time Setup

```bash
cdk bootstrap aws://ACCOUNT-NUMBER/REGION
```
