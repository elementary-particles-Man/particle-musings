import re
import os

# File path
file_path = r'G:\マイドライブ\Guide-Website\Economy\0930\reference-materials.html'

# Read the original HTML content
with open(file_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# --- 1. Remove Royenthal content ---
# This is tricky without a proper parser. We'll find the cards and remove them.
# A card starts with <div class="card"> and ends with </div>
# We'll find the cards containing the keyword and remove them.

cards = re.findall(r'<div class="card">.*?</div>', html_content, re.DOTALL)
royenthal_cards = [card for card in cards if 'ロイエンタール' in card]

for card in royenthal_cards:
    html_content = html_content.replace(card, '')

# --- 2. Categorize all cards ---
# We will extract all cards from each category and store them.

sections = re.findall(r'<section class="category">.*?</section>', html_content, re.DOTALL)

walpurgis_cards_html = ''
thp_cards_html = ''
countries_cards_html = ''
others_cards_html = ''

# Important links
important_walpurgis_html = ''
important_thp_html = ''

for section in sections:
    title = re.search(r'<h2>(.*?)</h2>', section).group(1)
    cards_in_section = re.findall(r'<div class="card">.*?</div>', section, re.DOTALL)

    for card in cards_in_section:
        # Check for important cards first
        if 'プロジェクト・ワルプルギス再評価' in card:
            important_walpurgis_html = card
            continue
        if 'The Horizon Protocol' in card:
            important_thp_html = card
            # Add the note about vulnerability
            important_thp_html = important_thp_html.replace('</p>', '<br><b>（現在、その脆弱性について対応作業中です）</b></p>')
            continue

        # Categorize other cards
        if 'ワルプルギス' in title:
            walpurgis_cards_html += card
        elif 'THP' in card or 'Horizon Protocol' in card:
            thp_cards_html += card
        elif '各国関連' in title:
            countries_cards_html += card
        else:
            others_cards_html += card

# --- 3. Build the new HTML ---

new_html = f'''
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>参考資料ハブ - 9.30 オペレーション</title>
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
            <h1>参考資料ハブ</h1>
            <p class="muted">最重要資料をトップに、関連資料をカテゴリ別に整理しました。</p>
        </header>

        <section class="category">
            <h2>共通最優先資料</h2>
            <div class="card-grid">
                {important_walpurgis_html}
                {important_thp_html}
            </div>
        </section>

        <button class="accordion">ワルプルギス関連</button>
        <div class="panel">
            <div class="card-grid">
                {walpurgis_cards_html}
            </div>
        </div>

        <button class="accordion">THP関連</button>
        <div class="panel">
            <div class="card-grid">
                {thp_cards_html}
            </div>
        </div>

        <button class="accordion">各国経済事情</button>
        <div class="panel">
            <div class="card-grid">
                {countries_cards_html}
            </div>
        </div>

        <button class="accordion">その他</button>
        <div class="panel">
            <div class="card-grid">
                {others_cards_html}
            </div>
        </div>

        <footer>
            <p><a href="./index.html">トップページへ戻る</a></p>
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