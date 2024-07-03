import os

def remove_text_from_filename(file_name, remove_text):
    # remove_textが空でない場合は文字列を削除
    if remove_text:
        new_file_name = file_name.replace(remove_text, "")
    else:
        # remove_textが空の場合は何もせずにそのままのファイル名を使用
        new_file_name = file_name
    return new_file_name

def replace_text_in_filename(file_name, old_text, new_text):
    # old_textが存在する場合は新しい文字列で置換
    new_file_name = file_name.replace(old_text, new_text)
    return new_file_name

def rename_files_in_directory(directory_path, remove_or_replace, old_text="", new_text="", subdirectories=False):
    # フォルダ内のファイル一覧を取得
    if subdirectories:
        # サブディレクトリを含む場合
        files = []
        for root, dirs, filenames in os.walk(directory_path):
            for filename in filenames:
                files.append(os.path.join(root, filename))
    else:
        # フォルダ直下のファイルのみ
        files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]

    # print(files)

    # ファイルごとに処理
    for file_path in files:
        # 新しいファイル名を生成
        if remove_or_replace == "remove":
            new_file_name = remove_text_from_filename(os.path.basename(file_path), old_text)
        elif remove_or_replace == "replace":
            new_file_name = replace_text_in_filename(os.path.basename(file_path), old_text, new_text)
        else:
            print("無効な選択です。")
            return

        # 新しいファイルのパスを作成
        new_path = os.path.join(os.path.dirname(file_path), new_file_name)

        # ファイルをリネーム
        os.rename(file_path, new_path)

if __name__ == "__main__":
    # ディレクトリのパスを入力
    directory_path = input("ディレクトリのパスを入力してください: ")

    # 削除か置換か選択
    remove_or_replace = input("削除する場合は 'remove'、置換する場合は 'replace' を入力してください: ")

    # サブディレクトリを含めるかどうかの選択
    subdirectories = input("サブディレクトリを含めますか？ (Yes/No): ").lower() == "yes"

    if remove_or_replace == "remove":
        # 削除したい文字列を入力
        remove_text = input("削除したい文字列を入力してください: ")
        rename_files_in_directory(directory_path, remove_or_replace, remove_text, subdirectories=subdirectories)
    elif remove_or_replace == "replace":
        # 置換したい文字列を入力
        old_text = input("置換したい文字列を入力してください: ")
        # 置換後の文字列を入力
        new_text = input("置換後の文字列を入力してください: ")
        rename_files_in_directory(directory_path, remove_or_replace, old_text, new_text, subdirectories=subdirectories)
    else:
        print("無効な選択です。")

    print("ファイルのリネームが完了しました。")
    key = input('Press Enter to exit')