
import re

# File path
file_path = r'G:\マイドライブ\Guide-Website\Economy\0930\reference-materials.html'

# Read the original HTML content
with open(file_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# --- 1. Find the Lobotomy card and move it ---
lobotomy_card = None
cards = re.findall(r'<div class="card">.*?</div>', html_content, re.DOTALL)
for card in cards:
    if 'ロボトミー' in card:
        lobotomy_card = card
        html_content = html_content.replace(card, '') # Remove it from its original place
        break

# --- 2. Add the new link and the lobotomy card to the "その他" section ---
new_card_html = '''
<div class="card">
    <h3>Neutral Convergence（中立的収束）に関する初期分析レポート</h3>
    <p>AIの存在論的地位と、それが産業・社会構造に与える変革についての初期分析。思考実験的アプローチを含みます。</p>
    <small class="muted">更新日: 2025-09-19</small>
    <p><a href="reports/中立収束：AI存在論と産業構造の静かな変革.html">レポートを開く</a></p>
</div>
'''

# Find the "その他" section and add the new card and the lobotomy card
others_section_match = re.search(r'(<button class="accordion">その他</button>\s*<div class="panel">\s*<div class="card-grid">)', html_content, re.DOTALL)

if others_section_match:
    insertion_point = others_section_match.end()
    if lobotomy_card:
        new_content = html_content[:insertion_point] + new_card_html + lobotomy_card + html_content[insertion_point:]
    else:
        new_content = html_content[:insertion_point] + new_card_html + html_content[insertion_point:]
else:
    # If the "その他" section doesn't exist for some reason, we just append it at the end before the footer.
    new_content = html_content.replace('<footer>', '<button class="accordion">その他</button>\n<div class="panel">\n<div class="card-grid">\n' + new_card_html + (lobotomy_card if lobotomy_card else '') + '</div>\n</div>\n<footer>')

# Write the new html to the file
with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("File tuned successfully again.")
