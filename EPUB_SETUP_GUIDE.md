# EPUB Book Project Setup Guide

## Quick Start for New Book Projects

### 1. Copy Template Scripts
Copy these three template scripts to your new book project directory:
- `epub_conversion_template.py` → `create_epub_enhanced.py`
- `epub_verification_template.py` → `verify_epub_conversion.py`  
- `epub_creation_template.py` → `create_final_epub.py`

### 2. Customize Scripts for Your Book

#### In `create_epub_enhanced.py`:
```python
# Update the files_to_process list with your book's structure
files_to_process = [
    "introduction.html",
    "chapter1.html", "chapter2.html", "chapter3.html",
    # Add all your HTML files here
    "conclusion.html"
]
```

#### In `verify_epub_conversion.py`:
```python
# Update the files_to_check list to match your book
files_to_check = [
    "introduction.html",
    "chapter1.html", "chapter2.html", "chapter3.html",
    # Add all your HTML files here
    "conclusion.html"
]
```

#### In `create_final_epub.py`:
```python
# Update the EPUB filename
if os.path.exists("Your_Book_Name_Final.epub"):
    os.remove("Your_Book_Name_Final.epub")

with zipfile.ZipFile("Your_Book_Name_Final.epub", 'w', zipfile.ZIP_DEFLATED) as epub:
    # ... rest of the script
```

### 3. Set Up EPUB Directory Structure
Create the following directory structure:
```
your-book-project/
├── epub/
│   ├── META-INF/
│   │   └── container.xml
│   ├── mimetype
│   └── OEBPS/
│       ├── content.opf
│       ├── nav.xhtml
│       ├── toc.ncx
│       ├── Styles/
│       │   └── style.css
│       ├── Images/
│       └── Text/
├── create_epub_enhanced.py
├── verify_epub_conversion.py
├── create_final_epub.py
├── introduction.html
├── chapter1.html
├── chapter2.html
└── [other HTML files]
```

### 4. HTML File Standards

#### Required CSS Classes
Ensure your HTML files use these standard classes:
- **Bible quotes**: `class="bible-quote"`
- **Callouts**: `class="highlight"`, `class="callout"`, etc.
- **Navigation**: `class="navigation"` and `class="nav-link"`

#### Example Bible Quote:
```html
<div class="bible-quote">
    "For God so loved the world..."<br/><br/>
    — John 3:16
</div>
```

#### Example Callout Box:
```html
<div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-left: 4px solid #0ea5e9; padding: 1.5rem; margin: 1.5rem 0; border-radius: 0 0.5rem 0.5rem 0;">
    <p style="margin-bottom: 0;"><strong>Important Note:</strong> This is a highlighted callout.</p>
</div>
```

### 5. EPUB Creation Workflow

#### Step 1: Convert HTML to XHTML
```bash
python create_epub_enhanced.py
```

#### Step 2: Verify Conversion
```bash
python verify_epub_conversion.py
```

#### Step 3: Create Final EPUB (only if verification passes)
```bash
python create_final_epub.py
```

### 6. Quality Checklist

#### Before Running Scripts:
- [ ] All HTML files exist and are valid
- [ ] Bible quotes use `bible-quote` class
- [ ] Images are properly referenced
- [ ] CSS classes are consistent

#### After Conversion:
- [ ] Verification shows "Perfect matches" for all files
- [ ] No missing CSS classes
- [ ] Inline styles preserved (accounting for navigation removal)
- [ ] Image counts match

#### Final EPUB:
- [ ] EPUB structure verification passes
- [ ] All required files present
- [ ] Images properly linked
- [ ] Styling renders correctly

### 7. Troubleshooting

#### Common Issues:
- **Missing files**: Check file paths in scripts match your HTML files
- **CSS not preserved**: Ensure conversion script preserves all classes
- **Verification fails**: Check for navigation elements (should be removed)
- **Images not found**: Verify image files exist and paths are correct

#### Debug Steps:
1. Run verification script to identify specific issues
2. Compare HTML source with XHTML output manually
3. Check conversion script preserves all styling
4. Verify EPUB directory structure is correct

### 8. Best Practices

1. **Always verify before finalizing** - Never skip verification step
2. **Test in multiple readers** - Verify styling works across devices
3. **Keep scripts updated** - Ensure scripts work with HTML changes
4. **Document customizations** - Note any project-specific modifications
5. **Version control** - Keep track of script changes

### 9. Success Criteria
- ✅ All files pass verification with "Perfect matches"
- ✅ Bible quotes display with proper styling
- ✅ All CSS classes and inline styles preserved
- ✅ Images properly linked and displayed
- ✅ EPUB structure meets standards
- ✅ Final EPUB file created successfully

## Template Scripts Location
- `epub_conversion_template.py` - Enhanced conversion with style preservation
- `epub_verification_template.py` - Automatic verification of HTML vs XHTML
- `epub_creation_template.py` - Final EPUB creation with proper structure

## Support
If you encounter issues:
1. Check the verification report for specific errors
2. Compare HTML source with XHTML output
3. Ensure all template customizations are correct
4. Verify EPUB directory structure is complete

Remember: **Quality over speed** - Always verify before finalizing EPUB files.
