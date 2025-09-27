import os
import shutil
from pathlib import Path

# Define base paths
reports_dir = Path(r'F:\マイドライブ\Guide-Website\Economy\0930\reports')
md_dir = reports_dir / 'md'

# Create the new 'md' directory
md_dir.mkdir(exist_ok=True)

# --- Move HTML files ---
html_files_moved = 0
for html_file in reports_dir.rglob('*.html'):
    if html_file.parent != reports_dir:
        dest_path = reports_dir / html_file.name
        try:
            if dest_path.exists():
                continue
            shutil.move(str(html_file), str(dest_path))
            html_files_moved += 1
        except Exception:
            pass # Fail silently
print(f"Moved {html_files_moved} HTML files.")

# --- Move MD files ---
md_files_moved = 0
md_file_list = list(reports_dir.rglob('*.md'))
for md_file in md_file_list:
    if md_file.is_file() and not str(md_file.resolve()).startswith(str(md_dir.resolve())):
        try:
            relative_to_reports = md_file.relative_to(reports_dir)
            dest_path = md_dir / relative_to_reports
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(md_file), str(dest_path))
            md_files_moved += 1
        except Exception:
            pass # Fail silently
print(f"Moved {md_files_moved} MD files.")

# --- Cleanup ---
for root, dirs, files in os.walk(reports_dir, topdown=False):
    if Path(root).resolve() == reports_dir.resolve() or (md_dir.exists() and Path(root).resolve().is_relative_to(md_dir.resolve())):
        continue
    if not os.listdir(root):
        try:
            os.rmdir(root)
        except Exception:
            pass # Fail silently

print("Refactoring complete.")
