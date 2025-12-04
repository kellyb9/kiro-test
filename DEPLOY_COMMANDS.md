# Deployment Commands Reference

## Quick Deploy (Recommended)

```bash
cd infrastructure
./deploy.sh
```

## Manual Deployment Steps

### 1. Install Dependencies

```bash
# Install CDK CLI globally
npm install -g aws-cdk

# Install Python dependencies
cd infrastructure
pip install -r requirements.txt
```

### 2. Configure AWS

```bash
# Configure AWS credentials
aws configure

# Verify configuration
aws sts get-caller-identity
```

### 3. Bootstrap CDK (First Time Only)

```bash
cd infrastructure
cdk bootstrap
```

### 4. Deploy

```bash
# Preview changes
cdk diff

# Deploy to AWS
cdk deploy

# Deploy without confirmation prompts
cdk deploy --require-approval never
```

### 5. Get Outputs

```bash
# View stack outputs
aws cloudformation describe-stacks \
  --stack-name BackendStack \
  --query 'Stacks[0].Outputs'
```

## Testing Commands

### Test API Endpoint

```bash
# Set your API URL (from deployment output)
export API_URL="https://YOUR-FUNCTION-URL"

# Health check
curl $API_URL/health

# Run full test suite
cd infrastructure
./test_api.sh $API_URL
```

### Manual API Tests

```bash
# Create event
curl -X POST $API_URL/events \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Event",
    "description": "This is a test event",
    "date": "2024-12-31T18:00:00",
    "location": "Test Location",
    "capacity": 100,
    "organizer": "Test Organizer",
    "status": "draft"
  }'

# List events
curl $API_URL/events

# Get specific event
curl $API_URL/events/{EVENT_ID}

# Update event
curl -X PUT $API_URL/events/{EVENT_ID} \
  -H "Content-Type: application/json" \
  -d '{"status": "published"}'

# Delete event
curl -X DELETE $API_URL/events/{EVENT_ID}
```

## Monitoring Commands

### View Lambda Logs

```bash
# Get function name
aws lambda list-functions --query 'Functions[?contains(FunctionName, `EventsApi`)].FunctionName'

# Tail logs
aws logs tail /aws/lambda/YOUR-FUNCTION-NAME --follow

# View recent logs
aws logs tail /aws/lambda/YOUR-FUNCTION-NAME --since 1h
```

### Check DynamoDB Table

```bash
# Describe table
aws dynamodb describe-table --table-name events-table

# Scan table (list all items)
aws dynamodb scan --table-name events-table

# Get item count
aws dynamodb describe-table --table-name events-table \
  --query 'Table.ItemCount'
```

### Lambda Metrics

```bash
# Get function metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=YOUR-FUNCTION-NAME \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Sum
```

## Update Commands

### Update Lambda Code

```bash
cd infrastructure
cdk deploy
```

### Update Environment Variables

Edit `infrastructure/stacks/backend_stack.py`, then:

```bash
cdk deploy
```

### Update Lambda Configuration

```bash
# Increase memory
aws lambda update-function-configuration \
  --function-name YOUR-FUNCTION-NAME \
  --memory-size 1024

# Increase timeout
aws lambda update-function-configuration \
  --function-name YOUR-FUNCTION-NAME \
  --timeout 60
```

## Cleanup Commands

### Destroy Stack

```bash
cd infrastructure
cdk destroy
```

### Manual Cleanup

```bash
# Delete Lambda function
aws lambda delete-function --function-name YOUR-FUNCTION-NAME

# Delete DynamoDB table
aws dynamodb delete-table --table-name events-table

# Delete CloudWatch logs
aws logs delete-log-group --log-group-name /aws/lambda/YOUR-FUNCTION-NAME
```

## Troubleshooting Commands

### Check CDK Version

```bash
cdk --version
```

### Check Docker

```bash
docker --version
docker ps
```

### Validate CDK App

```bash
cd infrastructure
cdk synth
```

### Check Stack Status

```bash
aws cloudformation describe-stacks --stack-name BackendStack
```

### View Stack Events

```bash
aws cloudformation describe-stack-events \
  --stack-name BackendStack \
  --max-items 20
```

### Test Lambda Locally

```bash
# Install SAM CLI
brew install aws-sam-cli

# Invoke function locally
sam local invoke -e test_event.json
```

## CI/CD Commands

### GitHub Actions Example

```yaml
- name: Deploy to AWS
  run: |
    cd infrastructure
    npm install -g aws-cdk
    pip install -r requirements.txt
    cdk deploy --require-approval never
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    AWS_DEFAULT_REGION: us-east-1
```

## Useful Aliases

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
# CDK shortcuts
alias cdkd='cdk deploy --require-approval never'
alias cdks='cdk synth'
alias cdkdiff='cdk diff'

# API testing
alias api-health='curl $API_URL/health'
alias api-events='curl $API_URL/events'

# Logs
alias api-logs='aws logs tail /aws/lambda/YOUR-FUNCTION-NAME --follow'
```

## Environment-Specific Deployments

### Development

```bash
cdk deploy --context environment=dev
```

### Production

```bash
cdk deploy --context environment=prod
```

## Backup Commands

### Backup DynamoDB

```bash
# Enable point-in-time recovery
aws dynamodb update-continuous-backups \
  --table-name events-table \
  --point-in-time-recovery-specification PointInTimeRecoveryEnabled=true

# Create on-demand backup
aws dynamodb create-backup \
  --table-name events-table \
  --backup-name events-backup-$(date +%Y%m%d)
```

### Export DynamoDB Data

```bash
# Export to S3
aws dynamodb export-table-to-point-in-time \
  --table-arn arn:aws:dynamodb:REGION:ACCOUNT:table/events-table \
  --s3-bucket YOUR-BUCKET \
  --export-format DYNAMODB_JSON
```

## Quick Reference

| Task | Command |
|------|---------|
| Deploy | `cd infrastructure && ./deploy.sh` |
| Test | `./test_api.sh $API_URL` |
| Logs | `aws logs tail /aws/lambda/FUNCTION --follow` |
| Update | `cdk deploy` |
| Destroy | `cdk destroy` |
| Docs | Open `$API_URL/docs` in browser |
