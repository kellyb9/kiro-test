# API Test Requirements

This document outlines the specific endpoint requirements that the API must satisfy.

## Test Endpoints

### 1. GET /events
- **Expected Status**: 200
- **Description**: List all events
- **Response**: Array of event objects

### 2. GET /events?status=active
- **Expected Status**: 200
- **Description**: List events filtered by status
- **Query Parameter**: `status=active`
- **Response**: Array of event objects with status "active"

### 3. POST /events
- **Expected Status**: 201
- **Description**: Create a new event
- **Required Response Keys**: `eventId`
- **Request Body**:
```json
{
  "date": "2024-12-15",
  "eventId": "api-test-event-456",
  "organizer": "API Test Organizer",
  "description": "Testing API Gateway integration",
  "location": "API Test Location",
  "title": "API Gateway Test Event",
  "capacity": 200,
  "status": "active"
}
```

### 4. GET /events/api-test-event-456
- **Expected Status**: 200
- **Description**: Get a specific event by ID
- **Path Parameter**: `api-test-event-456`
- **Response**: Single event object

### 5. PUT /events/api-test-event-456
- **Expected Status**: 200
- **Description**: Update an existing event
- **Path Parameter**: `api-test-event-456`
- **Request Body**:
```json
{
  "title": "Updated API Gateway Test Event",
  "capacity": 250
}
```

### 6. DELETE /events/api-test-event-456
- **Expected Status**: 200 or 204
- **Description**: Delete an event
- **Path Parameter**: `api-test-event-456`

## Key Requirements

### Event ID Support
- ✅ Support custom event IDs (client-provided)
- ✅ Support auto-generated UUIDs (when not provided)
- ✅ Event ID can be any string format

### Status Values
- ✅ Support "active" status
- ✅ Support "inactive" status
- ✅ Support "draft", "published", "cancelled", "completed" (original)

### Date Format
- ✅ Support "YYYY-MM-DD" format (e.g., "2024-12-15")
- ✅ Support "YYYY-MM-DDTHH:MM:SS" format (e.g., "2024-12-15T09:00:00")

### Query Parameters
- ✅ Support `?status=active` for filtering
- ✅ Support `?status_filter=published` for backward compatibility

### Response Codes
- ✅ 200 for successful GET, PUT
- ✅ 201 for successful POST
- ✅ 204 for successful DELETE (or 200)
- ✅ 404 for not found
- ✅ 422 for validation errors

## Implementation Changes

### 1. EventStatus Enum
Added new status values:
```python
class EventStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    ACTIVE = "active"      # New
    INACTIVE = "inactive"  # New
```

### 2. EventCreate Model
Added optional eventId field:
```python
class EventCreate(EventBase):
    eventId: Optional[str] = Field(
        None,
        description="Optional custom event ID"
    )
```

### 3. Date Validation
Updated to support both formats:
```python
# Supports both:
# - "2024-12-15"
# - "2024-12-15T09:00:00"
```

### 4. List Events Endpoint
Added `status` query parameter:
```python
async def list_events(
    status: Optional[str] = None,           # New
    status_filter: Optional[EventStatus] = None,  # Backward compatible
    ...
)
```

### 5. Event ID Validation
Changed from UUID-only to any string:
```python
def validate_event_id(event_id: str) -> None:
    """Validate that event_id is not empty"""
    # Accepts any non-empty string
```

## Testing

### Automated Test Script
```bash
# Python test script (comprehensive)
python backend/test_endpoints.py https://YOUR-API-URL

# Bash test script (quick)
./infrastructure/test_api.sh https://YOUR-API-URL
```

### Manual Testing
Use the interactive API documentation:
```
https://YOUR-API-URL/docs
```

### Test Scenarios

#### Scenario 1: Custom Event ID
```bash
curl -X POST https://YOUR-API-URL/events \
  -H "Content-Type: application/json" \
  -d '{
    "eventId": "my-custom-id-123",
    "title": "Test Event",
    "description": "Test Description",
    "date": "2024-12-15",
    "location": "Test Location",
    "capacity": 100,
    "organizer": "Test Organizer",
    "status": "active"
  }'
```

#### Scenario 2: Auto-Generated ID
```bash
curl -X POST https://YOUR-API-URL/events \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Event",
    "description": "Test Description",
    "date": "2024-12-15",
    "location": "Test Location",
    "capacity": 100,
    "organizer": "Test Organizer",
    "status": "active"
  }'
```

#### Scenario 3: Filter by Status
```bash
# Using 'status' parameter
curl https://YOUR-API-URL/events?status=active

# Using 'status_filter' parameter (backward compatible)
curl https://YOUR-API-URL/events?status_filter=published
```

#### Scenario 4: Different Date Formats
```bash
# Date only
"date": "2024-12-15"

# Date with time
"date": "2024-12-15T09:00:00"
```

## Validation Rules

### Required Fields
- title (1-200 chars)
- description (1-2000 chars)
- date (ISO 8601 format)
- location (1-500 chars)
- capacity (1-1,000,000)
- organizer (1-200 chars)
- status (valid enum value)

### Optional Fields
- eventId (auto-generated if not provided)

### Constraints
- All string fields: no whitespace-only values
- Capacity: must be positive integer
- Date: must be valid ISO 8601 format
- Status: must be valid enum value

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Event ID cannot be empty"
}
```

### 404 Not Found
```json
{
  "detail": "Event with ID {id} not found"
}
```

### 422 Validation Error
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

## Compatibility

### Backward Compatibility
The API maintains backward compatibility:
- ✅ Old status values still work (draft, published, etc.)
- ✅ Auto-generated UUIDs still work
- ✅ `status_filter` parameter still works
- ✅ Full datetime format still works

### New Features
- ✅ Custom event IDs
- ✅ "active" and "inactive" status values
- ✅ Simple date format (YYYY-MM-DD)
- ✅ `status` query parameter

## Deployment

After updating the code, redeploy:
```bash
cd infrastructure
cdk deploy
```

The same API URL will serve the updated code with all new features!
