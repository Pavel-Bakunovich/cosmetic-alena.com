#!/usr/bin/env python3
"""
Comprehensive script to analyze the cosmetic-alena.com website structure
"""
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import defaultdict
import json
import re

def fetch_website(url):
    """Fetch website and return response"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text, response.status_code
    except Exception as e:
        print(f"Error fetching website: {e}")
        return None, None

def analyze_website(html, base_url):
    """Comprehensive website structure analysis"""
    soup = BeautifulSoup(html, 'html.parser')
    base_domain = urlparse(base_url).netloc
    
    analysis = {
        'title': soup.title.string if soup.title else 'No title',
        'description': '',
        'meta_tags': [],
        'stylesheets': [],
        'scripts': [],
        'images': [],
        'links': [],
        'forms': [],
        'buttons': [],
        'text_content': [],
        'page_structure': {},
        'colors': set(),
        'interactive_elements': [],
        'api_endpoints': [],
        'inline_scripts': []
    }
    
    # Meta tags
    for meta in soup.find_all('meta'):
        meta_dict = {
            'name': meta.get('name'),
            'content': meta.get('content'),
            'charset': meta.get('charset'),
            'http_equiv': meta.get('http-equiv')
        }
        analysis['meta_tags'].append({k: v for k, v in meta_dict.items() if v})
        
        # Get description
        if meta.get('name') == 'description':
            analysis['description'] = meta.get('content', '')
    
    # Stylesheets
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href')
        if href:
            full_url = urljoin(base_url, href)
            analysis['stylesheets'].append({
                'href': href,
                'full_url': full_url
            })
    
    # Inline styles - extract colors
    for tag in soup.find_all(style=True):
        style = tag.get('style', '')
        # Extract color values
        colors = re.findall(r'(#[0-9a-fA-F]{3,6}|rgb\([^)]+\)|rgba\([^)]+\))', style)
        analysis['colors'].update(colors)
    
    # External Scripts
    for script in soup.find_all('script'):
        src = script.get('src')
        if src:
            full_url = urljoin(base_url, src)
            analysis['scripts'].append({
                'src': src,
                'full_url': full_url,
                'async': script.get('async') is not None,
                'defer': script.get('defer') is not None
            })
        else:
            # Inline scripts
            content = script.string
            if content:
                analysis['inline_scripts'].append(content.strip()[:200])  # First 200 chars
                # Look for API endpoints
                api_patterns = re.findall(r'(["\'])([^"\']*(?:api|endpoint|service)[^"\']*)\1', content, re.IGNORECASE)
                for _, api_url in api_patterns:
                    if api_url not in analysis['api_endpoints']:
                        analysis['api_endpoints'].append(api_url)
    
    # Images
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            full_url = urljoin(base_url, src)
            analysis['images'].append({
                'src': src,
                'full_url': full_url,
                'alt': img.get('alt', ''),
                'title': img.get('title', ''),
                'width': img.get('width'),
                'height': img.get('height')
            })
    
    # Picture elements (responsive images)
    for picture in soup.find_all('picture'):
        for source in picture.find_all('source'):
            srcset = source.get('srcset')
            if srcset:
                # Parse srcset
                sources = [s.strip().split()[0] for s in srcset.split(',')]
                for src in sources:
                    full_url = urljoin(base_url, src)
                    analysis['images'].append({
                        'src': src,
                        'full_url': full_url,
                        'alt': 'picture element',
                        'responsive': True
                    })
    
    # All links
    for a in soup.find_all('a'):
        href = a.get('href')
        if href:
            full_url = urljoin(base_url, href) if not href.startswith(('mailto:', 'tel:')) else href
            analysis['links'].append({
                'href': href,
                'full_url': full_url if not href.startswith(('mailto:', 'tel:')) else href,
                'text': a.get_text(strip=True),
                'class': a.get('class', [])
            })
    
    # Forms
    for form in soup.find_all('form'):
        form_data = {
            'action': form.get('action', ''),
            'method': form.get('method', 'GET').upper(),
            'fields': []
        }
        for field in form.find_all(['input', 'textarea', 'select']):
            field_info = {
                'type': field.name,
                'name': field.get('name', ''),
                'input_type': field.get('type', ''),
                'placeholder': field.get('placeholder', ''),
                'required': field.has_attr('required')
            }
            form_data['fields'].append(field_info)
        analysis['forms'].append(form_data)
    
    # Buttons and interactive elements
    for button in soup.find_all('button'):
        analysis['buttons'].append({
            'text': button.get_text(strip=True),
            'type': button.get('type', 'submit'),
            'class': button.get('class', [])
        })
    
    # Interactive elements
    for interactive in soup.find_all(['input', 'textarea', 'select', 'button']):
        if interactive.name == 'input':
            analysis['interactive_elements'].append({
                'type': 'input',
                'input_type': interactive.get('type', 'text'),
                'name': interactive.get('name', ''),
                'placeholder': interactive.get('placeholder', '')
            })
    
    # Page Structure - identify major sections
    structure_sections = {
        'header': soup.find('header'),
        'nav': soup.find('nav'),
        'main': soup.find('main'),
        'footer': soup.find('footer'),
        'sections': soup.find_all('section'),
        'articles': soup.find_all('article'),
        'divs_with_ids': []
    }
    
    # Important divs with IDs
    for div in soup.find_all('div'):
        div_id = div.get('id')
        if div_id:
            structure_sections['divs_with_ids'].append(div_id)
    
    analysis['page_structure'] = {
        'has_header': structure_sections['header'] is not None,
        'has_nav': structure_sections['nav'] is not None,
        'has_main': structure_sections['main'] is not None,
        'has_footer': structure_sections['footer'] is not None,
        'sections_count': len(structure_sections['sections']),
        'articles_count': len(structure_sections['articles']),
        'important_divs': structure_sections['divs_with_ids'][:10]  # Top 10
    }
    
    # Extract all text content
    text_elements = []
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
        text = tag.get_text(strip=True)
        if text:
            text_elements.append({
                'tag': tag.name,
                'text': text
            })
    analysis['text_content'] = text_elements
    
    return analysis, soup

if __name__ == '__main__':
    url = 'https://cosmetic-alena.com'
    print(f"Fetching {url}...")
    
    html, status = fetch_website(url)
    if html:
        print(f"✓ Status: {status}\n")
        analysis, soup = analyze_website(html, url)
        
        print("=" * 60)
        print("WEBSITE ANALYSIS - cosmetic-alena.com")
        print("=" * 60)
        
        print(f"\n📄 BASIC INFO:")
        print(f"  Title: {analysis['title']}")
        print(f"  Description: {analysis['description'][:100]}...")
        
        print(f"\n🎨 STYLESHEETS ({len(analysis['stylesheets'])}):")
        for css in analysis['stylesheets']:
            print(f"  - {css['href']}")
        
        print(f"\n📜 EXTERNAL SCRIPTS ({len(analysis['scripts'])}):")
        for js in analysis['scripts']:
            print(f"  - {js['src']}")
        
        print(f"\n🖼️  IMAGES ({len(analysis['images'])}):")
        for img in analysis['images'][:10]:  # Show first 10
            print(f"  - {img['src']} (alt: {img['alt'][:30] if img['alt'] else 'N/A'})")
        if len(analysis['images']) > 10:
            print(f"  ... and {len(analysis['images']) - 10} more images")
        
        print(f"\n🔗 LINKS ({len(analysis['links'])}):")
        unique_links = {}
        for link in analysis['links']:
            href = link['href']
            if href not in unique_links:
                unique_links[href] = link['text'][:50]
        for href, text in list(unique_links.items())[:15]:
            print(f"  - {href} → {text}")
        if len(unique_links) > 15:
            print(f"  ... and {len(unique_links) - 15} more links")
        
        print(f"\n📋 FORMS FOUND: {len(analysis['forms'])}")
        for i, form in enumerate(analysis['forms'], 1):
            print(f"  Form {i}: {form['method']} to {form['action']}")
            for field in form['fields']:
                print(f"    - {field['name']} ({field['input_type']})")
        
        print(f"\n🔘 BUTTONS: {len(analysis['buttons'])}")
        for btn in analysis['buttons'][:5]:
            print(f"  - {btn['text']}")
        
        print(f"\n🏗️  PAGE STRUCTURE:")
        print(f"  Has Header: {analysis['page_structure']['has_header']}")
        print(f"  Has Navigation: {analysis['page_structure']['has_nav']}")
        print(f"  Has Main Content: {analysis['page_structure']['has_main']}")
        print(f"  Has Footer: {analysis['page_structure']['has_footer']}")
        print(f"  Sections: {analysis['page_structure']['sections_count']}")
        print(f"  Articles: {analysis['page_structure']['articles_count']}")
        
        print(f"\n🎨 COLOR SCHEME:")
        if analysis['colors']:
            for color in list(analysis['colors'])[:10]:
                print(f"  - {color}")
        else:
            print("  No inline colors found")
        
        print(f"\n📝 TEXT CONTENT SUMMARY ({len(analysis['text_content'])} elements):")
        for elem in analysis['text_content'][:10]:
            preview = elem['text'][:60].replace('\n', ' ')
            print(f"  <{elem['tag']}> {preview}...")
        
        if analysis['forms']:
            print(f"\n✉️  INTERACTIVE ELEMENTS: {len(analysis['interactive_elements'])}")
        
        if analysis['api_endpoints']:
            print(f"\n🔌 API ENDPOINTS FOUND: {len(analysis['api_endpoints'])}")
            for endpoint in analysis['api_endpoints'][:5]:
                print(f"  - {endpoint}")
        
        # Save detailed JSON report
        report_data = {
            'title': analysis['title'],
            'description': analysis['description'],
            'stylesheets': analysis['stylesheets'],
            'scripts': analysis['scripts'],
            'images': analysis['images'],
            'links': analysis['links'],
            'forms': analysis['forms'],
            'buttons': analysis['buttons'],
            'page_structure': analysis['page_structure'],
            'text_content': analysis['text_content'][:50],  # First 50 text elements
            'colors': list(analysis['colors'])[:20],
            'api_endpoints': analysis['api_endpoints']
        }
        
        with open('website_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Detailed analysis saved to website_analysis.json")
        
        # Save full HTML
        with open('website_html.txt', 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✓ Full HTML saved to website_html.txt")
        
        # Save pretty HTML
        with open('website_html_pretty.txt', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print(f"✓ Formatted HTML saved to website_html_pretty.txt")
        
        print("\n" + "=" * 60)
        with open('website_analysis.json', 'w') as f:
            json.dump(analysis, f, indent=2)
        print("Analysis saved to website_analysis.json")
