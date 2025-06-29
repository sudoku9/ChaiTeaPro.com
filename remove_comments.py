#!/usr/bin/env python3
"""
Script to remove comment sections from all article HTML files
"""
import os
import re
from pathlib import Path

def remove_comments_from_file(file_path):
    """Remove comment sections from a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove comment-related CSS link
        content = re.sub(r'<link rel="stylesheet" id="kadence-comments-css"[^>]*>\n?', '', content)
        
        # Remove comment feed links
        content = re.sub(r'<link rel="alternate"[^>]*Comments Feed[^>]*>\n?', '', content)
        
        # Remove comment-reply script
        content = re.sub(r'<script src="[^"]*comment-reply[^"]*"[^>]*></script>\n?', '', content)
        
        # Remove the entire comments section
        # This pattern matches from <div id="comments" to the closing </div>
        comment_pattern = r'<div id="comments" class="comments-area">.*?</div>\s*<!-- #comments -->'
        content = re.sub(comment_pattern, '', content, flags=re.DOTALL)
        
        # Alternative pattern for respond section
        respond_pattern = r'<div id="respond" class="comment-respond">.*?</div>\s*<!-- #respond -->'
        content = re.sub(respond_pattern, '', content, flags=re.DOTALL)
        
        # Remove any remaining comment-related divs
        content = re.sub(r'<div[^>]*comments-area[^>]*>.*?</div>', '', content, flags=re.DOTALL)
        
        # Clean up extra whitespace
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all article files"""
    current_dir = Path('.')
    processed_files = []
    
    # Find all article directories (those containing index.html)
    for item in current_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.') and not item.name.startswith('wp-'):
            index_file = item / 'index.html'
            if index_file.exists():
                print(f"Processing: {item.name}")
                if remove_comments_from_file(index_file):
                    processed_files.append(str(item.name))
                    print(f"  ✅ Removed comments from {item.name}")
                else:
                    print(f"  ⚠️  No changes needed for {item.name}")
    
    print(f"\n🎉 Processed {len(processed_files)} files:")
    for file in processed_files:
        print(f"  - {file}")

if __name__ == "__main__":
    main()
