#!/usr/bin/env python3
"""
Advanced Website Analyzer with Media Extraction
Downloads all resources for offline browsing and analysis
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import os
import shutil
from pathlib import Path
import re
from datetime import datetime

class AdvancedWebsiteAnalyzer:
    def __init__(self, url, output_dir='website_content'):
        self.url = url
        self.output_dir = output_dir
        self.base_domain = urlparse(url).netloc
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Create output directories
        self.create_directories()
        
    def create_directories(self):
        """Create directory structure for organized output"""
        dirs = [
            self.output_dir,
            f"{self.output_dir}/images",
            f"{self.output_dir}/css",
            f"{self.output_dir}/js",
            f"{self.output_dir}/fonts",
            f"{self.output_dir}/html",
            f"{self.output_dir}/reports"
        ]
        
        for d in dirs:
            Path(d).mkdir(parents=True, exist_ok=True)
    
    def fetch_url(self, url, timeout=10):
        """Safely fetch a URL"""
        try:
            response = self.session.get(url, timeout=timeout)
            return response
        except Exception as e:
            print(f"  ✗ Failed to fetch {url}: {e}")
            return None
    
    def fetch_and_save_resource(self, resource_url, save_dir, resource_type):
        """Fetch and save a resource (CSS, JS, image, font)"""
        try:
            full_url = urljoin(self.url, resource_url) if not resource_url.startswith(('http://', 'https://')) else resource_url
            
            # Skip if not from our domain or common CDNs
            parsed = urlparse(full_url)
            domain = parsed.netloc
            
            response = self.fetch_url(full_url, timeout=5)
            if response and response.status_code == 200:
                # Extract filename
                path = parsed.path
                filename = os.path.basename(path) or f"{resource_type}_{datetime.now().timestamp()}"
                
                # Remove query parameters from filename
                filename = filename.split('?')[0]
                
                filepath = os.path.join(save_dir, filename)
                
                # For binary files
                if resource_type in ['image', 'font']:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                else:
                    # For text files
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                
                return filename
        except Exception as e:
            pass
        return None
    
    def analyze(self):
        """Complete website analysis"""
        print(f"\n{'='*70}")
        print("ADVANCED WEBSITE ANALYSIS - COSMETIC-ALENA.COM")
        print(f"{'='*70}\n")
        
        print(f"📡 Fetching {self.url}...")
        response = self.fetch_url(self.url)
        
        if not response or response.status_code != 200:
            print(f"✗ Failed to fetch website (Status: {response.status_code if response else 'N/A'})")
            return False
        
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        print(f"✓ Successfully fetched ({len(html):,} bytes)\n")
        
        # Save raw HTML
        with open(f"{self.output_dir}/html/index.html", 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✓ Saved raw HTML to html/index.html")
        
        # Save pretty HTML
        with open(f"{self.output_dir}/html/index_pretty.html", 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print(f"✓ Saved formatted HTML to html/index_pretty.html\n")
        
        analysis = self.analyze_resources(soup)
        
        print("\n" + "="*70)
        print("DOWNLOADING RESOURCES")
        print("="*70 + "\n")
        
        self.download_resources(soup)
        
        print("\n" + "="*70)
        print("GENERATING REPORTS")
        print("="*70 + "\n")
        
        self.generate_reports(analysis)
        
        print(f"\n✓ Analysis complete! Files saved to '{self.output_dir}/' directory\n")
        return True
    
    def analyze_resources(self, soup):
        """Analyze all resources"""
        analysis = {
            'title': soup.title.string if soup.title else 'No Title',
            'stylesheets': [],
            'scripts': [],
            'images': [],
            'links': [],
            'forms': [],
            'fonts': [],
            'metadata': {}
        }
        
        # Stylesheets
        print("🎨 Stylesheets:")
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                analysis['stylesheets'].append({
                    'href': href,
                    'media': link.get('media', 'all'),
                    'full_url': urljoin(self.url, href)
                })
                print(f"  - {href}")
        
        # Scripts
        print(f"\n📜 Scripts: {len(soup.find_all('script'))}")
        for script in soup.find_all('script'):
            src = script.get('src')
            if src:
                analysis['scripts'].append({
                    'src': src,
                    'full_url': urljoin(self.url, src),
                    'async': script.has_attr('async'),
                    'defer': script.has_attr('defer')
                })
                print(f"  - {src}")
        
        # Images
        images = {}
        for img in soup.find_all('img'):
            src = img.get('src')
            if src and src not in images:
                images[src] = {
                    'src': src,
                    'full_url': urljoin(self.url, src),
                    'alt': img.get('alt', ''),
                    'width': img.get('width'),
                    'height': img.get('height')
                }
        analysis['images'] = list(images.values())
        print(f"\n🖼️  Images: {len(analysis['images'])}")
        
        # Links
        links = {}
        for a in soup.find_all('a'):
            href = a.get('href')
            if href and not href.startswith('#'):
                if href not in links:
                    links[href] = {
                        'href': href,
                        'text': a.get_text(strip=True),
                        'full_url': urljoin(self.url, href) if not href.startswith(('http://', 'https://')) else href
                    }
        analysis['links'] = list(links.values())
        print(f"🔗 Links: {len(analysis['links'])}")
        
        # Forms
        for form in soup.find_all('form'):
            form_fields = []
            for field in form.find_all(['input', 'textarea', 'select']):
                form_fields.append({
                    'name': field.get('name', ''),
                    'type': field.get('type', field.name)
                })
            analysis['forms'].append({
                'action': form.get('action', ''),
                'method': form.get('method', 'GET'),
                'fields': form_fields
            })
        print(f"📋 Forms: {len(analysis['forms'])}")
        
        # Google Fonts
        for link in soup.find_all('link'):
            if 'fonts.googleapis.com' in link.get('href', '') or 'fonts.gstatic.com' in link.get('href', ''):
                analysis['fonts'].append(link.get('href'))
        print(f"📝 Web Fonts: {len(analysis['fonts'])}")
        
        # Metadata
        for meta in soup.find_all('meta'):
            if meta.get('name'):
                analysis['metadata'][meta.get('name')] = meta.get('content')
        
        return analysis
    
    def download_resources(self, soup):
        """Download all resources"""
        print("CSS Files:")
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                filename = self.fetch_and_save_resource(href, f"{self.output_dir}/css", 'css')
                if filename:
                    print(f"  ✓ {filename}")
        
        print("\nJavaScript Files:")
        for script in soup.find_all('script'):
            src = script.get('src')
            if src:
                filename = self.fetch_and_save_resource(src, f"{self.output_dir}/js", 'js')
                if filename:
                    print(f"  ✓ {filename}")
        
        print("\nImages:")
        count = 0
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                filename = self.fetch_and_save_resource(src, f"{self.output_dir}/images", 'image')
                if filename and count < 10:  # Show first 10
                    print(f"  ✓ {filename}")
                    count += 1
        
        total_imgs = len(soup.find_all('img'))
        if total_imgs > 10:
            print(f"  ... and {total_imgs - 10} more images")
        
        print("\nFonts:")
        for link in soup.find_all('link'):
            href = link.get('href', '')
            if 'fonts' in href.lower():
                filename = self.fetch_and_save_resource(href, f"{self.output_dir}/fonts", 'font')
                if filename:
                    print(f"  ✓ {filename}")
    
    def generate_reports(self, analysis):
        """Generate analysis reports"""
        
        # JSON Report
        report_file = f"{self.output_dir}/reports/analysis.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False, default=str)
        print(f"✓ analysis.json - Complete analysis in JSON format")
        
        # Manifest file
        manifest = {
            'url': self.url,
            'title': analysis['title'],
            'fetched': datetime.now().isoformat(),
            'resources': {
                'stylesheets': len(analysis['stylesheets']),
                'scripts': len(analysis['scripts']),
                'images': len(analysis['images']),
                'links': len(analysis['links']),
                'forms': len(analysis['forms']),
                'fonts': len(analysis['fonts'])
            },
            'output_directory': self.output_dir
        }
        
        manifest_file = f"{self.output_dir}/MANIFEST.json"
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
        print(f"✓ MANIFEST.json - Overview of extracted resources")
        
        # Markdown Report
        md_file = f"{self.output_dir}/reports/ANALYSIS.md"
        md_content = self.generate_markdown_report(analysis)
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"✓ ANALYSIS.md - Human-readable report")
        
        # Directory listing
        listing_file = f"{self.output_dir}/reports/DIRECTORY_STRUCTURE.txt"
        with open(listing_file, 'w', encoding='utf-8') as f:
            self.write_directory_tree(f, self.output_dir, prefix='')
        print(f"✓ DIRECTORY_STRUCTURE.txt - File organization")
        
        # URLs file
        urls_file = f"{self.output_dir}/reports/ALL_URLS.txt"
        with open(urls_file, 'w', encoding='utf-8') as f:
            f.write("=== STYLESHEETS ===\n")
            for css in analysis['stylesheets']:
                f.write(f"{css['full_url']}\n")
            f.write("\n=== SCRIPTS ===\n")
            for js in analysis['scripts']:
                f.write(f"{js['full_url']}\n")
            f.write("\n=== IMAGES ===\n")
            for img in analysis['images']:
                f.write(f"{img['full_url']}\n")
            f.write("\n=== EXTERNAL LINKS ===\n")
            for link in analysis['links']:
                if link['href'].startswith(('http://', 'https://')):
                    f.write(f"{link['full_url']}\n")
        print(f"✓ ALL_URLS.txt - Complete list of all external URLs")
    
    def write_directory_tree(self, f, path, prefix=''):
        """Write directory tree structure"""
        try:
            items = sorted(os.listdir(path))
            for i, item in enumerate(items):
                item_path = os.path.join(path, item)
                is_last = i == len(items) - 1
                current_prefix = '└── ' if is_last else '├── '
                f.write(f"{prefix}{current_prefix}{item}\n")
                
                if os.path.isdir(item_path) and not item.startswith('.'):
                    next_prefix = prefix + ('    ' if is_last else '│   ')
                    self.write_directory_tree(f, item_path, next_prefix)
        except PermissionError:
            pass
    
    def generate_markdown_report(self, analysis):
        """Generate comprehensive markdown report"""
        md = f"""# Website Analysis Report

