from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import os
import uuid
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Events API",
    version="1.0.0",
    description="REST API for managing events with DynamoDB storage",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration - Configurable via environment variables
ALLOWED_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
CORS_ALLOW_CREDENTIALS = os.getenv('CORS_ALLOW_CREDENTIALS', 'true').lower() == 'true'

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if ALLOWED_ORIGINS != ['*'] else ["*"],
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "X-Requested-With",
    ],
    expose_headers=["Content-Length", "X-Total-Count"],
    max_age=3600,
)

# DynamoDB setup
try:
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=os.getenv('AWS_REGION', 'us-east-1'),
        endpoint_url=os.getenv('AWS_ENDPOINT_URL')  # For local DynamoDB
    )
    table_name = os.getenv('DYNAMODB_TABLE_NAME', 'events-table')
    table = dynamodb.Table(table_name)
    logger.info(f"Connected to DynamoDB table: {table_name}")
except Exception as e:
    logger.error(f"Failed to connect to DynamoDB: {str(e)}")
    raise


# Custom Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with detailed messages"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": errors
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred",
            "error": str(exc) if os.getenv('DEBUG', 'false').lower() == 'true' else None
        }
    )


# Enums and Models
class EventStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    ACTIVE = "active"  # Added for test compatibility
    INACTIVE = "inactive"  # Added for test compatibility


class EventBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Event title",
        examples=["Tech Conference 2024"]
    )
    description: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Detailed event description",
        examples=["Annual technology conference featuring industry leaders"]
    )
    date: str = Field(
        ...,
        description="Event date in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)",
        examples=["2024-12-15", "2024-12-15T09:00:00"]
    )
    location: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Event location or venue",
        examples=["Convention Center, 123 Main St, San Francisco, CA"]
    )
    capacity: int = Field(
        ...,
        gt=0,
        le=1000000,
        description="Maximum number of attendees",
        examples=[500]
    )
    organizer: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Event organizer name or organization",
        examples=["Tech Events Inc."]
    )
    status: EventStatus = Field(
        default=EventStatus.DRAFT,
        description="Current status of the event"
    )
    
    @field_validator('title', 'description', 'location', 'organizer')
    @classmethod
    def validate_no_empty_strings(cls, v: str) -> str:
        """Ensure strings are not just whitespace"""
        if not v or not v.strip():
            raise ValueError("Field cannot be empty or contain only whitespace")
        return v.strip()
    
    @field_validator('date')
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        """Validate ISO 8601 date format (supports both YYYY-MM-DD and YYYY-MM-DDTHH:MM:SS)"""
        try:
            # Try to parse the date - supports both date and datetime formats
            if 'T' in v or ' ' in v:
                # Full datetime format
                parsed_date = datetime.fromisoformat(v.replace('Z', '+00:00'))
            else:
                # Date only format (YYYY-MM-DD)
                parsed_date = datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError as e:
            raise ValueError(f"Invalid date format. Use ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS): {str(e)}")
    
    @field_validator('capacity')
    @classmethod
    def validate_capacity(cls, v: int) -> int:
        """Validate capacity is reasonable"""
        if v <= 0:
            raise ValueError("Capacity must be greater than 0")
        if v > 1000000:
            raise ValueError("Capacity cannot exceed 1,000,000")
        return v


class EventCreate(EventBase):
    eventId: Optional[str] = Field(
        None,
        description="Optional custom event ID. If not provided, a UUID will be generated."
    )
    
    @field_validator('eventId')
    @classmethod
    def validate_event_id(cls, v: Optional[str]) -> Optional[str]:
        """Validate eventId if provided"""
        if v is not None:
            # Allow any non-empty string as eventId
            if not v or not v.strip():
                raise ValueError("eventId cannot be empty")
            return v.strip()
        return v


