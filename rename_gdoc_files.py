
import os
import re
import unicodedata

def sanitize_filename_for_windows(filename):
    # Windowsで無効な文字をアンダースコアに置き換える
    # また、制御文字も除去する
    sanitized = re.sub(r'[\\/:*?"<>|\x00-\x1f]', '_', filename)
    # ファイル名の末尾のピリオドはWindowsで問題になる場合があるため除去
    sanitized = sanitized.rstrip('.')
    # Unicode正規化 (NFC) を適用して、結合文字などを単一文字に変換
    sanitized = unicodedata.normalize('NFC', sanitized)
    return sanitized

def rename_gdoc_files(directory):
    print(f"Starting file rename process in: {directory}")
    renamed_count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".gdoc"):
                original_file_path = os.path.join(root, file)
                sanitized_filename = sanitize_filename_for_windows(file)
                
                if file != sanitized_filename:
                    new_file_path = os.path.join(root, sanitized_filename)
                    try:
                        # 同じ名前のファイルが既に存在する場合はスキップまたはリネーム戦略を検討
                        if os.path.exists(new_file_path):
                            print(f"Warning: Skipped renaming '{original_file_path}' to '{new_file_path}' because target already exists.")
                            continue
                        
                        os.rename(original_file_path, new_file_path)
                        print(f"Renamed: '{original_file_path}' -> '{new_file_path}'")
                        renamed_count += 1
                    except OSError as e:
                        print(f"Error renaming '{original_file_path}' to '{new_file_path}': {e}")
                    except Exception as e:
                        print(f"An unexpected error occurred during renaming '{original_file_path}': {e}")
    
    print(f"Finished file rename process. Total renamed files: {renamed_count}")

# --- ここから設定 ---
TARGET_DIRECTORY = r"G:\マイドライブ\Guide-Website\gdoc"
# --- 設定はここまで ---

if __name__ == "__main__":
    if os.path.isdir(TARGET_DIRECTORY):
        rename_gdoc_files(TARGET_DIRECTORY)
    else:
        print(f"Error: The specified directory does not exist. -> {TARGET_DIRECTORY}")
