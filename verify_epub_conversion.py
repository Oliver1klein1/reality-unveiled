#!/usr/bin/env python3
"""
EPUB Verification Script
Automatically compares HTML source files with their XHTML EPUB counterparts
to ensure styling and content are preserved
"""

import os
import re
from bs4 import BeautifulSoup
import json
from datetime import datetime

def analyze_html_file(file_path):
    """Analyze an HTML file and extract key styling information"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    body = soup.find('body')
    
    if not body:
        return None
    
    analysis = {
        'file': file_path,
        'classes': {},
        'inline_styles': 0,
        'images': 0,
        'bible_quotes': 0,
        'total_elements': 0,
        'has_style_tag': bool(soup.find('style'))
    }
    
    # Count elements with classes
    for element in body.find_all():
        analysis['total_elements'] += 1
        
        if element.get('class'):
            for class_name in element.get('class'):
                analysis['classes'][class_name] = analysis['classes'].get(class_name, 0) + 1
        
        if element.get('style'):
            analysis['inline_styles'] += 1
        
        if element.name == 'img':
            analysis['images'] += 1
        
        if element.get('class') and 'bible-quote' in element.get('class'):
            analysis['bible_quotes'] += 1
    
    return analysis

def compare_html_xhtml(html_file, xhtml_file):
    """Compare HTML and XHTML files for styling consistency"""
    html_analysis = analyze_html_file(html_file)
    xhtml_analysis = analyze_html_file(xhtml_file)
    
    if not html_analysis or not xhtml_analysis:
        return {'status': 'error', 'message': 'Could not analyze one or both files'}
    
    issues = []
    
    # Compare class usage (ignore navigation classes as they should be removed for EPUB)
    html_classes = set(html_analysis['classes'].keys())
    xhtml_classes = set(xhtml_analysis['classes'].keys())
    
    # Remove navigation classes from comparison as they should be removed for EPUB
    navigation_classes = {'navigation', 'nav-link'}
    html_classes = html_classes - navigation_classes
    xhtml_classes = xhtml_classes - navigation_classes
    
    missing_classes = html_classes - xhtml_classes
    extra_classes = xhtml_classes - html_classes
    
    if missing_classes:
        issues.append(f"Missing classes in XHTML: {', '.join(missing_classes)}")
    
    if extra_classes:
        issues.append(f"Extra classes in XHTML: {', '.join(extra_classes)}")
    
    # Compare class counts
    for class_name in html_classes & xhtml_classes:
        html_count = html_analysis['classes'][class_name]
        xhtml_count = xhtml_analysis['classes'][class_name]
        if html_count != xhtml_count:
            issues.append(f"Class '{class_name}' count mismatch: HTML={html_count}, XHTML={xhtml_count}")
    
    # Compare other metrics (account for navigation elements being removed)
    # Count navigation elements with inline styles in HTML
    html_soup = BeautifulSoup(open(html_file, 'r', encoding='utf-8').read(), 'html.parser')
    html_nav_styles = 0
    for element in html_soup.find('body').find_all(['div', 'a'], class_=['navigation', 'nav-link']):
        if element.get('style'):
            html_nav_styles += 1
    
    # Adjust HTML count by removing navigation styles
    adjusted_html_styles = html_analysis['inline_styles'] - html_nav_styles
    
    if adjusted_html_styles != xhtml_analysis['inline_styles']:
        issues.append(f"Inline styles count mismatch: HTML={adjusted_html_styles} (after removing {html_nav_styles} nav styles), XHTML={xhtml_analysis['inline_styles']}")
    
    if html_analysis['images'] != xhtml_analysis['images']:
        issues.append(f"Images count mismatch: HTML={html_analysis['images']}, XHTML={xhtml_analysis['images']}")
    
    if html_analysis['bible_quotes'] != xhtml_analysis['bible_quotes']:
        issues.append(f"Bible quotes count mismatch: HTML={html_analysis['bible_quotes']}, XHTML={xhtml_analysis['bible_quotes']}")
    
    return {
        'status': 'success' if not issues else 'issues',
        'issues': issues,
        'html_analysis': html_analysis,
        'xhtml_analysis': xhtml_analysis
    }

def generate_verification_report():
    """Generate a comprehensive verification report"""
    print("🔍 EPUB Verification Report")
    print("=" * 50)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Files to check
    files_to_check = [
        "copyright.html",
        "introduction.html",
        "toc.html",
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
    
    epub_text_dir = "epub/OEBPS/Text"
    results = []
    
    for html_file in files_to_check:
        if not os.path.exists(html_file):
            print(f"❌ {html_file}: Source file not found")
            continue
        
        xhtml_file = os.path.join(epub_text_dir, html_file.replace('.html', '.xhtml'))
        if not os.path.exists(xhtml_file):
            print(f"❌ {html_file}: XHTML file not found")
            continue
        
        print(f"🔍 Checking {html_file}...")
        result = compare_html_xhtml(html_file, xhtml_file)
        results.append((html_file, result))
        
        if result['status'] == 'success':
            print(f"  ✅ Perfect match")
        elif result['status'] == 'issues':
            print(f"  ⚠️ Issues found:")
            for issue in result['issues']:
                print(f"    - {issue}")
        else:
            print(f"  ❌ Error: {result['message']}")
    
    # Summary
    print("\n📊 Summary:")
    successful = sum(1 for _, result in results if result['status'] == 'success')
    with_issues = sum(1 for _, result in results if result['status'] == 'issues')
    errors = sum(1 for _, result in results if result['status'] == 'error')
    
    print(f"✅ Perfect matches: {successful}")
    print(f"⚠️ Files with issues: {with_issues}")
    print(f"❌ Errors: {errors}")
    
    if with_issues > 0:
        print("\n🔧 Files needing attention:")
        for html_file, result in results:
            if result['status'] == 'issues':
                print(f"  - {html_file}")
    
    return results

def main():
    """Main verification function"""
    if not os.path.exists("epub/OEBPS/Text"):
        print("❌ EPUB Text directory not found. Run the conversion script first.")
        return False
    
    results = generate_verification_report()
    
    # Check if all files passed
    all_passed = all(result['status'] == 'success' for _, result in results)
    
    if all_passed:
        print("\n🎉 All files passed verification!")
        return True
    else:
        print("\n⚠️ Some files need attention. Review the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
