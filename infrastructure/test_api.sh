#!/bin/bash

# Test script for Events API

if [ -z "$1" ]; then
    echo "Usage: ./test_api.sh <API_URL>"
    echo "Example: ./test_api.sh https://abc123.lambda-url.us-east-1.on.aws/"
    exit 1
fi

API_URL="${1%/}"  # Remove trailing slash if present

echo "🧪 Testing Events API at: $API_URL"
echo ""

# Test 1: Health Check
echo "1️⃣  Testing health endpoint..."
curl -s "$API_URL/health" | jq '.'
echo ""

# Test 2: GET /events
echo "2️⃣  GET /events (list all events)..."
curl -s "$API_URL/events" | jq '.'
echo ""

# Test 3: GET /events?status=active
echo "3️⃣  GET /events?status=active (filter by status)..."
curl -s "$API_URL/events?status=active" | jq '.'
echo ""

# Test 4: POST /events (with custom eventId)
echo "4️⃣  POST /events (create event with custom ID)..."
EVENT_RESPONSE=$(curl -s -X POST "$API_URL/events" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2024-12-15",
    "eventId": "api-test-event-456",
    "organizer": "API Test Organizer",
    "description": "Testing API Gateway integration",
    "location": "API Test Location",
    "title": "API Gateway Test Event",
    "capacity": 200,
    "status": "active"
  }')

echo "$EVENT_RESPONSE" | jq '.'
EVENT_ID=$(echo "$EVENT_RESPONSE" | jq -r '.eventId')
echo ""

# Test 5: GET /events/{eventId}
echo "5️⃣  GET /events/api-test-event-456 (get specific event)..."
curl -s "$API_URL/events/api-test-event-456" | jq '.'
echo ""

# Test 6: PUT /events/{eventId}
echo "6️⃣  PUT /events/api-test-event-456 (update event)..."
curl -s -X PUT "$API_URL/events/api-test-event-456" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated API Gateway Test Event",
    "capacity": 250
  }' | jq '.'
echo ""

# Test 7: DELETE /events/{eventId}
echo "7️⃣  DELETE /events/api-test-event-456 (delete event)..."
curl -s -X DELETE "$API_URL/events/api-test-event-456" -w "\nHTTP Status: %{http_code}\n"
echo ""

# Additional Test: Create event with auto-generated ID
echo "8️⃣  POST /events (create event with auto-generated ID)..."
EVENT_RESPONSE2=$(curl -s -X POST "$API_URL/events" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tech Conference 2024",
    "description": "Annual technology conference featuring industry leaders",
    "date": "2024-12-15T09:00:00",
    "location": "Convention Center, San Francisco, CA",
    "capacity": 500,
    "organizer": "Tech Events Inc.",
    "status": "published"
  }')

echo "$EVENT_RESPONSE2" | jq '.'
EVENT_ID2=$(echo "$EVENT_RESPONSE2" | jq -r '.eventId')
echo ""

# Test 9: List with different filter
echo "9️⃣  GET /events?status=published (filter by published status)..."
curl -s "$API_URL/events?status=published" | jq '.'
echo ""

# Cleanup
echo "🧹 Cleaning up test event..."
curl -s -X DELETE "$API_URL/events/$EVENT_ID2" -w "\nHTTP Status: %{http_code}\n"
echo ""

echo "✅ All tests completed!"
echo ""
echo "📚 View API documentation at: ${API_URL}docs"
