#!/bin/bash
curl -X POST "http://localhost:8101/v1/agentic/score" -H "Content-Type: application/json" -d '{"sourceType": "SMS", "text": "Tin nhan vcb: tai khoan se bi khoa, xin vao link update.com", "metadata": {}}' | jq