**URL:** {self.url}
**Title:** {analysis['title']}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

- **Stylesheets:** {len(analysis['stylesheets'])}
- **JavaScript Files:** {len(analysis['scripts'])}
- **Images:** {len(analysis['images'])}
- **Links:** {len(analysis['links'])}
- **Forms:** {len(analysis['forms'])}
- **Web Fonts:** {len(analysis['fonts'])}

## Stylesheets

"""
        for css in analysis['stylesheets']:
            md += f"- `{css['href']}`\n"
            md += f"  - Full URL: {css['full_url']}\n"
            md += f"  - Media: {css['media']}\n"
        
        md += "\n## JavaScript Files\n\n"
        for js in analysis['scripts']:
            attrs = []
            if js['async']: attrs.append('async')
            if js['defer']: attrs.append('defer')
            attr_str = f" ({', '.join(attrs)})" if attrs else ""
            md += f"- `{js['src']}`{attr_str}\n"
        
        md += "\n## Images\n\n"
        for img in analysis['images'][:20]:
            md += f"- {img['src']}\n"
            if img['alt']:
                md += f"  - Alt: {img['alt']}\n"
        
        if len(analysis['images']) > 20:
            md += f"\n... and {len(analysis['images']) - 20} more images\n"
        
        md += "\n## Links\n\n"
        md += "### Internal Navigation\n\n"
        for link in analysis['links'][:15]:
            if not link['href'].startswith(('http://', 'https://')):
                md += f"- [{link['text'] or link['href']}]({link['href']})\n"
        
        md += "\n### External Links\n\n"
        for link in analysis['links']:
            if link['href'].startswith(('http://', 'https://')):
                md += f"- {link['full_url']}\n"
        
        md += "\n## Forms\n\n"
        for i, form in enumerate(analysis['forms'], 1):
            md += f"### Form {i}\n\n"
            md += f"- **Action:** {form['action']}\n"
            md += f"- **Method:** {form['method']}\n"
            md += f"- **Fields:** {len(form['fields'])}\n\n"
            for field in form['fields']:
                md += f"  - `{field['name']}` ({field['type']})\n"
            md += "\n"
        
        md += "\n## Files Extracted\n\n"
        md += "- `html/index.html` - Raw HTML\n"
        md += "- `html/index_pretty.html` - Formatted HTML\n"
        md += "- `css/` - All stylesheets\n"
        md += "- `js/` - All JavaScript files\n"
        md += "- `images/` - All images\n"
        md += "- `fonts/` - All web fonts\n"
        md += "- `reports/` - Analysis reports\n"
        
        return md


if __name__ == '__main__':
    analyzer = AdvancedWebsiteAnalyzer('https://cosmetic-alena.com', 'website_content')
    analyzer.analyze()
