#!/usr/bin/env python3
import requests
import json

# Fetch the website
response = requests.get('https://cosmetic-alena.com')
print("Status Code:", response.status_code)
print("\n=== HTML CONTENT ===\n")
print(response.text)
