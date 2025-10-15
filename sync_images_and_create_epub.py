#!/usr/bin/env python3
"""
Sync images from root to EPUB folder, then create EPUB for Amazon KDP
"""
import os
import shutil
import zipfile
from pathlib import Path

def sync_images(source_dir, epub_images_dir):
    """
    Copy all .jpg images from source directory to EPUB images directory
    """
    source_path = Path(source_dir)
    epub_images_path = Path(epub_images_dir)
    
    # Create images directory if it doesn't exist
    epub_images_path.mkdir(parents=True, exist_ok=True)
    
    # Find all .jpg files in the source directory (not in subdirectories)
    image_files = list(source_path.glob('*.jpg'))
    
    copied_count = 0
    for image_file in image_files:
        dest_file = epub_images_path / image_file.name
        shutil.copy2(image_file, dest_file)
        copied_count += 1
        print(f"  Copied: {image_file.name}")
    
    print(f"\nTotal images synced: {copied_count}")

def create_epub(source_dir, output_file):
    """
    Create an EPUB file with proper structure:
    1. mimetype file first (uncompressed)
    2. META-INF directory
    3. OEBPS directory with all content
    """
    source_path = Path(source_dir)
    
    # Remove existing EPUB if it exists
    if os.path.exists(output_file):
        os.remove(output_file)
    
    # Create the EPUB (ZIP file)
    with zipfile.ZipFile(output_file, 'w') as epub:
        # 1. Add mimetype first, uncompressed (required by EPUB spec)
        mimetype_path = source_path / 'mimetype'
        epub.write(mimetype_path, 'mimetype', compress_type=zipfile.ZIP_STORED)
        
        # 2. Add META-INF directory
        meta_inf_dir = source_path / 'META-INF'
        for file_path in meta_inf_dir.rglob('*'):
            if file_path.is_file():
                arcname = str(file_path.relative_to(source_path))
                epub.write(file_path, arcname, compress_type=zipfile.ZIP_DEFLATED)
        
        # 3. Add OEBPS directory (all content)
        oebps_dir = source_path / 'OEBPS'
        for file_path in oebps_dir.rglob('*'):
            if file_path.is_file():
                arcname = str(file_path.relative_to(source_path))
                epub.write(file_path, arcname, compress_type=zipfile.ZIP_DEFLATED)
    
    print(f"\nEPUB created successfully: {output_file}")
    print(f"File size: {os.path.getsize(output_file) / (1024*1024):.2f} MB")

if __name__ == '__main__':
    root_directory = r'C:\Users\Michael\OneDrive\Older Documents\Desktop\reality-unveiled'
    epub_images_directory = r'C:\Users\Michael\OneDrive\Older Documents\Desktop\reality-unveiled\reality-unveiled-epub\OEBPS\images'
    epub_source_directory = r'C:\Users\Michael\OneDrive\Older Documents\Desktop\reality-unveiled\reality-unveiled-epub'
    output_epub = r'C:\Users\Michael\OneDrive\Older Documents\Desktop\reality-unveiled\Reality-Unveiled.epub'
    
    print("=" * 60)
    print("STEP 1: Syncing images from root to EPUB images folder...")
    print("=" * 60)
    sync_images(root_directory, epub_images_directory)
    
    print("\n" + "=" * 60)
    print("STEP 2: Creating EPUB file...")
    print("=" * 60)
    create_epub(epub_source_directory, output_epub)
    
    print("\n" + "=" * 60)
    print("DONE! All images synced and EPUB created successfully!")
    print("=" * 60)

