
import re

# File path
file_path = r'G:\マイドライブ\Guide-Website\Economy\0930-E\reference-materials.html'

# Read the original HTML content
with open(file_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# --- 1. Remove Royenthal content ---
cards = re.findall(r'<div class="card">.*?</div>', html_content, re.DOTALL)
royenthal_cards = [card for card in cards if 'Reuenthal' in card]

for card in royenthal_cards:
    html_content = html_content.replace(card, '')

# --- 2. Categorize all cards ---
sections = re.findall(r'<section class="category">.*?</section>', html_content, re.DOTALL)

walpurgis_cards_html = ''
thp_cards_html = ''
countries_cards_html = ''
others_cards_html = ''

# Important links
important_walpurgis_html = ''
important_thp_html = ''
lobotomy_card_html = ''

for section in sections:
    title = re.search(r'<h2>(.*?)</h2>', section).group(1)
    cards_in_section = re.findall(r'<div class="card">.*?</div>', section, re.DOTALL)

    for card in cards_in_section:
        # Check for important cards first
        if 'Project Walpurgis reassessment' in card:
            important_walpurgis_html = card
            continue
        if 'The Horizon Protocol' in card:
            important_thp_html = card
            important_thp_html = important_thp_html.replace('</p>', '<br><b>(We are currently working on addressing its vulnerabilities.)</b></p>')
            continue
        if 'Lobotomy' in card:
            lobotomy_card_html = card
            continue

        # Categorize other cards
        if 'Walpurgis' in title:
            walpurgis_cards_html += card
        elif 'THP' in card or 'Horizon Protocol' in card:
            thp_cards_html += card
        elif 'Country-related' in title:
            countries_cards_html += card
        else:
            others_cards_html += card

# --- 3. Add the new link ---
new_card_html = '''
<div class="card">
    <h3>Neutral Convergence: A Strategic Analysis of the Silent Singularity</h3>
    <p>An initial analysis of the ontological status of AI and the transformation it brings to industrial and social structures. Includes a thought experiment-based approach.</p>
    <small class="muted">Updated: 2025-09-19</small>
    <p><a href="reports/Neutral_Convergence_EN.html">Open Report</a></p>
</div>
'''

others_cards_html = new_card_html + lobotomy_card_html + others_cards_html

# --- 4. Build the new HTML ---

new_html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Reference Hub - 9.30 Operations</title>
    <link rel="stylesheet" href="/assets/css/Economy_0930-E_style.css"/>
    <style>
        .accordion {{
            background-color: #eee;
            color: #444;
            cursor: pointer;
            padding: 18px;
            width: 100%;
            border: none;
            text-align: left;
            outline: none;
            font-size: 15px;
            transition: 0.4s;
            margin-top: 10px;
        }}

        .active, .accordion:hover {{
            background-color: #ccc;
        }}

        .panel {{
            padding: 0 18px;
            background-color: white;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.2s ease-out;
        }}
        .card-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            padding-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Reference Hub</h1>
            <p class="muted">Top-priority materials are at the top, with related materials organized by category.</p>
        </header>

        <section class="category">
            <h2>Top Priority Materials</h2>
            <div class="card-grid">
                {important_walpurgis_html}
                {important_thp_html}
            </div>
        </section>

        <button class="accordion">Walpurgis Related</button>
        <div class="panel">
            <div class="card-grid">
                {walpurgis_cards_html}
            </div>
        </div>

        <button class="accordion">THP Related</button>
        <div class="panel">
            <div class="card-grid">
                {thp_cards_html}
            </div>
        </div>

        <button class="accordion">Country-related economic conditions</button>
        <div class="panel">
            <div class="card-grid">
                {countries_cards_html}
            </div>
        </div>

        <button class="accordion">Others</button>
        <div class="panel">
            <div class="card-grid">
                {others_cards_html}
            </div>
        </div>

        <footer>
            <p><a href="./index.html">Return to top page</a></p>
        </footer>
    </div>

    <script>
        var acc = document.getElementsByClassName("accordion");
        var i;

        for (i = 0; i < acc.length; i++) {{
            acc[i].addEventListener("click", function() {{
                this.classList.toggle("active");
                var panel = this.nextElementSibling;
                if (panel.style.maxHeight) {{
                    panel.style.maxHeight = null;
                }} else {{
                    panel.style.maxHeight = panel.scrollHeight + "px";
                }}
            }});
        }}
    </script>
</body>
</html>
'''

# Write the new html to the file
with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_html)

print("File tuned successfully.")
