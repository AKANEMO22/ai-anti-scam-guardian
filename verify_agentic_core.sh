#!/bin/bash
curl -X POST "http://localhost:8101/v1/agentic/score" -H "Content-Type: application/json" -d '{"sourceType": "SMS", "text": "Tin nhan tu me: Hom nay ve an com nhe con.", "metadata": {}}' | jq
