
import os
import shutil
from datetime import datetime

def move_gdoc_files_by_timestamp(source_directory, destination_directory_prefix, cutoff_date_str):
    """
    指定された日付以前に最終更新された.gdocファイルを指定のディレクトリに移動する。
    """
    moved_count = 0
    
    try:
        # カットオフ日付をdatetimeオブジェクトに変換
        cutoff_date = datetime.strptime(cutoff_date_str, "%Y-%m-%d")
    except ValueError:
        print(f"Error: Invalid date format for cutoff_date_str. Please use YYYY-MM-DD (e.g., 2025-04-01).")
        return

    # 移動先ディレクトリの名前を生成
    destination_folder_name = f"{destination_directory_prefix}_{cutoff_date.strftime('%Y年%m月以前')}"
    full_destination_path = os.path.join(source_directory, destination_folder_name)

    # ソースディレクトリを再帰的に検索
    for root, _, files in os.walk(source_directory):
        # 移動先フォルダ自体は検索対象から除外（無限ループ防止）
        if root == full_destination_path or root.startswith(full_destination_path + os.sep):
            continue

        for file in files:
            if file.endswith(".gdoc"):
                file_path = os.path.join(root, file)
                try:
                    # ファイルの最終更新日時を取得 (UNIXタイムスタンプ)
                    timestamp = os.path.getmtime(file_path)
                    
                    # UNIXタイムスタンプをdatetimeオブジェクトに変換
                    file_modified_date = datetime.fromtimestamp(timestamp)

                    # 最終更新日時がカットオフ日付より前かチェック
                    # 日付のみを比較するため、時刻情報は無視
                    if file_modified_date.date() < cutoff_date.date():
                        # 移動先ディレクトリが存在しない場合は作成
                        if not os.path.exists(full_destination_path):
                            os.makedirs(full_destination_path)
                            print(f"Created destination directory: {full_destination_path}")
                        
                        # ファイルを移動
                        destination_file_path = os.path.join(full_destination_path, file)
                        shutil.move(file_path, destination_file_path)
                        print(f"Moved: '{file_path}' -> '{destination_file_path}'")
                        moved_count += 1
                except FileNotFoundError:
                    print(f"Warning: File not found (possibly moved or deleted): {file_path}")
                except OSError as e:
                    print(f"Error processing file '{file_path}': {e}")
                except Exception as e:
                    print(f"An unexpected error occurred for '{file_path}': {e}")

    if moved_count == 0:
        print(f"\nNo .gdoc files found or moved before {cutoff_date_str}.")
    else:
        print(f"\nSuccessfully moved {moved_count} .gdoc files to '{full_destination_path}'.")

# --- ここから設定 ---

# .gdocファイルが格納されている、対象のルートフォルダのパス
SOURCE_FOLDER = "G:\\マイドライブ\\Guide-Website\\gdoc"

# 移動先フォルダの接頭辞（例: '_OLD_' とすると '_OLD_2025年04月以前' となる）
DESTINATION_FOLDER_PREFIX = "_OLD"

# カットオフ日付を指定 (YYYY-MM-DD形式)
# この日付以前に最終更新されたファイルが移動されます。
CUTOFF_DATE = "2025-04-01"

# --- 設定はここまで ---


if __name__ == "__main__":
    if os.path.isdir(SOURCE_FOLDER):
        print("="*50)
        print("WARNING: This script will move files based on local file timestamps.")
        print(f"Target folder: {SOURCE_FOLDER}")
        print(f"Files modified before {CUTOFF_DATE} will be moved.")
        print("It is highly recommended to back up the folder before proceeding.")
        print("="*50)
        
        move_gdoc_files_by_timestamp(SOURCE_FOLDER, DESTINATION_FOLDER_PREFIX, CUTOFF_DATE)

    else:
        print(f"Error: The specified source folder does not exist. -> {SOURCE_FOLDER}")
