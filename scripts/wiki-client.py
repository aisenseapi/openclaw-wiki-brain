#!/usr/bin/env python3
"""
Wiki Client - OpenClaw Integration
Reads directly from files for speed, falls back to XML-RPC for metadata.
"""

import xmlrpc.client
import os
from pathlib import Path

# Configuration
WIKI_DIR = os.environ.get('WIKI_DIR', '/home/user/dokuwiki/data/pages')
WIKI_URL = os.environ.get('WIKI_URL', 'http://localhost:8080/lib/exe/xmlrpc.php')
WIKI_TOKEN = os.environ.get('WIKI_TOKEN', '')  # Optional

class WikiClient:
    """Client for reading/writing wiki pages."""
    
    def __init__(self):
        self.wiki_dir = Path(WIKI_DIR)
        self.use_xmlrpc = False
        self.xmlrpc = None
        
        # Try XML-RPC if token available
        if WIKI_TOKEN:
            try:
                self.xmlrpc = xmlrpc.client.ServerProxy(WIKI_URL)
                self.xmlrpc.wiki.getAllPages({}, WIKI_TOKEN)
                self.use_xmlrpc = True
            except:
                pass
    
    def get_page(self, page_name):
        """Read page content. Tries XML-RPC first, then file."""
        if self.use_xmlrpc:
            try:
                return self.xmlrpc.wiki.getPage(page_name, {}, WIKI_TOKEN)
            except:
                pass
        
        # File fallback (fastest for OpenClaw)
        page_file = self.wiki_dir / f"{page_name}.txt"
        if page_file.exists():
            return page_file.read_text()
        return None
    
    def put_page(self, page_name, content, summary=""):
        """Write page content."""
        if self.use_xmlrpc:
            try:
                return self.xmlrpc.wiki.putPage(page_name, content, {'sum': summary}, WIKI_TOKEN)
            except:
                pass
        
        # File fallback
        page_file = self.wiki_dir / f"{page_name}.txt"
        page_file.parent.mkdir(parents=True, exist_ok=True)
        page_file.write_text(content)
        return True
    
    def search(self, query):
        """Search across all pages."""
        if self.use_xmlrpc:
            try:
                return self.xmlrpc.wiki.search(query, {}, WIKI_TOKEN)
            except:
                pass
        
        # File-based search
        results = []
        for txt_file in self.wiki_dir.rglob("*.txt"):
            try:
                content = txt_file.read_text()
                if query.lower() in content.lower():
                    results.append({
                        'id': txt_file.stem,
                        'snippet': content[:200]
                    })
            except:
                pass
        return results
    
    def list_pages(self):
        """List all pages."""
        if self.use_xmlrpc:
            try:
                pages = self.xmlrpc.wiki.getAllPages({}, WIKI_TOKEN)
                return [p['id'] for p in pages]
            except:
                pass
        
        # File listing
        pages = []
        for txt_file in self.wiki_dir.rglob("*.txt"):
            rel = txt_file.relative_to(self.wiki_dir)
            pages.append(str(rel.with_suffix('')))
        return sorted(pages)

if __name__ == "__main__":
    client = WikiClient()
    print("=== Wiki Client ===")
    print(f"Mode: {'XML-RPC' if client.use_xmlrpc else 'File-based'}")
    print(f"\nPages: {len(client.list_pages())}")
    print(f"Sample search for 'docker': {len(client.search('docker'))} matches")