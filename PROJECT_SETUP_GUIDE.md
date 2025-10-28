# Project Setup Guide: Copy This System to New Book Projects

## 📋 Overview
This guide lists all Cursor rules and files you need to copy to set up the complete book publishing system in a new project.

---

## 🎯 Cursor Rules Files to Copy

### 1. EPUB Conversion Rules (`.cursorrules`)
**Location**: Root directory  
**Purpose**: Defines EPUB conversion workflow, Amazon KDP compliance, and Kindle-specific requirements

**Key Features**:
- Enhanced conversion with style preservation
- Mandatory verification step
- Amazon KDP compliance (mimetype ordering, metadata)
- Spine order prevention (critical for Kindle)
- Duplicate ID handling
- Table of Contents management
- Kindle Previewer compatibility solutions
- Comprehensive testing checklist

### 2. PDF Printing Rules (`.cursorrules_pdf`)
**Location**: Root directory  
**Purpose**: Defines HTML to PDF printing workflow with print-specific CSS

**Key Features**:
- Page setup and size control
- Navigation element hiding
- Content preservation
- Page break control
- Multiple PDF generation methods (Puppeteer, wkhtmltopdf, etc.)
- Print CSS template

---

## 📜 Python Scripts to Copy

### Core EPUB Scripts

#### 1. `create_epub_enhanced.py`
**Purpose**: Converts HTML to EPUB-compatible XHTML with style preservation

**To Customize**:
```python
# Update the files_to_process list with your book's structure
files_to_process = [
    "introduction.html",
    "chapter1.html", "chapter2.html", "chapter3.html",
    "conclusion.html"
]
```

#### 2. `verify_epub_conversion.py`
**Purpose**: Verifies HTML conversion integrity (CSS classes, inline styles, image counts)

**To Customize**:
```python
# Update the files_to_check list to match your book
files_to_check = [
    "introduction.html",
    "chapter1.html", "chapter2.html", "chapter3.html",
    "conclusion.html"
]
```

#### 3. `create_final_epub.py`
**Purpose**: Creates final EPUB with proper structure and spine order

**To Customize**:
```python
# Update the EPUB filename
if os.path.exists("Your_Book_Name_Final.epub"):
    os.remove("Your_Book_Name_Final.epub")

# Update correct_order in fix_spine_order()
correct_order = [
    "cover",
    "titlepage",
    "toc",
    "introduction",
    "chapter1",
    # ... rest of chapters
]
```

#### 4. `create_kdp_epub.py`
**Purpose**: Creates Amazon KDP-compliant EPUB with proper metadata

**To Customize**:
```python
# Update metadata
metadata = {
    "title": "Your Book Title",
    "subtitle": "Your Subtitle",
    "author": "Your Name",
    "publisher": "Your Publisher",
    # ...
}

# Update correct_order in fix_spine_order()
# Same as create_final_epub.py
```

#### 5. `check_metadata.py`
**Purpose**: Checks for metadata completeness and prompts for missing information

**To Customize**:
```python
# Update metadata prompts to match your book
required_metadata = {
    "title": "Book Title",
    "subtitle": "Book Subtitle",
    # ...
}
```

### Template Scripts (Start New Projects With These)

#### 6. `epub_conversion_template.py`
**Purpose**: Template for HTML to XHTML conversion

#### 7. `epub_verification_template.py`
**Purpose**: Template for verification script

#### 8. `epub_creation_template.py`
**Purpose**: Template for final EPUB creation

---

## 📚 Documentation Files

### 1. `EPUB_SETUP_GUIDE.md`
**Purpose**: Step-by-step guide for setting up EPUB conversion in new projects

**Contains**:
- Directory structure
- Script customization instructions
- HTML file standards
- Workflow steps
- Quality checklist
- Troubleshooting

### 2. `KINDLE_COMPATIBILITY_GUIDE.md`
**Purpose**: Kindle-specific CSS and HTML optimizations

**Contains**:
- Common Kindle issues and solutions
- Verse quote sizing fixes
- Table scrambling solutions
- Image sizing constraints
- Complete Kindle-optimized CSS template
- Testing checklist