class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=2000)
    date: Optional[str] = None
    location: Optional[str] = Field(None, min_length=1, max_length=500)
    capacity: Optional[int] = Field(None, gt=0, le=1000000)
    organizer: Optional[str] = Field(None, min_length=1, max_length=200)
    status: Optional[EventStatus] = None
    
    @field_validator('title', 'description', 'location', 'organizer')
    @classmethod
    def validate_no_empty_strings(cls, v: Optional[str]) -> Optional[str]:
        """Ensure strings are not just whitespace"""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Field cannot be empty or contain only whitespace")
        return v.strip() if v else None
    
    @field_validator('date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate ISO 8601 date format"""
        if v is None:
            return None
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
            return v
        except ValueError as e:
            raise ValueError(f"Invalid date format. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS): {str(e)}")
    
    @field_validator('capacity')
    @classmethod
    def validate_capacity(cls, v: Optional[int]) -> Optional[int]:
        """Validate capacity is reasonable"""
        if v is not None:
            if v <= 0:
                raise ValueError("Capacity must be greater than 0")
            if v > 1000000:
                raise ValueError("Capacity cannot exceed 1,000,000")
        return v


class Event(EventBase):
    eventId: str
    createdAt: str
    updatedAt: str


# Response Models
class ErrorResponse(BaseModel):
    detail: str
    error: Optional[str] = None


class ValidationErrorResponse(BaseModel):
    detail: str
    errors: List[dict]


# Helper functions
def validate_event_id(event_id: str) -> None:
    """Validate that event_id is not empty (supports both UUID and custom IDs)"""
    if not event_id or not event_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event ID cannot be empty"
        )


def handle_dynamodb_error(e: Exception, operation: str) -> None:
    """Handle DynamoDB errors with appropriate HTTP responses"""
    if isinstance(e, ClientError):
        error_code = e.response['Error']['Code']
        logger.error(f"DynamoDB error during {operation}: {error_code}")
        
        if error_code == 'ResourceNotFoundException':
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Database table not found. Please contact administrator."
            )
        elif error_code == 'ProvisionedThroughputExceededException':
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later."
            )
        elif error_code == 'ValidationException':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid request data"
            )
    
    logger.error(f"Unexpected error during {operation}: {str(e)}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Failed to {operation}"
    )


