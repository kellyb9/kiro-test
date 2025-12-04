# 🚀 START HERE - Events API Deployment

Welcome! This guide will get your Events API deployed to AWS in 5 minutes.

## What You're Deploying

A production-ready REST API for managing events with:
- ✅ FastAPI backend with full CRUD operations
- ✅ DynamoDB database (serverless, auto-scaling)
- ✅ AWS Lambda (serverless compute)
- ✅ Public HTTPS endpoint
- ✅ Auto-generated API documentation

## Prerequisites (2 minutes)

### 1. AWS Account
If you don't have one: https://aws.amazon.com/free/

### 2. Install AWS CLI
```bash
# macOS
brew install awscli

# Or download from: https://aws.amazon.com/cli/
```

### 3. Configure AWS Credentials
```bash
aws configure
```
Enter:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., `us-east-1`)
- Default output format (press Enter for default)

### 4. Verify Setup
```bash
aws sts get-caller-identity
```
Should show your AWS account info.

### 5. Ensure Docker is Running
```bash
docker ps
```
If not installed: https://www.docker.com/get-started/

## Deploy (3 minutes)

### One Command Deploy
```bash
cd infrastructure
./deploy.sh
```

That's it! The script will:
1. Install dependencies
2. Build your application
3. Deploy to AWS
4. Give you a public URL

### Expected Output
```
✅ Deployment complete!

📝 Your API endpoints:
https://abc123xyz.lambda-url.us-east-1.on.aws/

📚 API Documentation:
https://abc123xyz.lambda-url.us-east-1.on.aws/docs

🎉 Your Events API is now live!
```

## Test Your API (1 minute)

### Quick Test
```bash
# Replace with your actual URL
curl https://YOUR-URL/health
```

Should return: `{"status":"healthy"}`

### Full Test Suite
```bash
cd infrastructure
./test_api.sh https://YOUR-URL
```

### Interactive Documentation
Open in browser:
```
https://YOUR-URL/docs
```

Try creating an event directly from the Swagger UI!

## What's Next?

### Immediate
1. ✅ Test all endpoints
2. ✅ View API documentation
3. ✅ Share URL with your team

### This Week
- Configure CORS for your domain
- Add custom domain (optional)
- Set up monitoring alerts

### This Month
- Add authentication
- Set up CI/CD
- Implement advanced features

## API Quick Reference

### Create Event
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

## Troubleshooting

### "AWS credentials not configured"
```bash
aws configure
```

### "Docker not found"
Install Docker Desktop: https://www.docker.com/get-started/

### "CDK not found"
```bash
npm install -g aws-cdk
```

### Deployment fails
Check the logs and see [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

## Cost

Your API runs on AWS Free Tier:
- Lambda: 1M requests/month FREE
- DynamoDB: 25GB storage FREE
- Typical cost: **$0-5/month**

## Documentation

- **[README.md](README.md)** - Project overview
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Step-by-step guide
- **[DEPLOYMENT_READY.md](DEPLOYMENT_READY.md)** - Deployment details
- **[DEPLOY_COMMANDS.md](DEPLOY_COMMANDS.md)** - Command reference
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete summary
- **[infrastructure/QUICKSTART.md](infrastructure/QUICKSTART.md)** - Quick start
- **[backend/CONFIGURATION.md](backend/CONFIGURATION.md)** - Configuration

## Support

Need help?
1. Check [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
2. Review [infrastructure/DEPLOYMENT.md](infrastructure/DEPLOYMENT.md)
3. Check AWS CloudWatch logs
4. Review error messages carefully

## Update Your API

Made changes to the code?
```bash
cd infrastructure
cdk deploy
```

Same URL, updated code!

## Cleanup

To remove everything:
```bash
cd infrastructure
cdk destroy
```

⚠️ This deletes all data!

---

## Ready? Let's Deploy! 🚀

```bash
cd infrastructure && ./deploy.sh
```

Your API will be live in ~5 minutes!

---

## Architecture

```
┌─────────────┐
│   Client    │
│  (Browser)  │
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────────────┐
│  Lambda Function    │
│  URL (Public)       │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  AWS Lambda         │
│  (FastAPI + Mangum) │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  DynamoDB Table     │
│  (events-table)     │
└─────────────────────┘
```

## Features

- ✅ Full CRUD operations
- ✅ Input validation
- ✅ Error handling
- ✅ CORS support
- ✅ Auto-scaling
- ✅ Pay-per-use pricing
- ✅ CloudWatch logging
- ✅ API documentation
- ✅ Production-ready

## Event Properties

- `eventId` - Unique identifier (auto-generated)
- `title` - Event title
- `description` - Event description
- `date` - Event date (ISO 8601)
- `location` - Event location
- `capacity` - Maximum attendees
- `organizer` - Organizer name
- `status` - draft | published | cancelled | completed
- `createdAt` - Creation timestamp
- `updatedAt` - Last update timestamp

---

**Questions?** Check the documentation files listed above!

**Ready to deploy?** Run: `cd infrastructure && ./deploy.sh`
