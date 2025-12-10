#!/usr/bin/env python3
"""
Enhanced EPUB Conversion Script for Escape The Hell Myth
Converts HTML files to EPUB-compatible XHTML format while preserving ALL styling
"""

import os
import re
from bs4 import BeautifulSoup
import shutil
import json

def convert_html_to_xhtml_enhanced(html_file_path, output_dir):
    """Convert a single HTML file to EPUB-compatible XHTML while preserving all styling"""
    
    # Read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extract the title
    title_tag = soup.find('title')
    title = title_tag.get_text() if title_tag else "Chapter"
    
    # Extract the body content
    body = soup.find('body')
    if not body:
        return None
    
    # Clean up the content for EPUB while preserving styling
    # Remove navigation elements but keep everything else
    for nav in body.find_all(['div'], class_=['navigation']):
        nav.decompose()
    
    # Also remove any standalone navigation links
    for nav_link in body.find_all(['a'], class_=['nav-link']):
        nav_link.decompose()
    
    # Remove navigation buttons (the nav-buttons divs with Previous/Next buttons)
    for nav_buttons in body.find_all(['div'], class_=['navigation-buttons']):
        nav_buttons.decompose()
    
    # Remove any divs containing navigation-buttons
    for nav_container in body.find_all('div', class_=lambda x: x and 'navigation' in x):
        if 'Previous' in nav_container.get_text() or 'Next' in nav_container.get_text():
            nav_container.decompose()
    
    # Remove sections with "no-print" class (usually contain navigation)
    for no_print in body.find_all('section', class_=['no-print']):
        no_print.decompose()
    
    # Remove any comments about navigation
    from bs4 import Comment
    for comment in body.find_all(string=lambda text: isinstance(text, Comment)):
        if 'navigation' in comment.lower() or 'Navigation' in comment:
            comment.extract()
    
    # Remove entire comment blocks that precede navigation sections
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        if 'Navigation' in comment:
            # Get the next sibling element if it's navigation
            if hasattr(comment, 'next_sibling'):
                next_elem = comment.next_sibling
                while next_elem and hasattr(next_elem, 'name') and next_elem.name in ['section', 'div']:
                    if 'navigation' in str(next_elem.get('class', [])).lower() or 'Previous' in str(next_elem) or 'Next' in str(next_elem):
                        next_elem.decompose()
                        break
                    next_elem = next_elem.next_sibling
    
    # Update image src paths to EPUB format
    for img in body.find_all('img'):
        src = img.get('src', '')
        if src.startswith('.') or not src.startswith('../'):
            # Update to proper EPUB image path
            img['src'] = f"../images/{os.path.basename(src)}"
    
    # Update internal links from .html to .xhtml for EPUB compatibility
    for link in body.find_all('a', href=True):
        href = link.get('href', '')
        # Only update links that point to .html files (internal links)
        if href.endswith('.html') and not href.startswith('http'):
            link['href'] = href.replace('.html', '.xhtml')
    
    # Extract any inline styles from the original HTML
    style_content = ""
    style_tag = soup.find('style')
    if style_tag:
        style_content = str(style_tag)
    
    # Create XHTML structure with preserved styling
    xhtml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{title}</title>
    <link rel="stylesheet" type="text/css" href="../Styles/style.css"/>
    {style_content}
