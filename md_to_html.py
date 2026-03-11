
import re
import sys

def markdown_to_html(markdown_text):
    # Convert headings
    markdown_text = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', markdown_text, flags=re.MULTILINE)
    
    # Convert bold
    markdown_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', markdown_text)
    
    # Convert italic
    markdown_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', markdown_text)
    
    # Convert list items
    markdown_text = re.sub(r'^\* (.*?)$', r'<li>\1</li>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', markdown_text, flags=re.DOTALL)
    markdown_text = re.sub(r'</ul>\s*<ul>', '', markdown_text, flags=re.DOTALL) # remove redundant tags

    # Convert paragraphs
    paragraphs = markdown_text.split('\n\n')
    html_paragraphs = [f'<p>{p.strip()}</p>' for p in paragraphs if p.strip() and not p.strip().startswith('<')]
    markdown_text = '\n'.join(html_paragraphs)

    return markdown_text

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python md_to_html.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    html_body = markdown_to_html(md_content)

    html_template = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>{input_file}</title>
    <link rel="stylesheet" href="/assets/css/Economy_0930-E_style.css"/>
</head>
<body>
    <div class="container">
        {html_body}
    </div>
</body>
</html>
'''

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)

    print(f"Converted {input_file} to {output_file}")
