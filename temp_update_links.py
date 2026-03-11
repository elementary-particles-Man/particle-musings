
import os
import re

# The absolute path to the project root.
project_root = r"G:\マイドライブ\Guide-Website"
assets_css_dir = os.path.join(project_root, "assets", "css")

css_map = {}
# 1. Create a mapping from old CSS paths to new paths.
for filename in os.listdir(assets_css_dir):
    if filename.endswith(".css"):
        new_path = f"/assets/css/{filename}"
        
        # Reconstruct the original path
        # Handle the files that were already in assets
        if filename in ["Style_root.css", "Style_contents.css", "Style_LOG.css", "Style_sub.css"]:
            # These files were originally in assets, so their old path would be relative to the html files.
            # For simplicity, we will handle these as special cases.
            css_map[filename] = new_path
            css_map[f"./{filename}"] = new_path
            css_map[f"../{filename}"] = new_path
            css_map[f"../../{filename}"] = new_path
            css_map[f"../../../{filename}"] = new_path
            css_map[f"../../../../{filename}"] = new_path
            css_map[f"assets/css/{filename}"] = new_path
            css_map[f"/assets/css/{filename}"] = new_path
            css_map[f"../assets/css/{filename}"] = new_path
            css_map[f"../../assets/css/{filename}"] = new_path
            css_map[f"../../../assets/css/{filename}"] = new_path
            css_map[f"../../../../assets/css/{filename}"] = new_path
            css_map[f"../assets/{filename}"] = new_path
            css_map[f"../../assets/{filename}"] = new_path
            css_map[f"../../../assets/{filename}"] = new_path
            css_map[f"../../../../assets/{filename}"] = new_path
            css_map[f"assets/{filename}"] = new_path
            css_map[f"/assets/{filename}"] = new_path

        else:
            # Reconstruct path from filename like "Economy_0930_style.css"
            parts = filename.replace(".css", "").split("_")
            
            # The last part is the original filename, e.g., "style"
            original_filename = parts[-1] + ".css"
            
            # The rest of the parts form the directory path
            original_dir_parts = parts[:-1]
            
            # A special case for "style_old_media"
            if filename == "political_old_media_style_old_media.css":
                original_filename = "style_old_media.css"
                original_dir_parts = ["political", "old_media"]

            # Another special case for THP-HTML
            if "THP-HTML" in filename:
                original_dir_parts = ["Economy", "0930", "THP", "THP-HTML"]
                original_filename = "style.css"

            original_path_rel = os.path.join(*original_dir_parts, original_filename).replace("\\", "/")

            # The issue is that we don't know the original relative path from the HTML file.
            # Let's just search for the filename.
            css_map[original_filename] = new_path


# 2. Scan all HTML files and replace CSS links.
for root, _, files in os.walk(project_root):
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, "r+", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    original_content = content
                    
                    # General replacement for any css file
                    content = re.sub(r'href="([^ "]*?)"', lambda m: f'href="{css_map.get(m.group(1).split("/")[-1], m.group(0)[6:-1])}"', content)

                    # Also handle the case where the path is already relative to the assets directory
                    content = re.sub(r'href="\./(assets/.*?)"', r'href="/\1"', content)
                    content = re.sub(r'href="(assets/.*?)"', r'href="/\1"', content)
                    
                    # Normalize image paths
                    content = re.sub(r'src="\./(assets/images/.*?)"', r'src="/\1"', content)
                    content = re.sub(r'src="(assets/images/.*?)"', r'src="/\1"', content)

                    if content != original_content:
                        f.seek(0)
                        f.truncate()
                        f.write(content)
                        print(f"Updated links in: {filepath}")
            except Exception as e:
                print(f"Could not process {filepath}: {e}")

print("HTML link normalization complete.")
