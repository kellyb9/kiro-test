# 🚀 Ready to Deploy!

Your Events API is ready for deployment to AWS. Here's everything you need to know.

## What You've Built

A production-ready serverless REST API with:
- ✅ FastAPI backend with full CRUD operations
- ✅ DynamoDB for scalable data storage
- ✅ AWS Lambda for serverless compute
- ✅ Public HTTPS endpoint via Lambda Function URL
- ✅ Comprehensive validation and error handling
- ✅ CORS support for web applications
- ✅ Auto-generated API documentation
- ✅ CloudWatch logging

## Deploy Now (5 Minutes)

### Step 1: Verify Prerequisites

```bash
# Check AWS credentials
aws sts get-caller-identity

# If not configured:
aws configure
```

### Step 2: Deploy

```bash
cd infrastructure
./deploy.sh
```

### Step 3: Test

```bash
# Use the URL from deployment output
./test_api.sh https://YOUR-FUNCTION-URL
```

### Step 4: View Documentation

Open in browser:
```
https://YOUR-FUNCTION-URL/docs
```

## What Happens During Deployment?

1. **CDK Bootstrap** (first time only)
   - Sets up CDK resources in your AWS account
   - Creates S3 bucket for deployment artifacts

2. **Build Phase**
   - Bundles FastAPI application
   - Installs dependencies (FastAPI, Mangum, boto3)
   - Creates deployment package

3. **Deploy Phase**
   - Creates DynamoDB table (`events-table`)
   - Deploys Lambda function
   - Creates Function URL (public endpoint)
   - Sets up IAM permissions
   - Configures CloudWatch logging

4. **Output**
   - Public API URL
   - API documentation URL
   - Resource names

## Example API Usage

### Create an Event
```bash
curl -X POST https://YOUR-URL/events \
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

### List Events
```bash
curl https://YOUR-URL/events
```

### Get Event
```bash
curl https://YOUR-URL/events/{event-id}
```

### Update Event
```bash
curl -X PUT https://YOUR-URL/events/{event-id} \
  -H "Content-Type: application/json" \
  -d '{"capacity": 750}'
```

### Delete Event
```bash
curl -X DELETE https://YOUR-URL/events/{event-id}
```

## Architecture

```
Internet
   │
   ▼
Lambda Function URL (HTTPS)
   │
   ▼
AWS Lambda
   │
   ├─► FastAPI Application
   │   └─► Mangum (ASGI adapter)
   │
   ▼
DynamoDB Table
   └─► events-table
```

## Cost Breakdown

### Free Tier (First 12 Months)
- Lambda: 1M requests/month FREE
- DynamoDB: 25GB storage FREE
- CloudWatch: 5GB logs FREE

### After Free Tier
- Lambda: $0.20 per 1M requests
- DynamoDB: Pay-per-request (~$1.25 per million writes)
- Typical monthly cost: **$0-5** for moderate usage

## Security Features

- ✅ HTTPS only (enforced by Lambda Function URL)
- ✅ Input validation on all fields
- ✅ UUID validation for event IDs
- ✅ Structured error responses (no sensitive data leaks)
- ✅ CloudWatch logging for audit trail
- ✅ IAM-based DynamoDB access (no hardcoded credentials)

## Configuration Options

Edit `infrastructure/stacks/backend_stack.py` to customize:

```python
environment={
    "CORS_ORIGINS": "https://yourdomain.com",  # Restrict origins
    "CORS_ALLOW_CREDENTIALS": "true",          # Enable credentials
    "DEBUG": "false",                          # Disable debug mode
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
aws logs tail /aws/lambda/BackendStack-EventsApiFunction... --follow
```

### CloudWatch Dashboard
1. AWS Console → CloudWatch
2. Log Groups → `/aws/lambda/BackendStack-EventsApiFunction...`
3. View real-time logs and metrics

## Troubleshooting

### Deployment fails with "Docker not found"
- Start Docker Desktop
- Verify: `docker ps`

### "AWS credentials not configured"
```bash
aws configure
# Enter Access Key ID and Secret Access Key
```

### API returns 500 error
```bash
# Check Lambda logs
aws logs tail /aws/lambda/YOUR-FUNCTION-NAME --follow
```

### CORS errors in browser
- Update `CORS_ORIGINS` in `backend_stack.py`
- Redeploy: `cdk deploy`

## Update Your API

After making changes:

```bash
cd infrastructure
cdk deploy
```

The same URL will serve your updated code!

## Cleanup

To remove all resources:

```bash
cd infrastructure
cdk destroy
```

⚠️ This deletes the DynamoDB table and all data!

## Production Checklist

Before going to production:

- [ ] Restrict CORS origins to your domain
- [ ] Add authentication (Cognito/API Key)
- [ ] Set up custom domain with Route53
- [ ] Enable DynamoDB backups
- [ ] Set up CloudWatch alarms
- [ ] Configure WAF for DDoS protection
- [ ] Review IAM permissions
- [ ] Enable X-Ray tracing
- [ ] Set up CI/CD pipeline

## Documentation

- [Quick Start Guide](infrastructure/QUICKSTART.md)
- [Full Deployment Guide](infrastructure/DEPLOYMENT.md)
- [Backend Documentation](backend/README.md)
- [Configuration Guide](backend/CONFIGURATION.md)

## Support Resources

- AWS Lambda Docs: https://docs.aws.amazon.com/lambda/
- FastAPI Docs: https://fastapi.tiangolo.com/
- AWS CDK Docs: https://docs.aws.amazon.com/cdk/

## Ready to Deploy?

```bash
cd infrastructure && ./deploy.sh
```

Your API will be live in ~5 minutes! 🎉
