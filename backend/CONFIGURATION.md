# Configuration Guide

## Environment Variables

### AWS Configuration

- `AWS_REGION`: AWS region for DynamoDB (default: `us-east-1`)
- `AWS_ACCESS_KEY_ID`: AWS access key ID
- `AWS_SECRET_ACCESS_KEY`: AWS secret access key
- `AWS_ENDPOINT_URL`: Optional endpoint URL for local DynamoDB development

### DynamoDB Configuration

- `DYNAMODB_TABLE_NAME`: Name of the DynamoDB table (default: `events-table`)

### CORS Configuration

The API supports configurable CORS settings for secure web access:

- `CORS_ORIGINS`: Comma-separated list of allowed origins
  - Use `*` to allow all origins (not recommended for production)
  - Example: `http://localhost:3000,https://myapp.com`
  - Default: `*`

- `CORS_ALLOW_CREDENTIALS`: Allow credentials in CORS requests
  - Set to `true` or `false`
  - Default: `true`

### Debug Configuration

- `DEBUG`: Enable detailed error messages
  - Set to `true` or `false`
  - Default: `false`
  - **Warning**: Only enable in development environments

## CORS Best Practices

### Development Environment
```bash
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8080
CORS_ALLOW_CREDENTIALS=true
```

### Production Environment
```bash
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CORS_ALLOW_CREDENTIALS=true
DEBUG=false
```

### Public API (No Authentication)
```bash
CORS_ORIGINS=*
CORS_ALLOW_CREDENTIALS=false
```

## Security Considerations

1. **Never use `CORS_ORIGINS=*` with `CORS_ALLOW_CREDENTIALS=true` in production**
2. **Always specify exact origins in production**
3. **Keep `DEBUG=false` in production**
4. **Use HTTPS in production**
5. **Rotate AWS credentials regularly**
6. **Use IAM roles instead of access keys when possible**

## Input Validation

The API includes comprehensive validation:

### Field Validation
- **Title**: 1-200 characters, no empty strings
- **Description**: 1-2000 characters, no empty strings
- **Date**: ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
- **Location**: 1-500 characters, no empty strings
- **Capacity**: 1-1,000,000 attendees
- **Organizer**: 1-200 characters, no empty strings
- **Status**: Must be one of: draft, published, cancelled, completed

### UUID Validation
- Event IDs must be valid UUIDs
- Invalid UUIDs return 400 Bad Request

### Request Validation
- Empty or whitespace-only strings are rejected
- Invalid date formats are rejected
- Out-of-range values are rejected
- Detailed error messages indicate which fields failed validation

## Error Handling

The API provides structured error responses:

### Validation Errors (422)
```json
{
  "detail": "Validation error",
  "errors": [
    {
      "field": "capacity",
      "message": "Capacity must be greater than 0",
      "type": "value_error"
    }
  ]
}
```

### Not Found (404)
```json
{
  "detail": "Event with ID {event_id} not found"
}
```

### Bad Request (400)
```json
{
  "detail": "Invalid event ID format: {event_id}"
}
```

### Server Error (500)
```json
{
  "detail": "Failed to create event",
  "error": "Detailed error message (only in DEBUG mode)"
}
```

## Logging

The API logs important events:
- Event creation, updates, and deletions
- Database connection status
- Errors and warnings
- Request validation failures

Log level can be configured via Python's logging module.

## Rate Limiting

DynamoDB throttling is handled gracefully:
- Returns 429 Too Many Requests when throughput is exceeded
- Includes appropriate error messages
- Logs throttling events for monitoring
