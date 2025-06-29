#!/usr/bin/env python3
"""
Simple script to test if all internal links in the new homepage exist
"""
import os
import re
from pathlib import Path

def test_internal_links():
    """Test if all internal links in index.html point to existing files"""
    
    # Read the index.html file
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all internal links (href="/...")
    internal_links = re.findall(r'href="(/[^"]*)"', content)
    
    print("Testing internal links in index.html:")
    print("=" * 50)
    
    missing_links = []
    existing_links = []
    
    for link in internal_links:
        # Remove leading slash and convert to local path
        local_path = link.lstrip('/')
        
        # Check if it's a directory link (ends with /)
        if local_path.endswith('/'):
            # Check for index.html in that directory
            index_path = os.path.join(local_path, 'index.html')
            if os.path.exists(index_path):
                existing_links.append(f"{link} -> {index_path}")
            else:
                missing_links.append(f"{link} -> {index_path}")
        else:
            # Check if the file exists directly
            if os.path.exists(local_path):
                existing_links.append(f"{link} -> {local_path}")
            else:
                # Try adding index.html
                index_path = os.path.join(local_path, 'index.html')
                if os.path.exists(index_path):
                    existing_links.append(f"{link} -> {index_path}")
                else:
                    missing_links.append(f"{link} -> {local_path}")
    
    print(f"✅ EXISTING LINKS ({len(existing_links)}):")
    for link in existing_links:
        print(f"  {link}")
    
    if missing_links:
        print(f"\n❌ MISSING LINKS ({len(missing_links)}):")
        for link in missing_links:
            print(f"  {link}")
    else:
        print(f"\n🎉 All {len(existing_links)} internal links are valid!")
    
    return len(missing_links) == 0

if __name__ == "__main__":
    success = test_internal_links()
    exit(0 if success else 1)
