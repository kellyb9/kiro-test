#!/usr/bin/env python3
"""
Test script to verify API endpoints match the test requirements
"""
import requests
import json
import sys

def test_api(base_url):
    """Test API against specific endpoint requirements"""
    
    # Remove trailing slash
    base_url = base_url.rstrip('/')
    
    print("🧪 Testing Events API Endpoints\n")
    print(f"Base URL: {base_url}\n")
    
    results = []
    
    # Test 1: GET /events
    print("1️⃣  GET /events")
    try:
        response = requests.get(f"{base_url}/events")
        status_ok = response.status_code == 200
        results.append(("GET /events", status_ok, response.status_code, 200))
        print(f"   Status: {response.status_code} {'✅' if status_ok else '❌ Expected 200'}")
        print(f"   Response: {response.json()[:2] if isinstance(response.json(), list) else response.json()}\n")
    except Exception as e:
        results.append(("GET /events", False, str(e), 200))
        print(f"   ❌ Error: {e}\n")
    
    # Test 2: GET /events?status=active
    print("2️⃣  GET /events?status=active")
    try:
        response = requests.get(f"{base_url}/events?status=active")
        status_ok = response.status_code == 200
        results.append(("GET /events?status=active", status_ok, response.status_code, 200))
        print(f"   Status: {response.status_code} {'✅' if status_ok else '❌ Expected 200'}")
        print(f"   Response: {response.json()}\n")
    except Exception as e:
        results.append(("GET /events?status=active", False, str(e), 200))
        print(f"   ❌ Error: {e}\n")
    
    # Test 3: POST /events
    print("3️⃣  POST /events")
    event_data = {
        "date": "2024-12-15",
        "eventId": "api-test-event-456",
        "organizer": "API Test Organizer",
        "description": "Testing API Gateway integration",
        "location": "API Test Location",
        "title": "API Gateway Test Event",
        "capacity": 200,
        "status": "active"
    }
    try:
        response = requests.post(
            f"{base_url}/events",
            json=event_data,
            headers={"Content-Type": "application/json"}
        )
        status_ok = response.status_code == 201
        has_event_id = "eventId" in response.json() if response.status_code == 201 else False
        results.append(("POST /events", status_ok and has_event_id, response.status_code, 201))
        print(f"   Status: {response.status_code} {'✅' if status_ok else '❌ Expected 201'}")
        print(f"   Has eventId: {'✅' if has_event_id else '❌'}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
    except Exception as e:
        results.append(("POST /events", False, str(e), 201))
        print(f"   ❌ Error: {e}\n")
    
    # Test 4: GET /events/api-test-event-456
    print("4️⃣  GET /events/api-test-event-456")
    try:
        response = requests.get(f"{base_url}/events/api-test-event-456")
        status_ok = response.status_code == 200
        results.append(("GET /events/api-test-event-456", status_ok, response.status_code, 200))
        print(f"   Status: {response.status_code} {'✅' if status_ok else '❌ Expected 200'}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
    except Exception as e:
        results.append(("GET /events/api-test-event-456", False, str(e), 200))
        print(f"   ❌ Error: {e}\n")
    
    # Test 5: PUT /events/api-test-event-456
    print("5️⃣  PUT /events/api-test-event-456")
    update_data = {
        "title": "Updated API Gateway Test Event",
        "capacity": 250
    }
    try:
        response = requests.put(
            f"{base_url}/events/api-test-event-456",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        status_ok = response.status_code == 200
        results.append(("PUT /events/api-test-event-456", status_ok, response.status_code, 200))
        print(f"   Status: {response.status_code} {'✅' if status_ok else '❌ Expected 200'}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
    except Exception as e:
        results.append(("PUT /events/api-test-event-456", False, str(e), 200))
        print(f"   ❌ Error: {e}\n")
    
    # Test 6: DELETE /events/api-test-event-456
    print("6️⃣  DELETE /events/api-test-event-456")
    try:
        response = requests.delete(f"{base_url}/events/api-test-event-456")
        status_ok = response.status_code in [200, 204]
        results.append(("DELETE /events/api-test-event-456", status_ok, response.status_code, "200 or 204"))
        print(f"   Status: {response.status_code} {'✅' if status_ok else '❌ Expected 200 or 204'}\n")
    except Exception as e:
        results.append(("DELETE /events/api-test-event-456", False, str(e), "200 or 204"))
        print(f"   ❌ Error: {e}\n")
    
    # Summary
    print("=" * 70)
    print("📊 Test Summary\n")
    passed = sum(1 for _, success, _, _ in results if success)
    total = len(results)
    
    for endpoint, success, actual, expected in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {endpoint}")
        if not success:
            print(f"       Expected: {expected}, Got: {actual}")
    
    print(f"\n{'='*70}")
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_endpoints.py <API_URL>")
        print("Example: python test_endpoints.py https://abc123.lambda-url.us-east-1.on.aws")
        sys.exit(1)
    
    api_url = sys.argv[1]
    exit_code = test_api(api_url)
    sys.exit(exit_code)
