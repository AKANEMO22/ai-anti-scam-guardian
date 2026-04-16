#!/bin/bash
echo "Starting the FastAPI server in the background..."
cd lane-api-gateway/python-api-gateway

uvicorn app.main:app --port 8081 > server_logs.txt 2>&1 &
SERVER_PID=$!

echo "Waiting for server to boot..."
sleep 3

echo "Sending first request..."
curl -s -X POST "http://localhost:8000/v1/signals/analyze" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer some_dummy_token" \
     -d '{"sourceType": "SMS", "text": "URGENT: Your account has been suspended. Click here to verify: http://scam-link.com"}' | jq .

echo "Waiting 3 seconds..."
sleep 3

echo "Sending second request (should be a cache hit)..."
curl -s -X POST "http://localhost:8081/v1/signals/analyze" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer some_dummy_token" \
     -d '{"sourceType": "SMS", "text": "URGENT: Your account has been suspended. Click here to verify: http://scam-link.com"}' | jq .

echo "Server logs:"
cat server_logs.txt

echo "Cleaning up..."
kill $SERVER_PID