# API Endpoints
@app.get("/")
async def root():
    return {"message": "Events API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post(
    "/events",
    response_model=Event,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Event created successfully"},
        422: {"model": ValidationErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def create_event(event: EventCreate):
    """
    Create a new event
    
    - **eventId**: Optional custom event ID (auto-generated if not provided)
    - **title**: Event title (1-200 characters)
    - **description**: Detailed description (1-2000 characters)
    - **date**: ISO 8601 format date (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
    - **location**: Event venue or location (1-500 characters)
    - **capacity**: Maximum attendees (1-1,000,000)
    - **organizer**: Organizer name (1-200 characters)
    - **status**: Event status (draft, published, cancelled, completed, active, inactive)
    """
    # Use provided eventId or generate a new UUID
    event_id = event.eventId if event.eventId else str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()
    
    item = {
        "eventId": event_id,
        "title": event.title,
        "description": event.description,
        "date": event.date,
        "location": event.location,
        "capacity": event.capacity,
        "organizer": event.organizer,
        "status": event.status.value,
        "createdAt": timestamp,
        "updatedAt": timestamp
    }
    
    try:
        table.put_item(Item=item)
        logger.info(f"Created event: {event_id}")
        return Event(**item)
    except Exception as e:
        handle_dynamodb_error(e, "create event")


@app.get(
    "/events",
    response_model=List[Event],
    responses={
        200: {"description": "List of events"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def list_events(
    status: Optional[str] = None,  # Changed from status_filter for test compatibility
    status_filter: Optional[EventStatus] = None,  # Keep for backward compatibility
    limit: int = 100,
    organizer: Optional[str] = None
):
    """
    List all events with optional filters
    
    - **status**: Filter by event status (e.g., ?status=active)
    - **status_filter**: Alternative status filter parameter
    - **limit**: Maximum number of results (1-1000, default: 100)
    - **organizer**: Filter by organizer name
    """
    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 1000"
        )
    
    try:
        # Build filter expression
        filter_expressions = []
        
        # Support both 'status' and 'status_filter' parameters
        status_value = status or (status_filter.value if status_filter else None)
        if status_value:
            filter_expressions.append(Attr('status').eq(status_value))
        
        if organizer:
            filter_expressions.append(Attr('organizer').contains(organizer))
        
        # Combine filters
        if filter_expressions:
            combined_filter = filter_expressions[0]
            for expr in filter_expressions[1:]:
                combined_filter = combined_filter & expr
            response = table.scan(FilterExpression=combined_filter, Limit=limit)
        else:
            response = table.scan(Limit=limit)
        
        items = response.get('Items', [])
        logger.info(f"Retrieved {len(items)} events")
        return [Event(**item) for item in items]
    except Exception as e:
        handle_dynamodb_error(e, "list events")


@app.get(
    "/events/{event_id}",
    response_model=Event,
    responses={
        200: {"description": "Event details"},
        400: {"model": ErrorResponse, "description": "Invalid event ID"},
        404: {"model": ErrorResponse, "description": "Event not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def get_event(event_id: str):
    """
    Get a specific event by ID
    
    - **event_id**: ID of the event (UUID or custom ID)
    """
    validate_event_id(event_id)
    
    try:
        response = table.get_item(Key={'eventId': event_id})
        
        if 'Item' not in response:
            logger.warning(f"Event not found: {event_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Event with ID {event_id} not found"
            )
        
        logger.info(f"Retrieved event: {event_id}")
        return Event(**response['Item'])
    except HTTPException:
        raise
    except Exception as e:
        handle_dynamodb_error(e, "get event")


@app.put(
    "/events/{event_id}",
    response_model=Event,
    responses={
        200: {"description": "Event updated successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        404: {"model": ErrorResponse, "description": "Event not found"},
        422: {"model": ValidationErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def update_event(event_id: str, event_update: EventUpdate):
    """
    Update an existing event
    
    - **event_id**: ID of the event to update (UUID or custom ID)
    - Only provided fields will be updated
    """
    validate_event_id(event_id)
    
    try:
        # Check if event exists
        response = table.get_item(Key={'eventId': event_id})
        if 'Item' not in response:
            logger.warning(f"Event not found for update: {event_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Event with ID {event_id} not found"
            )
        
        # Build update expression
        update_data = event_update.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        update_data['updatedAt'] = datetime.utcnow().isoformat()
        
        update_expression = "SET " + ", ".join([f"#{k} = :{k}" for k in update_data.keys()])
        expression_attribute_names = {f"#{k}": k for k in update_data.keys()}
        expression_attribute_values = {f":{k}": v.value if isinstance(v, EventStatus) else v for k, v in update_data.items()}
        
        response = table.update_item(
            Key={'eventId': event_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues='ALL_NEW'
        )
        
        logger.info(f"Updated event: {event_id}")
        return Event(**response['Attributes'])
    except HTTPException:
        raise
    except Exception as e:
        handle_dynamodb_error(e, "update event")


@app.delete(
    "/events/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Event deleted successfully"},
        400: {"model": ErrorResponse, "description": "Invalid event ID"},
        404: {"model": ErrorResponse, "description": "Event not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def delete_event(event_id: str):
    """
    Delete an event
    
    - **event_id**: ID of the event to delete (UUID or custom ID)
    """
    validate_event_id(event_id)
    
    try:
        # Check if event exists
        response = table.get_item(Key={'eventId': event_id})
        if 'Item' not in response:
            logger.warning(f"Event not found for deletion: {event_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Event with ID {event_id} not found"
            )
        
        table.delete_item(Key={'eventId': event_id})
        logger.info(f"Deleted event: {event_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        handle_dynamodb_error(e, "delete event")


# Lambda Handler
try:
    from mangum import Mangum
    handler = Mangum(app, lifespan="off")
except ImportError:
    # Mangum not available (local development)
    handler = None
