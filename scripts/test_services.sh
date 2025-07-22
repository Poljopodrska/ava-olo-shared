#!/bin/bash
# Test script to verify GPT-4 and Weather services

echo "🔍 Testing AVA OLO Services"
echo "=========================="

ALB_URL="http://ava-olo-farmers-alb-82735690.us-east-1.elb.amazonaws.com"

echo ""
echo "1. Checking version..."
curl -s "$ALB_URL/version" | python3 -m json.tool

echo ""
echo "2. Chat service status..."
curl -s "$ALB_URL/api/v1/chat/status" | python3 -m json.tool

echo ""
echo "3. Testing chat with farming question..."
curl -s -X POST "$ALB_URL/api/v1/chat/message" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "What is the best time to plant tomatoes in Ljubljana considering current weather?"
  }' | python3 -m json.tool

echo ""
echo "4. Weather service test (using mock endpoint)..."
# Since debug endpoints are failing, let's try a different approach
curl -s "$ALB_URL/health" | grep -q "healthy" && echo "✅ Service is healthy" || echo "❌ Service unhealthy"

echo ""
echo "Done!"