### 3. `PDF_SETUP_GUIDE.md`
**Purpose**: Guide for PDF generation from HTML

**Contains**:
- Print CSS standards
- Navigation hiding techniques
- Page break control
- PDF generation methods
- Quality assurance checklist

### 4. `PROJECT_SETUP_GUIDE.md` (This File)
**Purpose**: Master list of all files to copy to new projects

---

## 📁 Directory Structure to Create

```
your-new-book/
├── .cursorrules                    ← Copy from root
├── .cursorrules_pdf                ← Copy from root
├── EPUB_SETUP_GUIDE.md             ← Copy from root
├── KINDLE_COMPATIBILITY_GUIDE.md   ← Copy from root
├── PDF_SETUP_GUIDE.md              ← Copy from root
├── PROJECT_SETUP_GUIDE.md          ← Copy from root
│
├── create_epub_enhanced.py         ← Copy from root (then customize)
├── verify_epub_conversion.py       ← Copy from root (then customize)
├── create_final_epub.py            ← Copy from root (then customize)
├── create_kdp_epub.py              ← Copy from root (then customize)
├── check_metadata.py               ← Copy from root (then customize)
│
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
│
├── introduction.html
├── chapter1.html
├── chapter2.html
├── conclusion.html
└── [other HTML files]
```

---

## 🚀 Setup Process for New Book

### Step 1: Copy Essential Files
```bash
# Copy Cursor rules
cp .cursorrules /path/to/new-book/
cp .cursorrules_pdf /path/to/new-book/

# Copy documentation
cp EPUB_SETUP_GUIDE.md /path/to/new-book/
cp KINDLE_COMPATIBILITY_GUIDE.md /path/to/new-book/
cp PDF_SETUP_GUIDE.md /path/to/new-book/
cp PROJECT_SETUP_GUIDE.md /path/to/new-book/

# Copy Python scripts
cp create_epub_enhanced.py /path/to/new-book/
cp verify_epub_conversion.py /path/to/new-book/
cp create_final_epub.py /path/to/new-book/
cp create_kdp_epub.py /path/to/new-book/
cp check_metadata.py /path/to/new-book/

# Copy EPUB directory structure
cp -r epub/ /path/to/new-book/
```

### Step 2: Customize Scripts
1. **Update file lists** in `create_epub_enhanced.py` and `verify_epub_conversion.py`
2. **Update EPUB filename** in `create_final_epub.py` and `create_kdp_epub.py`
3. **Update spine order** in `fix_spine_order()` functions
4. **Update metadata** in `create_kdp_epub.py` and `book_metadata.json`

### Step 3: Set Up Metadata
```bash
# Create book_metadata.json
cat > book_metadata.json << 'EOF'
{
  "title": "Your Book Title",
  "subtitle": "Your Subtitle",
  "author": "Your Name",
  "publisher": "Your Publisher",
  "publication_date": "2025",
  "cover_image": "path/to/cover.jpg",
  "tags": "keyword1, keyword2, keyword3",
  "description": "Your book description",
  "language": "en",
  "isbn": "978-1234567890"
}
EOF
```

### Step 4: Create Your HTML Files
- Create `introduction.html`
- Create `chapter1.html`, `chapter2.html`, etc.
- Create `part1.html`, `part2.html`, etc.
- Create `conclusion.html`
- Create `appendix1.html`, etc.

### Step 5: Run the Workflow
```bash
# 1. Check metadata
python check_metadata.py

# 2. Convert HTML to XHTML
python create_epub_enhanced.py

# 3. Verify conversion
python verify_epub_conversion.py

# 4. Create final EPUB
python create_final_epub.py

# 5. Create KDP EPUB
python create_kdp_epub.py
```

---

## ✅ Quality Assurance Checklist

Before finalizing your EPUB:

### EPUB Creation
- [ ] All HTML files converted to XHTML
- [ ] All CSS classes preserved
- [ ] All inline styles preserved (except navigation)
- [ ] Image counts match between HTML and XHTML
- [ ] Bible quotes display correctly

