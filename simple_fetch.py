#!/usr/bin/env python3
"""
Simple Website Fetcher for cosmetic-alena.com
Run this directly: python3 simple_fetch.py
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import re

def fetch_and_analyze():
    url = 'https://cosmetic-alena.com'
    
    # Fetch with proper headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print("=" * 80)
    print("FETCHING WEBSITE")
    print("=" * 80)
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Size: {len(html):,} bytes")
        print(f"✓ Parse: OK\n")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # =====================================================================
    # 1. RAW HTML
    # =====================================================================
    print("=" * 80)
    print("1. RAW HTML (First 2000 characters)")
    print("=" * 80)
    print(html[:2000])
    print(f"\n... Total HTML: {len(html)} characters\n")
    
    # Save full HTML
    with open('website_full.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✓ Saved: website_full.html\n")
    
    # =====================================================================
    # 2. CSS STYLESHEETS
    # =====================================================================
    print("=" * 80)
    print("2. CSS STYLESHEETS & STYLES")
    print("=" * 80)
    
    css_files = []
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href', '')
        if href:
            full_url = urljoin(url, href)
            css_files.append(full_url)
            print(f"  • {full_url}")
    
    print(f"\nTotal CSS files: {len(css_files)}")
    
    # Inline styles
    style_tags = soup.find_all('style')
    print(f"Inline <style> tags: {len(style_tags)}")
    
    if style_tags:
        for i, style in enumerate(style_tags[:2], 1):
            if style.string:
                print(f"\nInline Style {i} (first 500 chars):")
                print(style.string[:500])
    
    print()
    
    # =====================================================================
    # 3. JAVASCRIPT FILES
    # =====================================================================
    print("=" * 80)
    print("3. JAVASCRIPT FILES")
    print("=" * 80)
    
    js_files = []
    for script in soup.find_all('script', src=True):
        src = script.get('src', '')
        if src:
            full_url = urljoin(url, src)
            js_files.append(full_url)
            async_attr = " [async]" if script.has_attr('async') else ""
            defer_attr = " [defer]" if script.has_attr('defer') else ""
            print(f"  • {full_url}{async_attr}{defer_attr}")
    
    print(f"\nTotal JS files: {len(js_files)}")
    print()
    
    # =====================================================================
    # 4. IMAGES
    # =====================================================================
    print("=" * 80)
    print("4. IMAGES & VISUAL ASSETS")
    print("=" * 80)
    
    images = []
    
    # Regular img tags
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if src:
            full_url = urljoin(url, src)
            alt = img.get('alt', '')
            images.append({'url': full_url, 'alt': alt, 'src': src})
    
    # Picture elements
    for picture in soup.find_all('picture'):
        for source in picture.find_all('source'):
            srcset = source.get('srcset', '')
            if srcset:
                for src_part in srcset.split(','):
                    src = src_part.strip().split()[0]
                    full_url = urljoin(url, src)
                    images.append({'url': full_url, 'src': src, 'type': 'responsive'})
    
    # Background images
    for tag in soup.find_all(style=True):
        style = tag.get('style', '')
        if 'background' in style and 'url' in style:
            matches = re.findall(r'url\([\'"]?([^\)\'\"]+)[\'"]?\)', style)
            for match in matches:
                full_url = urljoin(url, match)
                images.append({'url': full_url, 'src': match, 'type': 'background'})
    
    # Remove duplicates
    seen = set()
    unique_images = []
    for img in images:
        key = img['url']
        if key not in seen:
            seen.add(key)
            unique_images.append(img)
    
    print(f"Total images found: {len(unique_images)}\n")
    for i, img in enumerate(unique_images[:15], 1):
        print(f"  {i:2}. {img['src']}")
        if img.get('alt'):
            print(f"      Alt: {img['alt']}")
    
    if len(unique_images) > 15:
        print(f"  ... and {len(unique_images) - 15} more images\n")
    else:
        print()
    
    # =====================================================================
    # 5. NAVIGATION & LINKS
    # =====================================================================
    print("=" * 80)
    print("5. NAVIGATION MENU & LINKS")
    print("=" * 80)
    
    nav = soup.find('nav')
    if nav:
        print("Navigation Menu Items:")
        for link in nav.find_all('a'):
            text = link.get_text(strip=True)
            href = link.get('href', '#')
            if text:
                print(f"  • {text} -> {href}")
    else:
        print("No <nav> element found")
    
    # All links
    all_links = {}
    for a in soup.find_all('a'):
        href = a.get('href', '')
        text = a.get_text(strip=True)
        if href and text:
            if href not in all_links:
                all_links[href] = text
    
    print(f"\nTotal unique links: {len(all_links)}")
    print()
    
    # =====================================================================
    # 6. PAGE TEXT CONTENT
    # =====================================================================
    print("=" * 80)
    print("6. PAGE TEXT CONTENT")
    print("=" * 80)
    
    # Remove scripts and styles
    soup_copy = BeautifulSoup(str(soup), 'html.parser')
    for script in soup_copy(["script", "style"]):
        script.decompose()
    
    text = soup_copy.get_text(separator='\n', strip=True)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    print(f"Total lines of visible text: {len(lines)}\n")
    print("Page Content (first 50 lines):\n")
    for line in lines[:50]:
        if len(line) > 80:
            print(f"  {line[:77]}...")
        else:
            print(f"  {line}")
    
    if len(lines) > 50:
        print(f"\n  ... ({len(lines) - 50} more lines of content)")
    
    print()
    
    # =====================================================================
    # 7. COLOR SCHEME
    # =====================================================================
    print("=" * 80)
    print("7. COLOR SCHEME/PALETTE")
    print("=" * 80)
    
    colors = set()
    
    # From inline styles
    for elem in soup.find_all(style=True):
        style = elem.get('style', '')
        hex_colors = re.findall(r'#[0-9a-fA-F]{3,6}', style)
        rgb_colors = re.findall(r'rgba?\([^)]+\)', style)
        colors.update(hex_colors)
        colors.update(rgb_colors)
    
    # From style tags
    for style_tag in soup.find_all('style'):
        if style_tag.string:
            hex_colors = re.findall(r'#[0-9a-fA-F]{3,6}', style_tag.string)
            rgb_colors = re.findall(r'rgba?\([^)]+\)', style_tag.string)
            colors.update(hex_colors)
            colors.update(rgb_colors)
    
    if colors:
        print("Colors found:")
        for color in sorted(colors)[:20]:
            print(f"  • {color}")
        if len(colors) > 20:
            print(f"  ... and {len(colors) - 20} more colors")
    else:
        print("No colors found in inline/internal styles")
        print("Check external CSS files for complete color palette")
    
    print()
    
    # =====================================================================
    # 8. FORMS
    # =====================================================================
    print("=" * 80)
    print("8. FORMS")
    print("=" * 80)
    
    forms = soup.find_all('form')
    if forms:
        for i, form in enumerate(forms, 1):
            print(f"\nForm {i}:")
            print(f"  Action: {form.get('action', 'Not specified')}")
            print(f"  Method: {form.get('method', 'GET').upper()}")
            print(f"  ID: {form.get('id', 'Not specified')}")
            
            fields = form.find_all(['input', 'textarea', 'select'])
            print(f"  Fields:")
            for field in fields:
                name = field.get('name', 'unnamed')
                field_type = field.get('type', field.name)
                print(f"    • {name} ({field_type})")
            
            buttons = form.find_all('button')
            if buttons:
                print(f"  Buttons:")
                for btn in buttons:
                    print(f"    • {btn.get_text(strip=True)}")
    else:
        print("No forms found on this page")
    
    print()
    
    # =====================================================================
    # 9. PAGE STRUCTURE
    # =====================================================================
    print("=" * 80)
    print("9. PAGE STRUCTURE")
    print("=" * 80)
    
    elements = {
        'header': len(soup.find_all('header')),
        'nav': len(soup.find_all('nav')),
        'main': len(soup.find_all('main')),
        'section': len(soup.find_all('section')),
        'article': len(soup.find_all('article')),
        'footer': len(soup.find_all('footer')),
    }
    
    for elem, count in elements.items():
        symbol = "✓" if count > 0 else "✗"
        print(f"  {symbol} <{elem}>: {count}")
    
    print()
    
    # =====================================================================
    # 10. PAGE METADATA
    # =====================================================================
    print("=" * 80)
    print("10. PAGE METADATA")
    print("=" * 80)
    
    title = soup.title.string if soup.title else "Not found"
    print(f"  Title: {title}")
    
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        print(f"  Description: {meta_desc.get('content', '')}")
    
    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
    if meta_keywords:
        print(f"  Keywords: {meta_keywords.get('content', '')}")
    
    meta_viewport = soup.find('meta', attrs={'name': 'viewport'})
    if meta_viewport:
        print(f"  Responsive: Yes (viewport defined)")
    
    print()
    
    # =====================================================================
    # SAVE JSON REPORT
    # =====================================================================
    report = {
        'url': url,
        'title': title,
        'html_size': len(html),
        'css_files': css_files,
        'js_files': js_files,
        'image_count': len(unique_images),
        'images': unique_images[:50],  # First 50
        'link_count': len(all_links),
        'form_count': len(forms),
        'text_lines': len(lines),
        'colors_found': list(colors)[:30],
        'page_elements': elements,
    }
    
    with open('analysis_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    print("=" * 80)
    print("FILES SAVED")
    print("=" * 80)
    print("✓ website_full.html")
    print("✓ analysis_report.json")
    print("=" * 80)
    print("\nAnalysis complete!")

if __name__ == '__main__':
    fetch_and_analyze()
