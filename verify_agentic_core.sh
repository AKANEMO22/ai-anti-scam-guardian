#!/bin/bash
curl -X POST "http://localhost:8101/v1/agentic/score" -H "Content-Type: application/json" -d '{"sourceType": "SMS", "text": "Chuc mung! Ban da trung thuong 1 ty dong tu VCB. Vui long nhan vao link https://vcb-qua-tang.com de nhan thuong ngay.", "metadata": {}}' | jq
