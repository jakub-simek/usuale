#!/usr/bin/env python3
"""
Convert Markdown presentation to standalone HTML
"""

import re
from pathlib import Path

def markdown_to_html_slides(md_file, output_file):
    """Convert markdown presentation to reveal.js HTML"""

    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove YAML frontmatter
    content = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)

    # Split by slide separators (---)
    slides = content.split('\n---\n')

    html_slides = []
    for slide in slides:
        slide = slide.strip()
        if not slide:
            continue

        # Convert markdown to basic HTML
        slide_html = convert_markdown_basics(slide)
        html_slides.append(f'<section>\n{slide_html}\n</section>')

    # Create full HTML document
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TEI Data Model for Divinum Officium</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.6.0/dist/reveal.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.6.0/dist/theme/serif.css">
    <style>
        .reveal section {{
            height: 100%;
            overflow-y: auto !important;
            padding: 20px 40px !important;
        }}
        .reveal h1 {{ font-size: 2.2em; margin-bottom: 0.5em; }}
        .reveal h2 {{ font-size: 1.8em; margin-bottom: 0.4em; margin-top: 0.5em; }}
        .reveal h3 {{ font-size: 1.4em; margin-bottom: 0.3em; margin-top: 0.4em; }}
        .reveal p {{ font-size: 0.9em; line-height: 1.4; margin: 0.5em 0; }}
        .reveal code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-size: 0.85em; color: #c7254e; }}
        .reveal pre {{ margin: 0.5em 0; background: #f8f8f8; border: 1px solid #ddd; border-radius: 4px; }}
        .reveal pre code {{
            padding: 15px;
            font-size: 0.55em;
            line-height: 1.4;
            background: #f8f8f8;
            color: #333;
            display: block;
            overflow-x: auto;
        }}
        /* Syntax highlighting with high contrast */
        .reveal pre code .hljs-comment {{ color: #008000; font-style: italic; }}
        .reveal pre code .hljs-string {{ color: #d14; }}
        .reveal pre code .hljs-number {{ color: #0086b3; }}
        .reveal pre code .hljs-literal {{ color: #0086b3; }}
        .reveal pre code .hljs-keyword {{ color: #a71d5d; font-weight: bold; }}
        .reveal pre code .hljs-attr {{ color: #795da3; }}
        .reveal pre code .hljs-name {{ color: #333; font-weight: bold; }}
        .reveal pre code .hljs-variable {{ color: #333; }}
        .reveal pre code .hljs-title {{ color: #795da3; }}
        .reveal pre code .hljs-built_in {{ color: #0086b3; }}
        .reveal pre code .hljs-meta {{ color: #999; }}

        .reveal table {{ font-size: 0.65em; margin: 0.5em 0; }}
        .reveal table th {{ background: #3498db; color: white; padding: 6px; }}
        .reveal table td {{ border: 1px solid #ddd; padding: 6px; }}
        .reveal ul {{ text-align: left; font-size: 0.9em; margin: 0.3em 0; }}
        .reveal ol {{ text-align: left; font-size: 0.9em; margin: 0.3em 0; }}
        .reveal li {{ margin: 0.2em 0; }}
        .reveal strong {{ color: #2c3e50; }}
    </style>
</head>
<body>
    <div class="reveal">
        <div class="slides">
{''.join(html_slides)}
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.6.0/dist/reveal.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.6.0/plugin/notes/notes.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.6.0/plugin/markdown/markdown.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.6.0/plugin/highlight/highlight.js"></script>
    <script>
        Reveal.initialize({{
            hash: true,
            controls: true,
            progress: true,
            center: true,
            transition: 'slide',
            plugins: [ RevealMarkdown, RevealHighlight, RevealNotes ]
        }});
    </script>
</body>
</html>
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Converted presentation to {output_file}")
    print(f"   Open in browser: file://{Path(output_file).absolute()}")

def convert_markdown_basics(text):
    """Convert basic markdown to HTML"""

    # Store code blocks with placeholders to protect them from further processing
    code_blocks = []
    inline_codes = []

    def store_code_block(match):
        lang = match.group(1) or ''
        code = match.group(2)
        # Escape HTML entities
        code = code.replace('&', '&amp;')
        code = code.replace('<', '&lt;')
        code = code.replace('>', '&gt;')
        code = code.replace('"', '&quot;')
        placeholder = f'___CODE_BLOCK_{len(code_blocks)}___'
        code_blocks.append(f'<pre><code class="language-{lang}">{code}</code></pre>')
        return placeholder

    text = re.sub(r'```(\w*)\n(.*?)```', store_code_block, text, flags=re.DOTALL)

    # Store inline code with placeholders
    def store_inline_code(match):
        code = match.group(1)
        code = code.replace('&', '&amp;')
        code = code.replace('<', '&lt;')
        code = code.replace('>', '&gt;')
        placeholder = f'___INLINE_CODE_{len(inline_codes)}___'
        inline_codes.append(f'<code>{code}</code>')
        return placeholder

    text = re.sub(r'`([^`]+)`', store_inline_code, text)

    # Headers
    text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)

    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)

    # Links
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)

    # Lists
    lines = text.split('\n')
    in_ul = False
    in_ol = False
    result = []

    for line in lines:
        # Unordered list
        if re.match(r'^[\-\*\+] (.+)', line):
            if not in_ul:
                result.append('<ul>')
                in_ul = True
            item = re.sub(r'^[\-\*\+] (.+)', r'<li>\1</li>', line)
            result.append(item)
        # Ordered list
        elif re.match(r'^\d+\. (.+)', line):
            if not in_ol:
                result.append('<ol>')
                in_ol = True
            item = re.sub(r'^\d+\. (.+)', r'<li>\1</li>', line)
            result.append(item)
        else:
            if in_ul:
                result.append('</ul>')
                in_ul = False
            if in_ol:
                result.append('</ol>')
                in_ol = False
            result.append(line)

    if in_ul:
        result.append('</ul>')
    if in_ol:
        result.append('</ol>')

    text = '\n'.join(result)

    # Tables
    def convert_table(text):
        lines = text.split('\n')
        table_lines = []
        in_table = False

        for line in lines:
            if '|' in line and not line.strip().startswith('<!--'):
                if not in_table:
                    table_lines.append('<table>')
                    in_table = True

                cells = [cell.strip() for cell in line.split('|')[1:-1]]

                # Check if separator row
                if all(re.match(r'^[\-:]+$', cell) for cell in cells):
                    continue

                # First row is header
                if in_table and '<thead>' not in ''.join(table_lines):
                    table_lines.append('<thead><tr>')
                    for cell in cells:
                        table_lines.append(f'<th>{cell}</th>')
                    table_lines.append('</tr></thead><tbody>')
                else:
                    table_lines.append('<tr>')
                    for cell in cells:
                        table_lines.append(f'<td>{cell}</td>')
                    table_lines.append('</tr>')
            else:
                if in_table:
                    table_lines.append('</tbody></table>')
                    in_table = False
                table_lines.append(line)

        if in_table:
            table_lines.append('</tbody></table>')

        return '\n'.join(table_lines)

    text = convert_table(text)

    # Paragraphs
    text = re.sub(r'\n\n+', '</p><p>', text)
    if not text.startswith('<'):
        text = '<p>' + text
    if not text.endswith('>'):
        text = text + '</p>'

    # Clean up empty paragraphs
    text = re.sub(r'<p>\s*</p>', '', text)
    text = re.sub(r'<p>(<h[1-6])', r'\1', text)
    text = re.sub(r'(</h[1-6]>)</p>', r'\1', text)
    text = re.sub(r'<p>(<pre)', r'\1', text)
    text = re.sub(r'(</pre>)</p>', r'\1', text)
    text = re.sub(r'<p>(<table)', r'\1', text)
    text = re.sub(r'(</table>)</p>', r'\1', text)
    text = re.sub(r'<p>(<ul)', r'\1', text)
    text = re.sub(r'(</ul>)</p>', r'\1', text)
    text = re.sub(r'<p>(<ol)', r'\1', text)
    text = re.sub(r'(</ol>)</p>', r'\1', text)

    # Restore code blocks from placeholders (LAST step)
    for i, code_block in enumerate(code_blocks):
        text = text.replace(f'___CODE_BLOCK_{i}___', code_block)

    # Restore inline code from placeholders
    for i, inline_code in enumerate(inline_codes):
        text = text.replace(f'___INLINE_CODE_{i}___', inline_code)

    return text

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        input_file = Path(sys.argv[1])
        output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else input_file.with_suffix('.html')
    else:
        input_file = Path(__file__).parent / 'tei-presentation.md'
        output_file = Path(__file__).parent / 'tei-presentation.html'

    markdown_to_html_slides(input_file, output_file)
