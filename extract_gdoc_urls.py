import os
import json

def extract_gdoc_urls(search_directory, output_file):
    """
    指定されたディレクトリ内の.gdocファイルからURLを抽出し、
    テキストファイルに書き出す。
    """
    summary_entries = []
    # 指定されたディレクトリ以下のファイルを再帰的に検索
    for root, _, files in os.walk(search_directory):
        for file in files:
            if file.endswith(".gdoc"):
                original_file_path = os.path.join(root, file)
                file_name_without_ext = os.path.splitext(file)[0]
                
                try:
                    with open(original_file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'url' in data:
                            summary_entries.append(f"ファイル名: {file_name_without_ext}, URL: {data['url']}")
                except (OSError, json.JSONDecodeError):
                    pass
                except Exception:
                    pass

    # 抽出した情報をファイルに書き出す
    if summary_entries:
        with open(output_file, 'w', encoding='utf-8') as f:
            for entry in summary_entries:
                f.write(entry + "\n")
        return f"Successfully extracted {len(summary_entries)} entries to {output_file}"
    else:
        return f"No URLs were successfully extracted from .gdoc files in {search_directory}."


if __name__ == "__main__":
    gdoc_folder = "/mnt/f/マイドライブ/Guide-Website/gdoc"
    output_summary_file = "/mnt/f/マイドライブ/Guide-Website/gdoc_summary.txt"

    if os.path.isdir(gdoc_folder):
        result = extract_gdoc_urls(gdoc_folder, output_summary_file)
        print(result)
    else:
        print(f"Error: The specified folder does not exist. -> {gdoc_folder}")