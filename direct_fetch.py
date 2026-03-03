#!/usr/bin/env python3
"""
Direct website fetcher and analyzer for cosmetic-alena.com
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import sys
import os

def get_website():
    """Fetch and return website content"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print("Fetching https://cosmetic-alena.com...", file=sys.stderr)
        response = requests.get('https://cosmetic-alena.com', headers=headers, timeout=10)
        print(f"Status: {response.status_code}", file=sys.stderr)
        
        if response.status_code == 200:
            # Print full HTML
            print("=== FULL HTML CONTENT ===")
            print(response.text)
            print("\n=== END HTML ===\n")
            
            # Parse and analyze
            soup = BeautifulSoup(response.text, 'html.parser')
            
            print("=== ANALYSIS ===", file=sys.stderr)
            
            # Extract resources
            stylesheets = []
            for link in soup.find_all('link', rel='stylesheet'):
                href = link.get('href')
                stylesheets.append(href)
            print(f"Stylesheets: {stylesheets}", file=sys.stderr)
            
            scripts = []
            for script in soup.find_all('script'):
                src = script.get('src')
                if src:
                    scripts.append(src)
            print(f"Scripts: {scripts}", file=sys.stderr)
            
            images = []
            for img in soup.find_all('img'):
                src = img.get('src')
                alt = img.get('alt', '')
                if src:
                    images.append({'src': src, 'alt': alt})
            print(f"Images count: {len(images)}", file=sys.stderr)
            
            # Extract text
            body = soup.find('body')
            if body:
                text = body.get_text(separator='\n', strip=True)
                print(f"\n=== BODY TEXT ===", file=sys.stderr)
                print(text[:2000], file=sys.stderr)
        else:
            print(f"Failed to fetch: {response.status_code}", file=sys.stderr)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    get_website()
