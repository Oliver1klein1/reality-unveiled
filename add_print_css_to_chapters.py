#!/usr/bin/env python3
"""
Add print CSS to all chapter, part, and conclusion HTML files.
"""

import os
import re

# Print CSS to add
print_css = """
        /* Print-specific styles for PDF generation */
        @media print {
            @page {
                size: 6in 9in; /* Paperback and hardcover dimensions */
                margin: 0.75in;
            }
            
            body {
                font-family: Georgia, 'Times New Roman', Times, serif;
                font-size: 11pt;
                line-height: 1.6;
                color: #000;
                background: #fff;
                margin: 0;
                padding: 0;
            }
            
            /* Hide navigation */
            .navigation-buttons,
            nav,
            .navbar,
            .menu,
            .breadcrumb,
            .pagination,
            .nav-button,
            [class*="nav"],
            [class*="menu"],
            [class*="breadcrumb"] {
                display: none !important;
            }
            
            /* Preserve content styling */
            .bible-quote,
            .callout,
            .callout-quote,
            .highlight {
                display: block !important;
            }
            
            /* Ensure images print properly */
            img {
                max-width: 100% !important;
                height: auto !important;
                page-break-inside: avoid;
            }
            
            /* Make all quote classes black for printing */
            .chapter-quote,
            .bible-reference,
            .callout-quote,
            .callout-quote * {
                color: #000 !important;
            }
            
            /* Force all elements with inline color to be black when printing */
            [style*="color"] {
                color: #000 !important;
            }
            
            /* Typography */
            h1, h2, h3, h4, h5, h6 {
                page-break-after: avoid;
                page-break-inside: avoid;
                color: #000;
            }
            
            h1 {
                font-size: 20pt;
                margin-bottom: 0.75rem;
            }
            
            h2 {
                font-size: 16pt;
                margin-top: 1.25rem;
                margin-bottom: 0.5rem;
            }
            
            .callout-title {
                margin-bottom: 0.5rem !important;
                page-break-after: avoid;
            }
            
            p, li {
                page-break-inside: auto;
                orphans: 2;
                widows: 2;
                margin-bottom: 0.5rem;
            }
            
            /* Allow paragraphs inside callouts to break more freely */
            .callout p,
            .callout-quote p {
                page-break-inside: auto;
                orphans: 1;
                widows: 1;
            }
            
            /* Page breaks */
            .page-break {
                page-break-before: always;
            }
            
            .no-break {
                page-break-inside: avoid;
            }
            
            .chapter {
                page-break-before: always;
            }
            
            /* Allow callouts and info-boxes to break across pages */
            .callout,
            .callout-quote,
            .info-box {
                page-break-inside: auto;
            }
            
            .bullet-points,
            ul, ol {
                page-break-inside: auto;
            }
            
            /* Reduce margins on callout titles */
            .callout-title {
                margin-bottom: 0.5rem !important;
                page-break-after: avoid;
            }
            
            /* Reduce margins on callout-quotes */
            .callout-quote {
                margin: 1rem 0 !important;
                padding: 1rem !important;
            }
            
            /* Links */
            a {
                color: #000;
                text-decoration: none;
            }
        }
"""

# Files to process (excluding already done ones)
files_to_process = [
    'copyright.html',
    'toc.html',
    'appendix.html',
    'bibliography.html'
]

for filename in files_to_process:
    if not os.path.exists(filename):
        print(f"Skipping {filename} - not found")
        continue
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if print CSS already exists
    if '@media print' in content:
        print(f"Skipping {filename} - print CSS already exists")
        continue
    
    # Find the closing </style> tag
    if '</style>' not in content:
        print(f"Skipping {filename} - no </style> tag found")
        continue
    
    # Replace </style> with print CSS + </style>
    new_content = content.replace('    </style>', print_css + '    </style>')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ Added print CSS to {filename}")

print("\nAll files processed!")

