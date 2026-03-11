
import os
import sys

def run():
    # Get the absolute path of the script
    script_path = os.path.abspath(__file__)
    # Get the directory of the script (tools)
    tools_dir = os.path.dirname(script_path)
    # Get the root directory of the website (parent of tools)
    root_dir = os.path.dirname(tools_dir)

    print(f"Script running from: {script_path}")
    print(f"Website root directory: {root_dir}")

    # The string to search for
    search_string = '''href="/particle-musings/assets/css/'''

    # The directory to exclude
    exclude_dir = os.path.join(root_dir, 'Economy', '0930')
    print(f"Excluding directory: {exclude_dir}")

    # Counter for updated files
    updated_files_count = 0

    # Walk through the directory
    for dirpath, _, filenames in os.walk(root_dir):
        # Check if the current directory is within the excluded directory
        if os.path.abspath(dirpath).startswith(exclude_dir):
            continue

        for filename in filenames:
            if filename.endswith('.html'):
                file_path = os.path.join(dirpath, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    if search_string in content:
                        # Calculate the depth from the root
                        file_rel_path = os.path.relpath(file_path, root_dir)
                        depth = file_rel_path.count(os.path.sep)
                        
                        # Create the relative path prefix
                        relative_prefix = '../' * depth
                        
                        # The new string to replace with
                        replace_string = f'''href="{relative_prefix}assets/css/'''
                        
                        # Replace the string
                        new_content = content.replace(search_string, replace_string)
                        
                        # Write the changes back to the file
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        updated_files_count += 1
                        # Use forward slashes for display
                        print(f"Updated: {file_path.replace(os.sep, '/')}")

                except Exception as e:
                    print(f"Error processing file {file_path}: {e}", file=sys.stderr)

    print(f"\nCSS path replacement complete.")
    print(f"Total files updated: {updated_files_count}")

if __name__ == "__main__":
    run()
