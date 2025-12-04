# Events API Backend

FastAPI REST API for managing events with DynamoDB storage.

## Features

- Full CRUD operations for events
- DynamoDB integration
- Input validation with Pydantic
- Auto-generated API documentation
- CORS support

## Event Properties

- `eventId`: Unique identifier (auto-generated UUID)
- `title`: Event title
- `description`: Event description
- `date`: Event date (ISO format)
- `location`: Event location
- `capacity`: Maximum number of attendees
- `organizer`: Event organizer name
- `status`: Event status (draft, published, cancelled, completed)
- `createdAt`: Creation timestamp
- `updatedAt`: Last update timestamp

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your AWS credentials and DynamoDB table name
```

4. Ensure DynamoDB table exists with `eventId` as the partition key

## Run

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000
API documentation at http://localhost:8000/docs

## API Endpoints

### Create Event
```
POST /events
```

### List Events
```
GET /events?status_filter=published&limit=100
```

### Get Event
```
GET /events/{event_id}
```

### Update Event
```
PUT /events/{event_id}
```

### Delete Event
```
DELETE /events/{event_id}
```

### Health Check
```
GET /health
```
