# Deployment Checklist ✅

Use this checklist to ensure a smooth deployment of your Events API.

## Pre-Deployment Checklist

### 1. Prerequisites Installed
- [ ] AWS CLI installed (`aws --version`)
- [ ] AWS credentials configured (`aws sts get-caller-identity`)
- [ ] Docker installed and running (`docker ps`)
- [ ] Node.js installed (`node --version`)
- [ ] Python 3.11+ installed (`python3 --version`)

### 2. AWS Account Setup
- [ ] AWS account created
- [ ] IAM user with appropriate permissions
- [ ] Access Key ID and Secret Access Key obtained
- [ ] Default region selected (e.g., us-east-1)

### 3. Project Files Ready
- [ ] All files downloaded/cloned
- [ ] Scripts are executable (`chmod +x infrastructure/*.sh`)
- [ ] Requirements files present

## Deployment Steps

### Step 1: Verify Prerequisites
```bash
# Check AWS
aws sts get-caller-identity

# Check Docker
docker ps

# Check Node.js
node --version

# Check Python
python3 --version
```
- [ ] All commands successful

### Step 2: Review Configuration
- [ ] Review `infrastructure/stacks/backend_stack.py`
- [ ] Check CORS settings (default: allow all origins)
- [ ] Verify region setting (default: us-east-1)
- [ ] Review Lambda memory/timeout settings

### Step 3: Deploy
```bash
cd infrastructure
./deploy.sh
```
- [ ] Deployment started
- [ ] No errors during build
- [ ] Stack deployed successfully
- [ ] Outputs displayed

### Step 4: Save Outputs
Copy these from deployment output:
- [ ] API URL: `_______________________________`
- [ ] API Docs URL: `_______________________________`
- [ ] Table Name: `_______________________________`
- [ ] Lambda Function Name: `_______________________________`

### Step 5: Test Deployment
```bash
# Replace with your actual URL
export API_URL="YOUR-FUNCTION-URL"

# Quick test
curl $API_URL/health

# Full test
./test_api.sh $API_URL
```
- [ ] Health check returns `{"status":"healthy"}`
- [ ] Can create event
- [ ] Can list events
- [ ] Can get event by ID
- [ ] Can update event
- [ ] Can delete event

### Step 6: Verify Documentation
- [ ] Open `YOUR-URL/docs` in browser
- [ ] Swagger UI loads correctly
- [ ] Can test endpoints from UI
- [ ] All endpoints visible

## Post-Deployment Checklist

### 1. Monitoring Setup
- [ ] CloudWatch logs accessible
- [ ] Can view Lambda metrics
- [ ] DynamoDB table visible in console

### 2. Documentation
- [ ] API URL documented
- [ ] Shared with team members
- [ ] Added to project documentation

### 3. Security Review
- [ ] CORS origins appropriate for environment
- [ ] No sensitive data in logs
- [ ] IAM permissions reviewed
- [ ] Consider adding authentication

### 4. Cost Monitoring
- [ ] AWS Cost Explorer enabled
- [ ] Budget alerts set up (optional)
- [ ] Free tier usage tracked

## Production Readiness Checklist

Before going to production:

### Security
- [ ] CORS restricted to specific domains
- [ ] Authentication implemented (Cognito/API Key)
- [ ] WAF configured for DDoS protection
- [ ] SSL/TLS certificate verified
- [ ] Rate limiting configured
- [ ] Input validation tested thoroughly

### Performance
- [ ] Load testing completed
- [ ] Lambda memory optimized
- [ ] DynamoDB capacity planned
- [ ] Cold start times acceptable
- [ ] Response times measured

### Monitoring
- [ ] CloudWatch alarms configured
- [ ] Error rate alerts set up
- [ ] Cost alerts configured
- [ ] Log retention policy set
- [ ] X-Ray tracing enabled (optional)

