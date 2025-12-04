#!/bin/bash

# Deployment script for Events API

set -e

echo "🚀 Deploying Events API to AWS..."

# Check if AWS credentials are configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Please run 'aws configure' first."
    exit 1
fi

# Install CDK dependencies
echo "📦 Installing CDK dependencies..."
pip install -r requirements.txt

# Bootstrap CDK (only needed once per account/region)
echo "🔧 Bootstrapping CDK (if needed)..."
cdk bootstrap || true

# Synthesize CloudFormation template
echo "🔨 Synthesizing CloudFormation template..."
cdk synth

# Deploy the stack
echo "☁️  Deploying to AWS..."
cdk deploy --require-approval never

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📝 Your API endpoints:"
cdk output BackendStack.ApiUrl
echo ""
echo "📚 API Documentation:"
cdk output BackendStack.ApiDocsUrl
echo ""
echo "🎉 Your Events API is now live!"
