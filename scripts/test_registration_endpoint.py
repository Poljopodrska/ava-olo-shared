#!/usr/bin/env python3
"""Test if registration endpoints are available"""
import requests

BASE_URL = "http://ava-olo-farmers-alb-82735690.us-east-1.elb.amazonaws.com"

print("Testing registration endpoints...")
print("=" * 50)

# Test version
response = requests.get(f"{BASE_URL}/version")
print(f"Version: {response.json().get('version', 'Unknown')}")

# Test registration status endpoint
print("\nTesting /api/v1/chat/registration/status...")
response = requests.get(f"{BASE_URL}/api/v1/chat/registration/status")
print(f"Status code: {response.status_code}")
if response.ok:
    print(f"Response: {response.json()}")

# Test registration page
print("\nTesting /auth/register/llm page...")
response = requests.get(f"{BASE_URL}/auth/register/llm")
print(f"Status code: {response.status_code}")
print(f"Page exists: {response.ok}")

# Test chat endpoint
print("\nTesting /api/v1/chat/message (dashboard)...")
response = requests.post(f"{BASE_URL}/api/v1/chat/message", 
                        json={"content": "test"})
print(f"Status code: {response.status_code}")

# Test registration chat endpoint
print("\nTesting /api/v1/chat/registration/message...")
response = requests.post(f"{BASE_URL}/api/v1/chat/registration/message", 
                        json={"content": "test"})
print(f"Status code: {response.status_code}")
if response.ok:
    print(f"Response: {response.json()}")