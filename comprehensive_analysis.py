#!/usr/bin/env python3
"""
Comprehensive Website Analysis Script
Fetches and analyzes https://cosmetic-alena.com
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import re
from datetime import datetime

class WebsiteAnalyzer:
    def __init__(self, url):
        self.url = url
        self.base_domain = urlparse(url).netloc
        self.html = None
        self.soup = None
        self.analysis = {}
        
    def fetch(self):
        """Fetch the website"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            print(f"📡 Fetching {self.url}...")
            response = requests.get(self.url, headers=headers, timeout=15)
            response.raise_for_status()
            
            self.html = response.text
            self.soup = BeautifulSoup(self.html, 'html.parser')
            print(f"✓ Successfully fetched (Status: {response.status_code}, Size: {len(self.html)} bytes)")
            return True
        except Exception as e:
            print(f"✗ Error fetching website: {e}")
            return False
    
    def analyze_all(self):
        """Run all analyses"""
        if not self.soup:
            return False
        
        print("\n" + "="*70)
        print("ANALYZING WEBSITE STRUCTURE")
        print("="*70)
        
        self.analyze_basic_info()
        self.analyze_stylesheets()
        self.analyze_scripts()
        self.analyze_images()
        self.analyze_links()
        self.analyze_forms()
        self.analyze_buttons()
        self.analyze_page_structure()
        self.analyze_text_content()
        self.analyze_colors()
        self.analyze_api_endpoints()
        
        return True
    
    def analyze_basic_info(self):
        """Extract basic page information"""
        print("\n📄 BASIC INFORMATION:")
        
        title = self.soup.title.string if self.soup.title else "No title found"
        print(f"  Title: {title}")
        
        description = ""
        meta_desc = self.soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            description = meta_desc.get('content', '')
            print(f"  Description: {description}")
        
        keywords = ""
        meta_keywords = self.soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            keywords = meta_keywords.get('content', '')
            print(f"  Keywords: {keywords}")
        
        self.analysis['basic'] = {
            'title': title,
            'description': description,
            'keywords': keywords,
            'url': self.url
        }
    
    def analyze_stylesheets(self):
        """Extract CSS stylesheets"""
        print("\n🎨 STYLESHEETS & STYLES:")
        
        stylesheets = []
        for link in self.soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                full_url = urljoin(self.url, href)
                stylesheets.append({
                    'path': href,
                    'full_url': full_url,
                    'media': link.get('media', 'all')
                })
                print(f"  - {href}")
                print(f"    Full URL: {full_url}")
        
        # Inline styles count
        inline_style_count = len(self.soup.find_all(style=True))
        if inline_style_count > 0:
            print(f"  + {inline_style_count} elements with inline styles")
        
        self.analysis['stylesheets'] = stylesheets
        print(f"✓ Found {len(stylesheets)} external stylesheets")
    
    def analyze_scripts(self):
        """Extract JavaScript files"""
        print("\n📜 JAVASCRIPT FILES:")
        
        external_scripts = []
        inline_scripts = []
        
        for script in self.soup.find_all('script'):
            src = script.get('src')
            if src:
                full_url = urljoin(self.url, src)
                external_scripts.append({
                    'src': src,
                    'full_url': full_url,
                    'async': script.has_attr('async'),
                    'defer': script.has_attr('defer'),
                    'type': script.get('type', 'text/javascript')
                })
                print(f"  - {src}")
                print(f"    Full URL: {full_url}")
                if script.has_attr('async'):
                    print(f"    Attributes: async")
                if script.has_attr('defer'):
                    print(f"    Attributes: defer")
            else:
                # Inline script
                content = script.string
                if content:
                    inline_scripts.append(content[:300])  # First 300 chars
        
        self.analysis['scripts'] = {
            'external': external_scripts,
            'inline_count': len(inline_scripts)
        }
        print(f"✓ Found {len(external_scripts)} external scripts, {len(inline_scripts)} inline scripts")
    
    def analyze_images(self):
        """Extract all images"""
        print("\n🖼️  IMAGES & VISUAL ASSETS:")
        
        images = []
        
        # Regular img tags
        for img in self.soup.find_all('img'):
            src = img.get('src')
            if src:
                full_url = urljoin(self.url, src)
                images.append({
                    'src': src,
                    'full_url': full_url,
                    'alt': img.get('alt', ''),
                    'title': img.get('title', ''),
                    'width': img.get('width'),
                    'height': img.get('height'),
                    'class': ' '.join(img.get('class', []))
                })
        
        # Picture elements
        for picture in self.soup.find_all('picture'):
            for source in picture.find_all('source'):
                srcset = source.get('srcset')
                if srcset:
                    sources = [s.strip().split()[0] for s in srcset.split(',')]
                    for src in sources:
                        full_url = urljoin(self.url, src)
                        images.append({
                            'src': src,
                            'full_url': full_url,
                            'type': 'responsive',
                            'media': source.get('media', '')
                        })
        
        # Background images in CSS
        for tag in self.soup.find_all():
            style = tag.get('style', '')
            bg_images = re.findall(r'background[^:]*:\s*url\([\'"]?([^\)\'\"]+)[\'"]?\)', style)
            for bg_img in bg_images:
                full_url = urljoin(self.url, bg_img)
                images.append({
                    'src': bg_img,
                    'full_url': full_url,
                    'type': 'background'
                })
        
        # Remove duplicates
        seen = set()
        unique_images = []
        for img in images:
            key = img['full_url']
            if key not in seen:
                seen.add(key)
                unique_images.append(img)
        
        print(f"  Found {len(unique_images)} unique images:")
        for i, img in enumerate(unique_images[:15], 1):
            print(f"  {i}. {img['src'][:60]}")
            if img.get('alt'):
                print(f"     Alt: {img['alt'][:50]}")
        
        if len(unique_images) > 15:
            print(f"  ... and {len(unique_images) - 15} more images")
        
        self.analysis['images'] = unique_images
        print(f"✓ Found {len(unique_images)} images total")
    
    def analyze_links(self):
        """Extract all links"""
        print("\n🔗 NAVIGATION & LINKS:")
        
        links = {}
        
        for a in self.soup.find_all('a'):
            href = a.get('href')
            if href:
                # Handle different link types
                if href.startswith('mailto:'):
                    link_type = 'email'
                    full_url = href
                elif href.startswith('tel:'):
                    link_type = 'phone'
                    full_url = href
                elif href.startswith('#'):
                    link_type = 'anchor'
                    full_url = href
                elif href.startswith('http'):
                    link_type = 'external'
                    full_url = href
                else:
                    link_type = 'internal'
                    full_url = urljoin(self.url, href)
                
                text = a.get_text(strip=True)
                
                if href not in links:
                    links[href] = {
                        'href': href,
                        'full_url': full_url,
                        'text': text,
                        'type': link_type,
                        'class': ' '.join(a.get('class', []))
                    }
        
        # Categorize links
        internal_links = [l for l in links.values() if l['type'] == 'internal']
        external_links = [l for l in links.values() if l['type'] == 'external']
        anchor_links = [l for l in links.values() if l['type'] == 'anchor']
        email_links = [l for l in links.values() if l['type'] == 'email']
        
        print(f"  Internal Links: {len(internal_links)}")
        for link in internal_links[:10]:
            print(f"    - {link['href'][:50]} ({link['text'][:30]})")
        
        if len(internal_links) > 10:
            print(f"    ... and {len(internal_links) - 10} more")
        
        if external_links:
            print(f"\n  External Links: {len(external_links)}")
            for link in external_links[:5]:
                print(f"    - {link['href']}")
        
        if email_links:
            print(f"\n  Email Links: {len(email_links)}")
            for link in email_links:
                print(f"    - {link['href']}")
        
        self.analysis['links'] = {
            'total': len(links),
            'internal': internal_links,
            'external': external_links,
            'anchors': anchor_links,
            'email': email_links
        }
    
    def analyze_forms(self):
        """Extract form information"""
        print("\n📋 FORMS & USER INPUT:")
        
        forms = []
        
        for form in self.soup.find_all('form'):
            form_data = {
                'action': form.get('action', ''),
                'method': form.get('method', 'GET').upper(),
                'id': form.get('id', ''),
                'class': form.get('class', []),
                'fields': [],
                'buttons': []
            }
            
            # Get all input fields
            for field in form.find_all(['input', 'textarea', 'select']):
                field_info = {
                    'type': field.name,
                    'name': field.get('name', ''),
                    'input_type': field.get('type', ''),
                    'placeholder': field.get('placeholder', ''),
                    'required': field.has_attr('required'),
                    'id': field.get('id', '')
                }
                form_data['fields'].append(field_info)
            
            # Get submit buttons
            for button in form.find_all('button'):
                form_data['buttons'].append({
                    'text': button.get_text(strip=True),
                    'type': button.get('type', 'submit'),
                    'name': button.get('name', '')
                })
            
            forms.append(form_data)
            
            if forms:
                print(f"  Form {len(forms)}:")
                print(f"    Action: {form_data['action']}")
                print(f"    Method: {form_data['method']}")
                print(f"    Fields: {len(form_data['fields'])}")
                for field in form_data['fields'][:5]:
                    print(f"      - {field['name']} ({field['input_type']})" + 
                          (", required" if field['required'] else ""))
                if len(form_data['fields']) > 5:
                    print(f"      ... and {len(form_data['fields']) - 5} more")
        
        self.analysis['forms'] = forms
        print(f"✓ Found {len(forms)} forms")
    
    def analyze_buttons(self):
        """Extract interactive buttons"""
        print("\n🔘 BUTTONS & INTERACTIVE ELEMENTS:")
        
        buttons = []
        interactive = []
        
        for button in self.soup.find_all('button'):
            buttons.append({
                'text': button.get_text(strip=True),
                'type': button.get('type', 'submit'),
                'class': ' '.join(button.get('class', [])),
                'id': button.get('id', '')
            })
        
        for input_el in self.soup.find_all('input'):
            if input_el.get('type') in ['button', 'submit', 'reset', 'checkbox', 'radio']:
                interactive.append({
                    'type': input_el.get('type', 'button'),
                    'value': input_el.get('value', ''),
                    'name': input_el.get('name', '')
                })
        
        print(f"  Buttons: {len(buttons)}")
        for btn in buttons[:10]:
            print(f"    - {btn['text'][:50]}")
        
        print(f"  Interactive Elements: {len(interactive)}")
        
        self.analysis['buttons'] = buttons
        self.analysis['interactive'] = interactive
    
    def analyze_page_structure(self):
        """Analyze page layout and structure"""
        print("\n🏗️  PAGE STRUCTURE:")
        
        structure = {
            'has_header': bool(self.soup.find('header')),
            'has_nav': bool(self.soup.find('nav')),
            'has_main': bool(self.soup.find('main')),
            'has_footer': bool(self.soup.find('footer')),
            'has_aside': bool(self.soup.find('aside')),
            'sections': len(self.soup.find_all('section')),
            'articles': len(self.soup.find_all('article')),
            'divs_with_ids': [],
            'important_divs': []
        }
        
        # Get important divs
        for div in self.soup.find_all('div', id=True):
            div_id = div.get('id')
            structure['divs_with_ids'].append(div_id)
        
        # Get divs with important classes
        important_classes = ['container', 'wrapper', 'main', 'content', 'sidebar', 'header', 'footer', 'nav']
        for div in self.soup.find_all('div', class_=True):
            div_classes = div.get('class', [])
            if any(ic in ' '.join(div_classes) for ic in important_classes):
                structure['important_divs'].append({
                    'class': ' '.join(div_classes),
                    'id': div.get('id', '')
                })
        
        print(f"  Semantic Elements:")
        print(f"    - Header: {structure['has_header']}")
        print(f"    - Navigation: {structure['has_nav']}")
        print(f"    - Main: {structure['has_main']}")
        print(f"    - Footer: {structure['has_footer']}")
        print(f"    - Aside: {structure['has_aside']}")
        print(f"    - Sections: {structure['sections']}")
        print(f"    - Articles: {structure['articles']}")
        
        print(f"\n  Important DIVs (IDs): {len(structure['divs_with_ids'])}")
        for div_id in structure['divs_with_ids'][:10]:
            print(f"    - {div_id}")
        
        self.analysis['structure'] = structure
    
    def analyze_text_content(self):
        """Extract text content and headings"""
        print("\n📝 TEXT CONTENT:")
        
        headings = []
        paragraphs = []
        
        # Headings
        for i in range(1, 7):
            tag = self.soup.find_all(f'h{i}')
            for heading in tag:
                text = heading.get_text(strip=True)
                if text:
                    headings.append({
                        'level': i,
                        'text': text
                    })
        
        # Paragraphs
        for p in self.soup.find_all('p'):
            text = p.get_text(strip=True)
            if text and len(text) > 10:
                paragraphs.append(text)
        
        print(f"  Headings: {len(headings)}")
        for h in headings[:10]:
            print(f"    H{h['level']}: {h['text'][:60]}")
        
        print(f"\n  Paragraphs: {len(paragraphs)}")
        for p in paragraphs[:5]:
            print(f"    - {p[:80]}...")
        
        if len(paragraphs) > 5:
            print(f"    ... and {len(paragraphs) - 5} more paragraphs")
        
        self.analysis['content'] = {
            'headings': headings,
            'paragraphs': paragraphs
        }
    
    def analyze_colors(self):
        """Extract color scheme"""
        print("\n🎨 COLOR SCHEME:")
        
        colors = set()
        
        # From CSS files
        for link in self.soup.find_all('link', rel='stylesheet'):
            # Would need to fetch CSS files to analyze them
            pass
        
        # From inline styles
        for tag in self.soup.find_all(style=True):
            style = tag.get('style', '')
            # Extract hex colors
            hex_colors = re.findall(r'#[0-9a-fA-F]{3,6}', style)
            colors.update(hex_colors)
            
            # Extract rgb colors
            rgb_colors = re.findall(r'rgb\([^)]+\)', style)
            colors.update(rgb_colors)
        
        colors = list(colors)[:20]  # Top 20 colors
        
        if colors:
            print(f"  Color from inline styles:")
            for color in colors:
                print(f"    - {color}")
        else:
            print("  No inline colors found - colors likely defined in external CSS")
        
        self.analysis['colors'] = colors
    
    def analyze_api_endpoints(self):
        """Look for API endpoints and data sources"""
        print("\n🔌 API ENDPOINTS & DATA SOURCES:")
        
        endpoints = set()
        
        # Look in inline scripts
        for script in self.soup.find_all('script'):
            content = script.string
            if content:
                # Look for fetch, axios, fetch URLs
                fetch_patterns = re.findall(r'(?:fetch|axios\.get|fetch|XMLHttpRequest)\s*\(\s*["\']([^"\']+)["\']', content, re.IGNORECASE)
                endpoints.update(fetch_patterns)
                
                # Look for API paths
                api_patterns = re.findall(r'["\']([/\w]*(?:api|endpoint|service)[/\w]*)["\']', content, re.IGNORECASE)
                endpoints.update(api_patterns)
        
        # Look in data attributes
        for tag in self.soup.find_all(attrs={'data-url': True}):
            endpoints.add(tag.get('data-url'))
        
        for tag in self.soup.find_all(attrs={'data-api': True}):
            endpoints.add(tag.get('data-api'))
        
        endpoints = [ep for ep in endpoints if ep][:10]  # Top 10
        
        if endpoints:
            print(f"  Found {len(endpoints)} potential API endpoints:")
            for endpoint in endpoints:
                print(f"    - {endpoint}")
        else:
            print("  No obvious API endpoints found in inline scripts")
        
        self.analysis['api_endpoints'] = endpoints
    
    def save_results(self):
        """Save analysis results to files"""
        print("\n" + "="*70)
        print("SAVING ANALYSIS RESULTS")
        print("="*70)
        
        # Save full HTML
        with open('/workspaces/cosmetic-alena.com/website_full.html', 'w', encoding='utf-8') as f:
            f.write(self.html)
        print("✓ Saved: website_full.html")
        
        # Save pretty HTML
        with open('/workspaces/cosmetic-alena.com/website_pretty.html', 'w', encoding='utf-8') as f:
            f.write(self.soup.prettify())
        print("✓ Saved: website_pretty.html")
        
        # Save JSON analysis
        # Convert sets and non-serializable objects
        analysis_json = json.dumps(self.analysis, indent=2, ensure_ascii=False, default=str)
        with open('/workspaces/cosmetic-alena.com/analysis_report.json', 'w', encoding='utf-8') as f:
            f.write(analysis_json)
        print("✓ Saved: analysis_report.json")
        
        # Save detailed markdown report
        report = self.generate_markdown_report()
        with open('/workspaces/cosmetic-alena.com/WEBSITE_ANALYSIS.md', 'w', encoding='utf-8') as f:
            f.write(report)
        print("✓ Saved: WEBSITE_ANALYSIS.md")
    
    def generate_markdown_report(self):
        """Generate a detailed markdown report"""
        report = f"""# Website Analysis Report
**URL:** {self.url}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Table of Contents
1. [Basic Information](#basic-information)
2. [Stylesheets](#stylesheets)
3. [JavaScript Files](#javascript-files)
4. [Images](#images)
5. [Links](#links)
6. [Forms](#forms)
7. [Page Structure](#page-structure)
8. [Content](#content)
9. [Colors](#colors)
10. [API Endpoints](#api-endpoints)

## Basic Information

- **Title:** {self.analysis['basic']['title']}
- **Description:** {self.analysis['basic']['description']}
- **Keywords:** {self.analysis['basic']['keywords']}

## Stylesheets

Total: **{len(self.analysis['stylesheets'])}** external stylesheets

"""
        
        for i, css in enumerate(self.analysis['stylesheets'], 1):
            report += f"{i}. `{css['path']}`\n"
            report += f"   - Full URL: {css['full_url']}\n"
            report += f"   - Media: {css['media']}\n\n"
        
        report += "## JavaScript Files\n\n"
        report += f"**External Scripts:** {len(self.analysis['scripts']['external'])}\n\n"
        
        for i, js in enumerate(self.analysis['scripts']['external'], 1):
            attrs = []
            if js['async']:
                attrs.append('async')
            if js['defer']:
                attrs.append('defer')
            attrs_str = f" ({', '.join(attrs)})" if attrs else ""
            report += f"{i}. `{js['src']}`{attrs_str}\n"
            report += f"   - Full URL: {js['full_url']}\n\n"
        
        report += f"**Inline Scripts:** {self.analysis['scripts']['inline_count']}\n\n"
        
        report += "## Images\n\n"
        report += f"Total: **{len(self.analysis['images'])}** images\n\n"
        
        for i, img in enumerate(self.analysis['images'][:20], 1):
            report += f"{i}. `{img['src']}`\n"
            if img.get('alt'):
                report += f"   - Alt: {img['alt']}\n"
            if img.get('type'):
                report += f"   - Type: {img.get('type')}\n"
            report += "\n"
        
        if len(self.analysis['images']) > 20:
            report += f"... and {len(self.analysis['images']) - 20} more images\n\n"
        
        report += "## Links\n\n"
        report += f"- **Internal Links:** {len(self.analysis['links']['internal'])}\n"
        report += f"- **External Links:** {len(self.analysis['links']['external'])}\n"
        report += f"- **Email Links:** {len(self.analysis['links']['email'])}\n"
        report += f"- **Anchor Links:** {len(self.analysis['links']['anchors'])}\n\n"
        
        if self.analysis['links']['internal']:
            report += "### Internal Links\n\n"
            for link in self.analysis['links']['internal'][:15]:
                report += f"- [{link['text']}]({link['href']})\n"
            if len(self.analysis['links']['internal']) > 15:
                report += f"- ... and {len(self.analysis['links']['internal']) - 15} more\n"
            report += "\n"
        
        if self.analysis['links']['external']:
            report += "### External Links\n\n"
            for link in self.analysis['links']['external'][:10]:
                report += f"- {link['href']}\n"
            if len(self.analysis['links']['external']) > 10:
                report += f"- ... and {len(self.analysis['links']['external']) - 10} more\n"
            report += "\n"
        
        report += "## Forms\n\n"
        if self.analysis['forms']:
            for i, form in enumerate(self.analysis['forms'], 1):
                report += f"### Form {i}\n\n"
                report += f"- **Action:** {form['action']}\n"
                report += f"- **Method:** {form['method']}\n"
                report += f"- **Fields:** {len(form['fields'])}\n\n"
                
                if form['fields']:
                    for field in form['fields']:
                        required = " (required)" if field['required'] else ""
                        report += f"  - `{field['name']}` - {field['input_type']}{required}\n"
                        if field['placeholder']:
                            report += f"    Placeholder: {field['placeholder']}\n"
                report += "\n"
        else:
            report += "No forms found.\n\n"
        
        report += "## Page Structure\n\n"
        structure = self.analysis['structure']
        report += f"- Has Header: {structure['has_header']}\n"
        report += f"- Has Navigation: {structure['has_nav']}\n"
        report += f"- Has Main: {structure['has_main']}\n"
        report += f"- Has Footer: {structure['has_footer']}\n"
        report += f"- Has Aside: {structure['has_aside']}\n"
        report += f"- Sections: {structure['sections']}\n"
        report += f"- Articles: {structure['articles']}\n\n"
        
        if structure['divs_with_ids']:
            report += "### DIV Elements with IDs\n\n"
            for div_id in structure['divs_with_ids'][:15]:
                report += f"- `{div_id}`\n"
            if len(structure['divs_with_ids']) > 15:
                report += f"- ... and {len(structure['divs_with_ids']) - 15} more\n"
            report += "\n"
        
        report += "## Content\n\n"
        if self.analysis['content']['headings']:
            report += "### Headings\n\n"
            for h in self.analysis['content']['headings'][:20]:
                report += f"- **H{h['level']}:** {h['text']}\n"
            if len(self.analysis['content']['headings']) > 20:
                report += f"- ... and {len(self.analysis['content']['headings']) - 20} more\n"
            report += "\n"
        
        report += "## Colors\n\n"
        if self.analysis['colors']:
            report += "Colors found in inline styles:\n\n"
            for color in self.analysis['colors']:
                report += f"- `{color}`\n"
        else:
            report += "No colors found in inline styles (likely defined in external CSS).\n"
        report += "\n"
        
        report += "## API Endpoints\n\n"
        if self.analysis['api_endpoints']:
            for endpoint in self.analysis['api_endpoints']:
                report += f"- `{endpoint}`\n"
        else:
            report += "No obvious API endpoints found in JavaScript code.\n"
        
        return report


if __name__ == '__main__':
    print("\n" + "="*70)
    print("COSMETIC-ALENA.COM WEBSITE ANALYZER")
    print("="*70 + "\n")
    
    analyzer = WebsiteAnalyzer('https://cosmetic-alena.com')
    
    if analyzer.fetch():
        if analyzer.analyze_all():
            analyzer.save_results()
            print("\n" + "="*70)
            print("✓ ANALYSIS COMPLETE!")
            print("="*70)
            print("\nGenerated files:")
            print("  1. website_full.html - Complete HTML source")
            print("  2. website_pretty.html - Formatted HTML")
            print("  3. analysis_report.json - Detailed analysis in JSON format")
            print("  4. WEBSITE_ANALYSIS.md - Human-readable markdown report")
            print("\n")
    else:
        print("Failed to fetch website")
