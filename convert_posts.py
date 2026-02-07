#!/usr/bin/env python3
import os
import re
import html
from pathlib import Path
from html.parser import HTMLParser

class ContentExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_post_body = False
        self.in_title = False
        self.title = ""
        self.description = ""
        self.content = []
        self.current_class = ""

    def handle_starttag(self, tag, attrs):
        self.current_class = dict(attrs).get('class', '')

        if tag == 'meta':
            attrs_dict = dict(attrs)
            if attrs_dict.get('name') == 'description':
                self.description = attrs_dict.get('content', '')

        if self.current_class == 'post-title' or self.in_post_body:
            self.in_post_body = True

    def handle_data(self, data):
        if self.in_post_body:
            self.content.append(data)

    def handle_endtag(self, tag):
        if tag == 'div' and self.current_class and 'post-body' in self.current_class:
            self.in_post_body = False

def extract_content_from_html(html_file):
    """Extract content from old HTML post"""
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Extract title
    title_match = re.search(r'<title>(.*?)\s*\|\s*重剑无锋</title>', html_content)
    title = title_match.group(1) if title_match else ""

    # Extract description
    desc_match = re.search(r'<meta name="description" content="([^"]*)"', html_content)
    description = desc_match.group(1) if desc_match else ""

    # Extract content from post-body
    body_match = re.search(r'<div class="post-body"[^>]*>(.*?)</div>', html_content, re.DOTALL)
    body_content = body_match.group(1) if body_match else ""

    # Convert HTML to simple markdown
    markdown = html_to_markdown(body_content)

    return title, description, markdown

def html_to_markdown(html_content):
    """Simple HTML to markdown conversion"""
    # Remove script tags
    markdown = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL)
    markdown = re.sub(r'<noscript[^>]*>.*?</noscript>', '', markdown, flags=re.DOTALL)

    # Handle code blocks
    def replace_code_block(m):
        code = m.group(1)
        # Remove line numbers
        code = re.sub(r'<span class="line">\d+</span>', '', code)
        # Get class info
        class_match = re.search(r'class="highlight (.*?)"', m.group(0))
        lang = class_match.group(1) if class_match else ''
        # Remove HTML tags from code
        code = re.sub(r'<[^>]+>', '', code)
        code = html.unescape(code)
        return f"\n```{lang}\n{code}\n```\n"

    markdown = re.sub(r'<figure class="highlight [^"]*"><table><tr><td class="gutter"><pre><span class="line">\d+</span><br></pre></td><td class="code"><pre>(.*?)</pre></td></tr></table></figure>',
                     replace_code_block, markdown, flags=re.DOTALL)

    # Handle paragraphs
    markdown = re.sub(r'<p>(.*?)</p>', r'\n\1\n', markdown, flags=re.DOTALL)

    # Handle headings
    for i in range(1, 7):
        markdown = re.sub(rf'<h{i}>(.*?)</h{i}>', f"\n{'#' * i} \1\n", markdown, flags=re.DOTALL)

    # Handle links
    markdown = re.sub(r'<a href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', markdown, flags=re.DOTALL)

    # Handle strong/bold
    markdown = re.sub(r'<strong>(.*?)</strong>', r'**\1**', markdown, flags=re.DOTALL)
    markdown = re.sub(r'<b>(.*?)</b>', r'**\1**', markdown, flags=re.DOTALL)

    # Handle images
    markdown = re.sub(r'<img[^>]*src="([^"]*)"[^>]*>', r'\n![](\1)\n', markdown, flags=re.DOTALL)

    # Handle br
    markdown = re.sub(r'<br\s*/?>', '\n', markdown)

    # Remove remaining HTML tags
    markdown = re.sub(r'<[^>]+>', '', markdown)

    # Decode HTML entities
    markdown = html.unescape(markdown)

    # Clean up multiple blank lines
    markdown = re.sub(r'\n\s*\n\s*\n', '\n\n', markdown)

    return markdown.strip()

def convert_post(directory):
    """Convert a single post directory"""
    html_file = os.path.join(directory, 'index.html')

    if not os.path.exists(html_file):
        return None

    # Extract date from directory name
    dir_name = os.path.basename(directory)
    date_match = re.match(r'(\d{4})-(\d{2})-(\d{2})-(.+)', dir_name)

    if not date_match:
        return None

    year, month, day, slug = date_match.groups()
    date_str = f"{year}-{month}-{day}"

    # Extract content
    title, description, markdown = extract_content_from_html(html_file)

    if not title:
        return None

    # Create markdown file
    md_filename = f"{slug}.md"
    md_path = os.path.join('source/_posts', md_filename)

    # Check for images
    images = []
    for item in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, item)) and item != 'index.html':
            if item.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                images.append(item)

    # Create front matter
    front_matter_lines = ['---', f'title: {title}', f'date: {date_str}', 'tags:', 'categories:']
    if description:
        # Truncate description if too long
        desc = description[:200] + '...' if len(description) > 200 else description
        # Escape colons and other special chars in YAML
        desc = desc.replace(':', '\\:').replace('\'', "\\'")
        front_matter_lines.insert(3, f"description: '{desc}'")
    front_matter_lines.append('---')

    md_content = '\n'.join(front_matter_lines) + '\n\n' + markdown

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    return md_filename

def main():
    # Find all dated directories
    dirs = []
    for d in os.listdir('.'):
        if os.path.isdir(d) and re.match(r'\d{4}-\d{2}-\d{2}', d):
            dirs.append(d)

    dirs.sort()

    print(f"Found {len(dirs)} posts to convert...")

    converted = []
    for d in dirs:
        result = convert_post(d)
        if result:
            converted.append(result)
            print(f"✓ Converted: {result}")

    print(f"\nConverted {len(converted)} posts to source/_posts/")

if __name__ == '__main__':
    main()
