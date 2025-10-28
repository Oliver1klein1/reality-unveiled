#!/usr/bin/env python3
"""
Metadata Checker for EPUB Creation
Checks for required metadata and prompts for missing information.
"""

import json
import os
import sys
from pathlib import Path

def check_metadata_file():
    """Check if metadata file exists and is valid."""
    metadata_files = ['book_metadata.json', 'metadata.txt']
    
    for file in metadata_files:
        if os.path.exists(file):
            print(f"✅ Found metadata file: {file}")
            return file
    
    print("❌ No metadata file found")
    return None

def load_json_metadata(file_path):
    """Load metadata from JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        return metadata
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"❌ Error loading {file_path}: {e}")
        return None

def check_required_metadata(metadata):
    """Check if all required metadata is present."""
    required_fields = {
        'title': 'Book Title',
        'author': 'Author Name',
        'publisher': 'Publisher Name',
        'publication_date': 'Publication Year',
        'cover_image': 'Cover Image Path'
    }
    
    missing_fields = []
    
    for field, description in required_fields.items():
        if field not in metadata or not metadata[field]:
            missing_fields.append((field, description))
    
    return missing_fields

def prompt_for_missing_metadata(missing_fields):
    """Prompt user for missing metadata."""
    print("\n" + "="*60)
    print("MISSING METADATA DETECTED")
    print("="*60)
    print("Please provide the following information:\n")
    
    metadata = {}
    
    for field, description in missing_fields:
        while True:
            value = input(f"{description}: ").strip()
            if value:
                metadata[field] = value
                break
            print("❌ This field is required. Please provide a value.")
    
    # Ask for optional fields
    print("\nOptional fields (press Enter to skip):")
    optional_fields = {
        'subtitle': 'Book Subtitle',
        'tags': 'Keywords/Tags (comma-separated)',
        'description': 'Book Description',
        'language': 'Language (default: en)',
        'isbn': 'ISBN Number'
    }
    
    for field, description in optional_fields.items():
        value = input(f"{description}: ").strip()
        if value:
            metadata[field] = value
        elif field == 'language':
            metadata[field] = 'en'  # Default language
    
    return metadata

def save_metadata(metadata, file_path='book_metadata.json'):
    """Save metadata to JSON file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        print(f"✅ Metadata saved to {file_path}")
        return True
    except Exception as e:
        print(f"❌ Error saving metadata: {e}")
        return False

def check_cover_image(cover_path):
    """Check if cover image exists and meets requirements."""
    if not cover_path:
        return False, "No cover image path provided"
    
    if not os.path.exists(cover_path):
        return False, f"Cover image not found: {cover_path}"
    
    # Check file size
    file_size = os.path.getsize(cover_path)
    if file_size > 5 * 1024 * 1024:  # 5MB
        return False, f"Cover image too large: {file_size / (1024*1024):.1f}MB (max 5MB)"
    
    # Check file extension
    ext = Path(cover_path).suffix.lower()
    if ext not in ['.jpg', '.jpeg', '.png']:
        return False, f"Cover image format not supported: {ext} (use JPG or PNG)"
    
    return True, "Cover image OK"

def main():
    """Main function to check metadata completeness."""
    print("🔍 Checking EPUB metadata...")
    
    # Check for existing metadata file
    metadata_file = check_metadata_file()
    metadata = {}
    
    if metadata_file:
        if metadata_file.endswith('.json'):
            metadata = load_json_metadata(metadata_file)
            if not metadata:
                return False
        else:
            print("❌ Only JSON metadata files are supported")
            return False
    
    # Check required fields
    missing_fields = check_required_metadata(metadata)
    
    if missing_fields:
        print(f"\n❌ Missing {len(missing_fields)} required fields")
        new_metadata = prompt_for_missing_metadata(missing_fields)
        
        # Merge with existing metadata
        metadata.update(new_metadata)
        
        # Save updated metadata
        if not save_metadata(metadata):
            return False
    
    # Check cover image
    if 'cover_image' in metadata:
        cover_ok, cover_msg = check_cover_image(metadata['cover_image'])
        if cover_ok:
            print(f"✅ {cover_msg}")
        else:
            print(f"❌ {cover_msg}")
            return False
    
    # Display final metadata
    print("\n" + "="*60)
    print("METADATA SUMMARY")
    print("="*60)
    
    for key, value in metadata.items():
        if key == 'cover_image':
            print(f"{key.title()}: {os.path.basename(value)}")
        else:
            print(f"{key.title()}: {value}")
    
    print("\n✅ All metadata requirements met!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
