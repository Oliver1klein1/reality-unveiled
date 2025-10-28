#!/usr/bin/env python3
"""
Amazon KDP-Compliant EPUB Creator
Creates EPUB files specifically optimized for Amazon KDP with proper metadata and mimetype ordering.
"""

import json
import os
import shutil
import zipfile
import re
from pathlib import Path
from datetime import datetime

def load_metadata():
    """Load book metadata from JSON file."""
    if not os.path.exists('book_metadata.json'):
        print("❌ No metadata file found. Run 'python check_metadata.py' first.")
        return None
    
    with open('book_metadata.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def fix_spine_order():
    """Ensure spine order is correct and not alphabetical"""
    content_opf_path = "epub/OEBPS/content.opf"
    
    if not os.path.exists(content_opf_path):
        return
    
    with open(content_opf_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define the correct reading order
    # Note: "cover" is NOT included in spine - only in guide section
    correct_order = [
        "copyright",
        "toc",
        "introduction",
        "part1",
        "chapter1",
        "chapter2",
        "part2",
        "chapter3",
        "part3",
        "chapter4",
        "chapter5",
        "part4",
        "chapter6",
        "chapter7",
        "chapter8",
        "chapter9",
        "conclusion",
        "other-books",
        "appendix",
        "bibliography"
    ]
    
    # Find the spine section
    spine_start = content.find('<spine toc="ncx">')
    spine_end = content.find('</spine>')
    
    if spine_start == -1 or spine_end == -1:
        print("⚠️ Could not find spine section")
        return
    
    # Extract everything before and after spine
    before_spine = content[:spine_start + len('<spine toc="ncx">')]
    after_spine = content[spine_end:]
    
    # Create new spine with correct order
    new_spine_lines = []
    for item_id in correct_order:
        new_spine_lines.append(f'    <itemref idref="{item_id}"/>')
    
    new_spine_content = before_spine + '\n' + '\n'.join(new_spine_lines) + '\n    ' + after_spine
    
    # Write the corrected content back
    with open(content_opf_path, 'w', encoding='utf-8') as f:
        f.write(new_spine_content)
    
    print("✅ Fixed spine order to prevent alphabetical sorting")

def create_kdp_content_opf(metadata):
    """Create content.opf file with complete metadata for Amazon KDP."""
    
    # Generate unique identifiers
    book_id = f"book_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Get all XHTML files from Text directory
    text_dir = Path('epub/OEBPS/Text')
    xhtml_files = list(text_dir.glob('*.xhtml'))
    
    # Get all image files (using lowercase 'images')
    images_dir = Path('epub/OEBPS/images')
    image_files = list(images_dir.glob('*'))
    
    # Create manifest items
    manifest_items = []
    spine_items = []
    
    # Note: cover.xhtml is NOT included - it causes issues in EPUB readers
    # The cover image is specified via the <meta name="cover" content="cover-image"/> tag
    
    # Add XHTML files to manifest
    for xhtml_file in sorted(xhtml_files):
        file_id = xhtml_file.stem
        manifest_items.append(f'    <item id="{file_id}" href="Text/{xhtml_file.name}" media-type="application/xhtml+xml"/>')
    
    # Get spine order from fix_spine_order function
    # Note: "cover" is NOT included in spine - it's only in the guide section
    correct_order = [
        "copyright", "toc", "introduction",
        "part1", "chapter1", "chapter2", 
        "part2", "chapter3",
        "part3", "chapter4", "chapter5",
        "part4", "chapter6", "chapter7", "chapter8", "chapter9",
        "conclusion", "other-books", "appendix", "bibliography"
    ]
    
    # Add spine items in correct order
    for item_id in correct_order:
        spine_items.append(f'    <itemref idref="{item_id}"/>')
    
    # Add images to manifest
    used_ids = set()  # Track used IDs to prevent duplicates
    # Reserve 'cover' ID for cover.xhtml and 'cover-image' for cover.jpg
    used_ids.add('cover')
    used_ids.add('cover-image')
    
    # Get cover filename from metadata
    cover_filename = os.path.basename(metadata.get('cover_image', ''))
    
    for image_file in image_files:
        # Skip cover.jpg as it's already added as 'cover-image'
        if image_file.name == cover_filename:
            continue
            
        # Create unique ID by adding extension if needed
        base_id = image_file.stem
        file_id = base_id
        
        # Handle duplicate IDs by adding extension
        counter = 1
        while file_id in used_ids:
            file_id = f"{base_id}_{counter}"
            counter += 1
        
        used_ids.add(file_id)
        
        if image_file.suffix.lower() in ['.jpg', '.jpeg']:
            media_type = 'image/jpeg'
        elif image_file.suffix.lower() == '.png':
            media_type = 'image/png'
        else:
            media_type = 'image/png'  # Default
        
        manifest_items.append(f'    <item id="{file_id}" href="images/{image_file.name}" media-type="{media_type}"/>')
    
    # Add CSS file
    manifest_items.append('    <item id="css" href="Styles/style.css" media-type="text/css"/>')
    
    # Create content.opf
    content_opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="book-id" version="2.0">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
        <dc:identifier id="book-id" opf:scheme="UUID">{book_id}</dc:identifier>
        <dc:title>{metadata.get('title', 'Untitled')}</dc:title>
        <dc:creator opf:file-as="{metadata.get('author', 'Unknown')}" opf:role="aut">{metadata.get('author', 'Unknown')}</dc:creator>
        <dc:publisher>{metadata.get('publisher', 'Unknown Publisher')}</dc:publisher>
        <dc:date opf:event="publication">{metadata.get('publication_date', '2025')}</dc:date>
        <dc:language>{metadata.get('language', 'en')}</dc:language>
        <dc:subject>{metadata.get('tags', '')}</dc:subject>
        <dc:description>{metadata.get('description', '')}</dc:description>
        <meta name="cover" content="cover-image"/>
        <meta name="generator" content="KDP EPUB Creator"/>
    </metadata>
    
    <manifest>
        <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
        <item id="cover-image" href="images/{os.path.basename(metadata.get('cover_image', ''))}" media-type="image/jpeg"/>
{chr(10).join(manifest_items)}
    </manifest>
    
    <spine toc="ncx">
{chr(10).join(spine_items)}
    </spine>
    
    <guide>
        <reference type="toc" title="Table of Contents" href="Text/toc.xhtml"/>
    </guide>
</package>'''
    
    return content_opf

def create_kdp_epub(metadata):
    """Create Amazon KDP-compliant EPUB file."""
    
    print("🚀 Creating Amazon KDP-compliant EPUB...")
    
    # Ensure epub directory exists
    if not os.path.exists('epub'):
        print("❌ EPUB directory not found. Run conversion scripts first.")
        return False
    
    # Create content.opf with metadata
    content_opf = create_kdp_content_opf(metadata)
    
    # Write content.opf
    with open('epub/OEBPS/content.opf', 'w', encoding='utf-8') as f:
        f.write(content_opf)
    
    # Fix spine order to prevent alphabetical sorting
    fix_spine_order()
    
    # Create EPUB file with proper mimetype ordering
    epub_filename = f"{metadata.get('title', 'Book').replace(' ', '_')}_KDP.epub"
    
    with zipfile.ZipFile(epub_filename, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as epub:
        # CRITICAL: Add mimetype first (Amazon KDP requirement)
        epub.write('epub/mimetype', 'mimetype', compress_type=zipfile.ZIP_STORED)
        
        # Add META-INF files
        epub.write('epub/META-INF/container.xml', 'META-INF/container.xml')
        
        # Add OEBPS files
        for root, dirs, files in os.walk('epub/OEBPS'):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, 'epub')
                epub.write(file_path, arc_path)
    
    print(f"✅ Amazon KDP-compliant EPUB created: {epub_filename}")
    
    # Verify mimetype is first
    with zipfile.ZipFile(epub_filename, 'r') as epub:
        file_list = epub.namelist()
        if file_list[0] == 'mimetype':
            print("✅ Mimetype file is first (Amazon KDP compliant)")
        else:
            print(f"❌ Warning: Mimetype is not first. First file: {file_list[0]}")
    
    return True

def main():
    """Main function to create KDP-compliant EPUB."""
    print("📚 Amazon KDP EPUB Creator")
    print("=" * 40)
    
    # Load metadata
    metadata = load_metadata()
    if not metadata:
        return False
    
    # Create KDP EPUB
    success = create_kdp_epub(metadata)
    
    if success:
        print("\n🎉 Amazon KDP-compliant EPUB creation complete!")
        print("\nNext steps:")
        print("1. Test the EPUB in Kindle Previewer")
        print("2. Upload to Amazon KDP")
        print("3. Verify all metadata displays correctly")
    else:
        print("\n❌ EPUB creation failed")
    
    return success

if __name__ == "__main__":
    main()
