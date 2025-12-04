# Deployment Guide

This guide will help you deploy the Events API to AWS using serverless technologies.

## Architecture

The deployment uses:
- **AWS Lambda**: Serverless compute for the FastAPI application
- **Lambda Function URL**: Public HTTPS endpoint (simpler than API Gateway)
- **DynamoDB**: NoSQL database for event storage
- **CloudWatch Logs**: Application logging

## Prerequisites

1. **AWS Account**: You need an active AWS account
2. **AWS CLI**: Install and configure with your credentials
   ```bash
   aws configure
   ```
3. **Python 3.11+**: Required for CDK
4. **Node.js**: Required for AWS CDK CLI
5. **Docker**: Required for bundling Lambda dependencies

## Installation

### 1. Install AWS CDK CLI
```bash
npm install -g aws-cdk
```

### 2. Install Python Dependencies
```bash
cd infrastructure
pip install -r requirements.txt
```

## Deployment Steps

### Quick Deploy (Automated)
```bash
cd infrastructure
chmod +x deploy.sh
./deploy.sh
```

### Manual Deploy

1. **Bootstrap CDK** (only needed once per account/region)
   ```bash
   cd infrastructure
   cdk bootstrap
   ```

2. **Synthesize CloudFormation Template**
   ```bash
   cdk synth
   ```

3. **Deploy to AWS**
   ```bash
   cdk deploy
   ```

4. **Get Your API URL**
   After deployment, the output will show:
   - `ApiUrl`: Your public API endpoint
   - `ApiDocsUrl`: Interactive API documentation
   - `TableName`: DynamoDB table name
   - `LambdaFunctionName`: Lambda function name

## Post-Deployment

### Test Your API

1. **Health Check**
   ```bash
   curl https://YOUR-FUNCTION-URL/health
   ```

2. **Create an Event**
   ```bash
   curl -X POST https://YOUR-FUNCTION-URL/events \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Tech Conference 2024",
       "description": "Annual technology conference",
       "date": "2024-12-15T09:00:00",
       "location": "San Francisco, CA",
       "capacity": 500,
       "organizer": "Tech Events Inc.",
       "status": "published"
     }'
   ```

3. **List Events**
   ```bash
   curl https://YOUR-FUNCTION-URL/events
   ```

4. **View API Documentation**
   Open `https://YOUR-FUNCTION-URL/docs` in your browser

## Configuration

### Environment Variables

The Lambda function is configured with:
- `DYNAMODB_TABLE_NAME`: events-table
- `AWS_REGION`: Your deployment region
- `CORS_ORIGINS`: * (all origins allowed)
- `CORS_ALLOW_CREDENTIALS`: false
- `DEBUG`: false

To modify these, edit `infrastructure/stacks/backend_stack.py`:
```python
environment={
    "DYNAMODB_TABLE_NAME": events_table.table_name,
    "CORS_ORIGINS": "https://yourdomain.com",  # Change this
    "DEBUG": "false",
}
```

Then redeploy:
```bash
cdk deploy
```

## Monitoring

### View Logs
```bash
# Get function name from deployment output
aws logs tail /aws/lambda/YOUR-FUNCTION-NAME --follow
```

### CloudWatch Dashboard
1. Go to AWS Console → CloudWatch
2. Navigate to Log Groups
3. Find `/aws/lambda/BackendStack-EventsApiFunction...`

## Cost Estimation

With AWS Free Tier:
- **Lambda**: 1M requests/month free, then $0.20 per 1M requests
- **DynamoDB**: 25GB storage free, pay-per-request pricing
- **CloudWatch Logs**: 5GB ingestion free

Estimated cost for moderate usage: **$0-5/month**

## Updating the API

1. Make changes to `backend/main.py`
2. Redeploy:
   ```bash
   cd infrastructure
   cdk deploy
   ```

The deployment will automatically:
- Bundle new dependencies
- Update Lambda function
- Maintain the same Function URL

## Cleanup

To remove all resources:
```bash
cd infrastructure
cdk destroy
```

**Warning**: This will delete the DynamoDB table and all data!

## Troubleshooting

### Deployment Fails
- Ensure Docker is running (needed for bundling)
- Check AWS credentials: `aws sts get-caller-identity`
- Verify CDK is bootstrapped: `cdk bootstrap`

### API Returns 500 Error
- Check Lambda logs: `aws logs tail /aws/lambda/YOUR-FUNCTION-NAME`
- Verify DynamoDB table exists
- Check IAM permissions

### CORS Issues
- Update `CORS_ORIGINS` in `backend_stack.py`
- Redeploy the stack

## Security Recommendations

For production:
1. **Restrict CORS origins** to your domain
2. **Add authentication** (API Gateway with Cognito or Lambda authorizer)
3. **Enable WAF** for DDoS protection
4. **Use custom domain** with Route53 and CloudFront
5. **Enable DynamoDB encryption** at rest
6. **Set up CloudWatch alarms** for monitoring

## Next Steps

- Add authentication with AWS Cognito
- Set up custom domain with Route53
- Add CloudFront for caching
- Implement CI/CD with GitHub Actions
- Add monitoring and alerting