### Kindle Compatibility
- [ ] **Book opens to correct page** (not alphabetically sorted)
- [ ] **No duplicate Table of Contents** at end
- [ ] **Part titles display correctly** (not missing)
- [ ] **Verse quotes properly sized** (not too large)
- [ ] **Tables render correctly** (not scrambled)
- [ ] **Book cover images sized appropriately** (not full-page)
- [ ] **Navigation links work** and are simple ("← Back")
- [ ] **No conversion errors** in Kindle Previewer log

### Amazon KDP Compliance
- [ ] **Mimetype file is FIRST** in archive
- [ ] **All metadata included** in content.opf
- [ ] **Cover image properly linked**
- [ ] **No duplicate IDs** (check for E27012 errors)
- [ ] **Spine order is correct** (not alphabetical)

---

## 📝 Quick Reference: What Each File Does

| File | Purpose | Key Features |
|------|---------|--------------|
| `.cursorrules` | EPUB conversion workflow | Style preservation, KDP compliance, spine order |
| `.cursorrules_pdf` | PDF printing workflow | Print CSS, navigation hiding, page breaks |
| `create_epub_enhanced.py` | HTML → XHTML conversion | Preserves CSS classes and inline styles |
| `verify_epub_conversion.py` | Content integrity check | Compares HTML vs XHTML |
| `create_final_epub.py` | Final EPUB creation | Ensures proper structure |
| `create_kdp_epub.py` | KDP-compliant EPUB | Includes metadata, proper ordering |
| `check_metadata.py` | Metadata validation | Prompts for missing info |
| `EPUB_SETUP_GUIDE.md` | Setup instructions | Step-by-step guide |
| `KINDLE_COMPATIBILITY_GUIDE.md` | Kindle fixes | Common issues and solutions |
| `PDF_SETUP_GUIDE.md` | PDF generation | Print CSS and methods |

---

## 🎯 Critical Learnings Captured

The Cursor rules now include all hard-won knowledge:

### 1. **Spine Order Prevention**
- EPUB readers sort spine alphabetically by default
- Solution: `fix_spine_order()` function in all scripts
- Prevents "opens to Appendix" issue

### 2. **Duplicate ID Handling**
- Multiple images with similar names cause errors
- Solution: Generate unique IDs for all items
- Prevents "E27012" errors in Kindle Previewer

### 3. **Table of Contents Management**
- Duplicate TOCs appear at end of book
- Solution: Proper `toc.xhtml` structure and `nav.xhtml` references
- Ensures clean, single TOC experience

### 4. **Kindle Previewer Compatibility**
- Poor CSS rendering capabilities
- Solutions:
  - Avoid complex CSS (flexbox/grid)
  - Use `!important` declarations
  - Simple HTML structure
  - Constrain image sizes
  - Simple navigation text

### 5. **Style Preservation**
- CSS classes and inline styles must be preserved
- Solution: Enhanced conversion script
- Ensures EPUB matches HTML exactly

---

## 🚨 Common Mistakes to Avoid

1. **Don't skip verification** - Always run `verify_epub_conversion.py`
2. **Don't forget spine order** - Always implement `fix_spine_order()`
3. **Don't use complex CSS** - Keep it simple for Kindle compatibility
4. **Don't forget metadata** - Always include complete metadata
5. **Don't skip testing** - Always test in Kindle Previewer
6. **Don't ignore errors** - Fix issues before finalizing

---

## 📚 Additional Resources

- **EPUB Specifications**: http://www.idpf.org/epub/
- **Amazon KDP Guidelines**: https://kdp.amazon.com/
- **Kindle Previewer**: Download from Amazon KDP
- **EPUB Testing**: Use Calibre, Adobe Digital Editions, or Kindle Previewer

---

## 🎉 Success Criteria

Your new book project is ready when:
- ✅ All scripts customized and working
- ✅ EPUB verification passes
- ✅ No errors in Kindle Previewer
- ✅ Book opens to correct page
- ✅ All styling preserved and functional
- ✅ Metadata complete and correct
- ✅ Amazon KDP compliant
- ✅ Final EPUB file created successfully

Remember: **Quality over speed** - Always verify before finalizing EPUB files.

