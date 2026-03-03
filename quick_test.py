import requests
from bs4 import BeautifulSoup

try:
    # Simple test fetch
    response = requests.get('https://cosmetic-alena.com', timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Size: {len(response.text)} bytes")
    
    # Save HTML
    with open('website_raw.html', 'w') as f:
        f.write(response.text)
    print("Saved HTML to website_raw.html")
    
    # Quick analysis
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f"\nTitle: {soup.title.string if soup.title else 'No title'}")
    print(f"CSS Files: {len(soup.find_all('link', rel='stylesheet'))}")
    print(f"JS Files: {len([s for s in soup.find_all('script') if s.get('src')])}")
    print(f"Images: {len(soup.find_all('img'))}")
    print(f"Links: {len(soup.find_all('a'))}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