### Backup & Recovery
- [ ] DynamoDB point-in-time recovery enabled
- [ ] Backup strategy documented
- [ ] Disaster recovery plan created
- [ ] Data retention policy defined

### Documentation
- [ ] API documentation complete
- [ ] Deployment process documented
- [ ] Troubleshooting guide created
- [ ] Team trained on operations

### Compliance
- [ ] Data privacy requirements met
- [ ] GDPR compliance verified (if applicable)
- [ ] Data residency requirements met
- [ ] Audit logging enabled

## Troubleshooting Checklist

If deployment fails:

### Docker Issues
- [ ] Docker daemon running
- [ ] Docker has internet access
- [ ] Sufficient disk space

### AWS Issues
- [ ] Credentials valid
- [ ] Correct region selected
- [ ] IAM permissions sufficient
- [ ] Service quotas not exceeded

### CDK Issues
- [ ] CDK CLI installed globally
- [ ] CDK bootstrapped in account/region
- [ ] Python dependencies installed
- [ ] No syntax errors in stack code

### Lambda Issues
- [ ] Function deployed successfully
- [ ] Environment variables set correctly
- [ ] IAM role has DynamoDB permissions
- [ ] Function URL created

### DynamoDB Issues
- [ ] Table created successfully
- [ ] Correct partition key (eventId)
- [ ] Billing mode set correctly
- [ ] Region matches Lambda

## Verification Commands

```bash
# Check stack status
aws cloudformation describe-stacks --stack-name BackendStack

# Check Lambda function
aws lambda get-function --function-name YOUR-FUNCTION-NAME

# Check DynamoDB table
aws dynamodb describe-table --table-name events-table

# View recent logs
aws logs tail /aws/lambda/YOUR-FUNCTION-NAME --since 10m

# Test API
curl YOUR-API-URL/health
```

## Success Criteria

Your deployment is successful when:
- [ ] All API endpoints respond correctly
- [ ] Can create, read, update, and delete events
- [ ] API documentation accessible
- [ ] CloudWatch logs showing requests
- [ ] No errors in Lambda logs
- [ ] DynamoDB table contains test data
- [ ] Response times acceptable (<1s)

## Next Steps After Deployment

1. **Immediate**
   - [ ] Test all endpoints thoroughly
   - [ ] Share API URL with team
   - [ ] Document any issues

2. **Short Term (1 week)**
   - [ ] Monitor usage and costs
   - [ ] Optimize Lambda memory if needed
   - [ ] Set up monitoring alerts
   - [ ] Configure custom domain (optional)

3. **Medium Term (1 month)**
   - [ ] Review security settings
   - [ ] Implement authentication
   - [ ] Set up CI/CD pipeline
   - [ ] Add integration tests

4. **Long Term (3 months)**
   - [ ] Review and optimize costs
   - [ ] Implement advanced features
   - [ ] Scale based on usage
   - [ ] Plan multi-region deployment

## Support Resources

- **Quick Start**: `infrastructure/QUICKSTART.md`
- **Full Guide**: `infrastructure/DEPLOYMENT.md`
- **Commands**: `DEPLOY_COMMANDS.md`
- **Configuration**: `backend/CONFIGURATION.md`
- **Summary**: `PROJECT_SUMMARY.md`

## Emergency Rollback

If you need to rollback:

```bash
# Destroy the stack
cd infrastructure
cdk destroy

# Or rollback to previous version
aws cloudformation rollback-stack --stack-name BackendStack
```

## Contact & Support

- AWS Support: https://console.aws.amazon.com/support/
- FastAPI Docs: https://fastapi.tiangolo.com/
- CDK Docs: https://docs.aws.amazon.com/cdk/

---

## Quick Deploy Command

```bash
cd infrastructure && ./deploy.sh
```

**Estimated Time**: 5 minutes
**Estimated Cost**: $0-5/month

---

**Ready to deploy?** Start with Step 1 above! 🚀
