#!/bin/bash
echo "Starting the FastAPI server in the background..."
cd lane-api-gateway/python-api-gateway

killall uvicorn 2>/dev/null
uvicorn app.main:app --port 8081 > server_logs_fb.txt 2>&1 &
SERVER_PID=$!

echo "Waiting for server to boot..."
sleep 3

echo -e "\n\n==========================================="
echo "TEST 3: FEEDBACK REQUEST (EXPECT BACKGROUND PROCESSING)"
echo "==========================================="
curl -s -X POST "http://localhost:8081/v1/feedback" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer some_dummy_token" \
     -d '{"eventId": "event_123", "label": "SCAM", "sourceType": "SMS", "timestamp": "2026-04-16T12:00:00Z"}' | jq .

echo -e "\n\nWaiting 3 seconds for the Background Task"
sleep 3

echo "Server logs:"
cat server_logs_fb.txt

echo "Cleaning up..."
kill $SERVER_PID