</head>
<body>
{str(body)}
</body>
</html>'''
    
    # Clean up the XHTML - but PRESERVE classes and styles
    xhtml_content = xhtml_content.replace('&nbsp;', '&#160;')  # Fix entities
    xhtml_content = xhtml_content.replace('&amp;', '&amp;')  # Ensure proper entity encoding
    
    # Get the filename for output
    filename = os.path.basename(html_file_path).replace('.html', '.xhtml')
    output_path = os.path.join(output_dir, filename)
    
    # Write the XHTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xhtml_content)
    
    return filename

def verify_html_xhtml_match(html_file, xhtml_file):
    """Verify that XHTML file matches HTML file content"""
    print(f"Verifying {html_file} vs {xhtml_file}...")
    
    # Read both files
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    with open(xhtml_file, 'r', encoding='utf-8') as f:
        xhtml_content = f.read()
    
    # Parse both files
    html_soup = BeautifulSoup(html_content, 'html.parser')
    xhtml_soup = BeautifulSoup(xhtml_content, 'html.parser')
    
    # Extract body content
    html_body = html_soup.find('body')
    xhtml_body = xhtml_soup.find('body')
    
    if not html_body or not xhtml_body:
        print(f"  ❌ Missing body content")
        return False
    
    # Check for key elements and classes
    issues = []

    def remove_navigation_elements(body_tag):
        """Strip navigation-related elements so counts align with EPUB output."""
        for selector in [
            ('div', 'navigation'),
            ('a', 'nav-link'),
            ('div', 'navigation-buttons'),
            ('section', 'no-print'),
        ]:
            for elem in body_tag.find_all(selector[0], class_=lambda x: x and selector[1] in x):
                elem.decompose()

    # Remove navigation elements from HTML body to mirror EPUB cleanup
    remove_navigation_elements(html_body)
    remove_navigation_elements(xhtml_body)
    
    # Check for bible-quote classes
    html_quotes = html_body.find_all('div', class_='bible-quote')
    xhtml_quotes = xhtml_body.find_all('div', class_='bible-quote')
    
    if len(html_quotes) != len(xhtml_quotes):
        issues.append(f"Bible quote count mismatch: HTML has {len(html_quotes)}, XHTML has {len(xhtml_quotes)}")
    
    # Check for other important classes
    important_classes = ['bible-quote', 'highlight', 'callout', 'emphasis']
    for class_name in important_classes:
        html_elements = html_body.find_all(class_=class_name)
        xhtml_elements = xhtml_body.find_all(class_=class_name)
        
        if len(html_elements) != len(xhtml_elements):
            issues.append(f"{class_name} class count mismatch: HTML has {len(html_elements)}, XHTML has {len(xhtml_elements)}")
    
    # Check for inline styles
    html_styled = html_body.find_all(attrs={'style': True})
    xhtml_styled = xhtml_body.find_all(attrs={'style': True})
    
    if len(html_styled) != len(xhtml_styled):
        issues.append(f"Inline style count mismatch: HTML has {len(html_styled)}, XHTML has {len(xhtml_styled)}")
    
    # Check for images
    html_images = html_body.find_all('img')
    xhtml_images = xhtml_body.find_all('img')
    
    if len(html_images) != len(xhtml_images):
        issues.append(f"Image count mismatch: HTML has {len(html_images)}, XHTML has {len(xhtml_images)}")
    
    if issues:
        print(f"  ❌ Issues found:")
        for issue in issues:
            print(f"    - {issue}")
        return False
    else:
        print(f"  ✅ Content matches")
        return True

def main():
    # Define paths
    epub_dir = "epub"
    oebps_dir = os.path.join(epub_dir, "OEBPS")
    text_dir = os.path.join(oebps_dir, "Text")
    images_dir = os.path.join(oebps_dir, "images")
    meta_inf_dir = os.path.join(epub_dir, "META-INF")
    
    # Create directories if they don't exist
    os.makedirs(text_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(meta_inf_dir, exist_ok=True)
    
    # Copy styles.css from existing epub if it exists
    existing_styles = os.path.join("reality-unveiled-epub", "OEBPS", "styles.css")
    if os.path.exists(existing_styles):
        styles_dir = os.path.join(oebps_dir, "Styles")
        os.makedirs(styles_dir, exist_ok=True)
        shutil.copy2(existing_styles, os.path.join(styles_dir, "style.css"))
        print("✅ Copied styles.css")
    
    # Create mimetype file
    mimetype_file = os.path.join(epub_dir, "mimetype")
    with open(mimetype_file, 'w', encoding='ascii') as f:
        f.write("application/epub+zip")
    
    # Create container.xml
    container_xml = os.path.join(meta_inf_dir, "container.xml")
    with open(container_xml, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n')
        f.write('    <rootfiles>\n')
        f.write('        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>\n')
        f.write('    </rootfiles>\n')
        f.write('</container>\n')
    
    # Create toc.ncx placeholder (will be generated later)
    toc_ncx = os.path.join(oebps_dir, "toc.ncx")
    if not os.path.exists(toc_ncx):
        with open(toc_ncx, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n')
            f.write('    <head>\n')
            f.write('        <meta name="dtb:uid" content="reality-unveiled-2025"/>\n')
            f.write('        <meta name="dtb:depth" content="1"/>\n')
            f.write('    </head>\n')
            f.write('    <docTitle><text>Reality Unveiled</text></docTitle>\n')
            f.write('    <navMap>\n')
            f.write('    </navMap>\n')
            f.write('</ncx>\n')
    
    # Files to process (in order)
    files_to_process = [
        "cover.html",
        "titlepage.html",
        "copyright.html",
        "dedication.html",
        "toc.html",
        "introduction.html",
        "part1.html",
        "chapter1.html", "chapter2.html",
        "part2.html",
        "chapter3.html",
        "part3.html",
        "chapter4.html", "chapter5.html",
        "part4.html",
        "chapter6.html", "chapter7.html", "chapter8.html", "chapter9.html",
        "conclusion.html",
        "other-books.html",
        "appendix.html",
        "bibliography.html"
    ]
    
    print("🔄 Converting HTML files to XHTML with preserved styling...")
    
    # Convert HTML files to XHTML
    converted_files = []
    for html_file in files_to_process:
        if os.path.exists(html_file):
            print(f"Converting {html_file}...")
            xhtml_filename = convert_html_to_xhtml_enhanced(html_file, text_dir)
            if xhtml_filename:
                converted_files.append((html_file, xhtml_filename))
        else:
            print(f"Warning: {html_file} not found")
    
    # Copy images to EPUB Images directory
    print("\n🖼️ Copying images...")
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg']
    for file in os.listdir('.'):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            print(f"Copying image {file}...")
            shutil.copy2(file, images_dir)
    
    # Verify conversions
    print("\n🔍 Verifying conversions...")
    verification_results = []
    for html_file, xhtml_filename in converted_files:
        xhtml_path = os.path.join(text_dir, xhtml_filename)
        if os.path.exists(xhtml_path):
            result = verify_html_xhtml_match(html_file, xhtml_path)
            verification_results.append((html_file, result))
        else:
            print(f"  ❌ XHTML file not found: {xhtml_filename}")
            verification_results.append((html_file, False))
    
    # Summary
    print("\n📊 Conversion Summary:")
    successful_conversions = sum(1 for _, result in verification_results if result)
    total_conversions = len(verification_results)
    
    print(f"✅ Successful conversions: {successful_conversions}/{total_conversions}")
    
    if successful_conversions < total_conversions:
        print("\n❌ Files with issues:")
        for html_file, result in verification_results:
            if not result:
                print(f"  - {html_file}")
    
    print("\n✨ Enhanced conversion complete!")
    return successful_conversions == total_conversions

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n⚠️ Some files had conversion issues. Please review the output above.")
        exit(1)
