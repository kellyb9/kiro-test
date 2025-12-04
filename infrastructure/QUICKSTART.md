# Quick Start - Deploy in 5 Minutes

## Prerequisites Check

```bash
# Check AWS CLI
aws --version

# Check credentials
aws sts get-caller-identity

# Check Docker (required for bundling)
docker --version

# Check Node.js (for CDK)
node --version
```

## One-Command Deploy

```bash
cd infrastructure && ./deploy.sh
```

That's it! The script will:
1. Install CDK dependencies
2. Bootstrap CDK (if needed)
3. Build and deploy your API
4. Output your public API URL

## Expected Output

```
✅ Deployment complete!

📝 Your API endpoints:
https://abc123xyz.lambda-url.us-east-1.on.aws/

📚 API Documentation:
https://abc123xyz.lambda-url.us-east-1.on.aws/docs

🎉 Your Events API is now live!
```

## Test Your API

```bash
# Save your API URL
export API_URL="https://YOUR-FUNCTION-URL"

# Quick test
curl $API_URL/health

# Full test suite
./test_api.sh $API_URL
```

## View API Documentation

Open in browser:
```
https://YOUR-FUNCTION-URL/docs
```

## Common Issues

### "AWS credentials not configured"
```bash
aws configure
# Enter your AWS Access Key ID and Secret Access Key
```

### "Docker not running"
```bash
# Start Docker Desktop or Docker daemon
```

### "CDK not found"
```bash
npm install -g aws-cdk
```

## What Gets Deployed?

- **Lambda Function**: Your FastAPI application
- **DynamoDB Table**: `events-table` for data storage
- **Function URL**: Public HTTPS endpoint
- **CloudWatch Logs**: Automatic logging

## Cost

Free Tier eligible:
- First 1M Lambda requests/month: FREE
- First 25GB DynamoDB storage: FREE
- Typical cost: $0-5/month

## Update Your API

After making changes to `backend/main.py`:

```bash
cd infrastructure
cdk deploy
```

Same URL, updated code!

## Cleanup

Remove all resources:

```bash
cd infrastructure
cdk destroy
```

## Next Steps

1. Test your API with the test script
2. View the interactive docs at `/docs`
3. Integrate with your frontend
4. Configure CORS for your domain
5. Add authentication (optional)

## Support

- [Full Deployment Guide](DEPLOYMENT.md)
- [Backend Documentation](../backend/README.md)
- [Configuration Guide](../backend/CONFIGURATION.md)
