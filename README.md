# Events API

A serverless REST API for managing events, built with FastAPI and deployed on AWS Lambda.

## Features

- ✅ Full CRUD operations for events
- ✅ DynamoDB storage with pay-per-request pricing
- ✅ Serverless deployment (Lambda + Function URL)
- ✅ Comprehensive input validation
- ✅ CORS support for web applications
- ✅ Auto-generated API documentation
- ✅ Production-ready error handling

## Quick Start

### Deploy to AWS (5 minutes)

```bash
# 1. Configure AWS credentials
aws configure

# 2. Deploy the API
cd infrastructure
chmod +x deploy.sh
./deploy.sh
```

Your API will be live with a public HTTPS endpoint!

### Test the API

```bash
# Get your API URL from deployment output
cd infrastructure
chmod +x test_api.sh
./test_api.sh https://YOUR-FUNCTION-URL
```

## Project Structure

```
.
├── backend/              # FastAPI application
│   ├── main.py          # API implementation
│   ├── requirements.txt # Python dependencies
│   └── README.md        # Backend documentation
│
└── infrastructure/       # AWS CDK deployment
    ├── stacks/          # CDK stack definitions
    ├── deploy.sh        # Deployment script
    ├── test_api.sh      # API testing script
    └── DEPLOYMENT.md    # Deployment guide
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/events` | Create event |
| GET | `/events` | List events |
| GET | `/events/{id}` | Get event |
| PUT | `/events/{id}` | Update event |
| DELETE | `/events/{id}` | Delete event |
| GET | `/docs` | API documentation |

## Event Schema

```json
{
  "eventId": "string (UUID or custom ID)",
  "title": "string (1-200 chars)",
  "description": "string (1-2000 chars)",
  "date": "ISO 8601 date or datetime (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)",
  "location": "string (1-500 chars)",
  "capacity": "integer (1-1,000,000)",
  "organizer": "string (1-200 chars)",
  "status": "draft|published|cancelled|completed|active|inactive",
  "createdAt": "ISO 8601 datetime",
  "updatedAt": "ISO 8601 datetime"
}
```

### Example with Custom Event ID
```json
{
  "eventId": "api-test-event-456",
  "title": "API Gateway Test Event",
  "description": "Testing API Gateway integration",
  "date": "2024-12-15",
  "location": "API Test Location",
  "capacity": 200,
  "organizer": "API Test Organizer",
  "status": "active",
  "createdAt": "2024-12-03T10:30:00.000000",
  "updatedAt": "2024-12-03T10:30:00.000000"
}
```

## Local Development

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables
export DYNAMODB_TABLE_NAME=events-table
export AWS_REGION=us-east-1

# Run locally
uvicorn main:app --reload
```

Visit http://localhost:8000/docs for API documentation.

## Documentation

- [Backend Documentation](backend/README.md)
- [Deployment Guide](infrastructure/DEPLOYMENT.md)
- [Configuration Guide](backend/CONFIGURATION.md)

## Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────────────┐
│  Lambda Function    │
│  (FastAPI + Mangum) │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  DynamoDB Table     │
│  (events-table)     │
└─────────────────────┘
```

## Cost

With AWS Free Tier:
- Lambda: 1M requests/month free
- DynamoDB: 25GB storage free
- Estimated: **$0-5/month** for moderate usage

## Security

- CORS configurable per environment
- Input validation on all fields
- UUID validation for event IDs
- Structured error responses
- CloudWatch logging enabled

## Next Steps

- [ ] Add authentication (Cognito)
- [ ] Set up custom domain
- [ ] Add CI/CD pipeline
- [ ] Implement rate limiting
- [ ] Add monitoring/alerting

## License

MIT
