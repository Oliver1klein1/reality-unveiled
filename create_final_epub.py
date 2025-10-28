#!/usr/bin/env python3
"""
Create EPUB file with proper file order for Amazon KDP
"""

import zipfile
import os
import shutil
import re

def fix_content_opf_duplicates():
    """Fix duplicate IDs in content.opf file"""
    content_opf_path = "epub/OEBPS/content.opf"
    
    if not os.path.exists(content_opf_path):
        return
    
    with open(content_opf_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all item IDs and fix duplicates
    used_ids = set()
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        if '<item id=' in line:
            # Extract the ID
            match = re.search(r'<item id="([^"]+)"', line)
            if match:
                original_id = match.group(1)
                file_id = original_id
                
                # Handle duplicate IDs
                counter = 1
                while file_id in used_ids:
                    file_id = f"{original_id}_{counter}"
                    counter += 1
                
                used_ids.add(file_id)
                
                # Replace the ID in the line
                line = line.replace(f'id="{original_id}"', f'id="{file_id}"')
        
        fixed_lines.append(line)
    
    # Write the fixed content back
    with open(content_opf_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed_lines))
    
    print("✅ Fixed duplicate IDs in content.opf")

def fix_spine_order():
    """Ensure spine order is correct and not alphabetical"""
    content_opf_path = "epub/OEBPS/content.opf"
    
    if not os.path.exists(content_opf_path):
        return
    
    with open(content_opf_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define the correct reading order
    correct_order = [
        "cover",
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

def create_epub():
    # Remove existing EPUB if it exists
    if os.path.exists("Reality_Unveiled_Final.epub"):
        os.remove("Reality_Unveiled_Final.epub")
    
    # Fix duplicate IDs and spine order in content.opf before creating EPUB
    fix_content_opf_duplicates()
    fix_spine_order()
    
    # Create EPUB file
    with zipfile.ZipFile("Reality_Unveiled_Final.epub", 'w', zipfile.ZIP_DEFLATED) as epub:
        
        # Add mimetype first, uncompressed (EPUB requirement)
        epub.write("epub/mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        
        # Add META-INF directory
        for root, dirs, files in os.walk("epub/META-INF"):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, "epub")
                epub.write(file_path, arc_path)
        
        # Add OEBPS directory
        for root, dirs, files in os.walk("epub/OEBPS"):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, "epub")
                epub.write(file_path, arc_path)
    
    print("EPUB created successfully: Reality_Unveiled_Final.epub")
    
    # Verify the structure
    print("\nVerifying EPUB structure...")
    with zipfile.ZipFile("Reality_Unveiled_Final.epub", 'r') as epub:
        file_list = epub.namelist()
        
        # Check that mimetype is first
        if file_list[0] == "mimetype":
            print("✓ mimetype file is first (EPUB requirement met)")
        else:
            print("✗ mimetype file is not first")
        
        # Check for required files
        required_files = [
            "mimetype",
            "META-INF/container.xml",
            "OEBPS/content.opf",
            "OEBPS/nav.xhtml",
            "OEBPS/toc.ncx",
            "OEBPS/styles.css",
            "OEBPS/images/reality-unveiled-cover.jpg"
        ]
        
        for file in required_files:
            if file in file_list:
                print(f"✓ {file}")
            else:
                print(f"✗ {file}")
        
        print(f"\nTotal files in EPUB: {len(file_list)}")
        
        print("\nFirst 10 files in EPUB:")
        for i, file in enumerate(file_list[:10]):
            print(f"{i+1}. {file}")

if __name__ == "__main__":
    create_epub()