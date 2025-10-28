# Kindle Compatibility Guide

## Overview
This guide provides specific CSS and HTML optimizations to ensure your EPUB files display correctly in Kindle Previewer and on actual Kindle devices.

## Common Kindle Issues and Solutions

### 1. Verse Quotes Too Large on Part Pages

**Problem**: Inline styles with large font sizes (2.2rem+) don't render properly on Kindle.

**Solution**: Use CSS classes instead of inline styles:

```css
/* Instead of inline style */
<span style="font-size: 2.2rem; font-weight: bold;">Verse text</span>

/* Use CSS class */
<span class="verse-text">Verse text</span>

.kindle-optimized .verse-text {
    font-size: 1.8rem;
    font-weight: bold;
    color: #3b3b98;
    font-family: 'Playfair Display', serif;
    letter-spacing: 0.03em;
    display: block;
    line-height: 1.3;
}
```

### 2. Tables Getting Scrambled

**Problem**: Flexbox layouts don't work well on Kindle.

**Solution**: Use traditional table CSS:

```css
/* Instead of flexbox */
.parts-table {
    display: flex;
    flex-direction: column;
}

/* Use table display */
.parts-table {
    display: table !important;
    width: 100%;
    border-collapse: collapse;
}

.part-row {
    display: table-row !important;
}

.part-number, .part-theme, .part-question {
    display: table-cell !important;
    padding: 1rem;
    border: 1px solid #e2e8f0;
    vertical-align: top;
}
```

### 3. Images Displaying Full-Page

**Problem**: Images without size constraints take up entire pages.

**Solution**: Add maximum dimensions:

```css
.book-cover img {
    width: 100%;
    height: auto;
    max-width: 200px;
    max-height: 300px;
    border-radius: 0.5rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
```

### 4. Titles Not Displaying

**Problem**: CSS gradients and complex styling can hide titles.

**Solution**: Ensure titles are always visible:

```css
.part-title {
    display: block !important;
    visibility: visible !important;
}
```

## Kindle-Specific CSS Best Practices

### Font Sizes
- Use `rem` units instead of `px`
- Keep font sizes reasonable (1.8rem max for large text)
- Avoid extremely large font sizes (3rem+)

### Layout
- Prefer `display: table` over `display: flex`
- Use `!important` for critical Kindle styles
- Avoid complex CSS gradients in titles

### Images
- Always set `max-width` and `max-height`
- Use `width: 100%; height: auto;` for responsive images
- Avoid images without size constraints

### Text Styling
- Use CSS classes instead of inline styles
- Keep line-height reasonable (1.3-1.6)
- Avoid complex text effects

## Complete Kindle-Optimized CSS Template

```css
/* Kindle-specific optimizations */
.kindle-optimized .verse-text {
    font-size: 1.8rem;
    font-weight: bold;
    color: #3b3b98;
    font-family: 'Playfair Display', serif;
    letter-spacing: 0.03em;
    display: block;
    line-height: 1.3;
}

.kindle-optimized .verse-reference {
    display: block;
    margin-top: 1.2em;
    font-size: 1.1rem;
    color: #5c6ac4;
    font-weight: 600;
}

/* Ensure titles display properly */
.part-title {
    display: block !important;
    visibility: visible !important;
}

/* Kindle-compatible tables */
.parts-table {
    display: table !important;
    width: 100%;
    border-collapse: collapse;
    margin: 1.5rem 0;
}

.part-row {
    display: table-row !important;
}

.part-number, .part-theme, .part-question {
    display: table-cell !important;
    padding: 1rem;
    border: 1px solid #e2e8f0;
    vertical-align: top;
}

/* Image size constraints */
.book-cover img {
    max-width: 200px;
    max-height: 300px;
    width: 100%;
    height: auto;
}

/* Text size constraints */
.parts-intro {
    font-size: 1.1rem !important;
    font-weight: bold;
    margin: 1.5rem 0;
    text-align: center;
}
```

## Testing Checklist

Before converting to Kindle format, verify:

- [ ] No inline styles with large font sizes (2rem+)
- [ ] Tables use `display: table` instead of flexbox
- [ ] Images have `max-width` and `max-height` constraints
- [ ] Titles use `display: block !important`
- [ ] All critical styles use `!important`
- [ ] Font sizes are reasonable (1.8rem max for large text)
- [ ] Line heights are appropriate (1.3-1.6)

## Conversion Process

1. **Apply Kindle CSS fixes** to HTML files
2. **Test in browser** to ensure styling still works
3. **Convert to EPUB** using enhanced conversion script
4. **Test in Kindle Previewer** to verify fixes
5. **Convert to Kindle format** using Kindle Previewer

## Troubleshooting

### If verse quotes are still too large:
- Check that CSS classes are applied correctly
- Verify no inline styles override the classes
- Ensure `!important` is used for critical styles

### If tables are still scrambled:
- Verify `display: table !important` is applied
- Check that all table elements use `display: table-cell !important`
- Ensure no flexbox styles are conflicting

### If images are still full-page:
- Add `max-width` and `max-height` constraints
- Check that `width: 100%; height: auto;` is applied
- Verify image containers have size limits

### If titles don't display:
- Add `display: block !important` and `visibility: visible !important`
- Check for CSS gradients that might hide text
- Ensure no conflicting styles are applied

Remember: **Kindle has limited CSS support**, so keep styling simple and use `!important` for critical Kindle-specific styles.
