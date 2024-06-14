import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def remove_s_from_txp_files(directory):
    """
    .txpファイルから's'を削除し、変更をログに記録する。
    """
    log_file_path = os.path.join(directory, "rename_log.txt")
    try:
        with open(log_file_path, "w") as log_file:
            for filename in os.listdir(directory):
                if filename.endswith(".txp"):
                    match = re.match(r"(x=\d+(\.\d+)?)(s)(\.txp)", filename)
                    if match:
                        base_name, _, s, extension = match.groups()
                        new_filename = f"{base_name}{extension}"
                        old_file_path = os.path.join(directory, filename)
                        new_file_path = os.path.join(directory, new_filename)

                        shutil.move(old_file_path, new_file_path)

                        log_file.write(f"{new_filename} <- {filename}\n")
                        print(f"Renamed: {filename} -> {new_filename}")
    except Exception as e:
        messagebox.showerror("エラー", f"'s'の削除に失敗しました: {e}")

def add_s_to_txp_and_pl3_files(directory):
    """
    ログに基づいて対応する.txpファイルに's'を再追加し、
    対応する.pl3ファイルにも's'を追加する。
    """
    log_file_path = os.path.join(directory, "rename_log.txt")
    if not os.path.exists(log_file_path):
        messagebox.showerror("エラー", "ログファイルが見つかりません。操作が実行されませんでした。")
        return

    try:
        with open(log_file_path, "r") as log_file:
            for line in log_file:
                try:
                    if ' <- ' in line:
                        new_filename, old_filename = line.strip().split(' <- ')
                        base_name_match = re.match(r"(x=\d+(\.\d+)?)(\.txp)", new_filename)
                        if base_name_match:
                            base_name = base_name_match.group(1)
                            new_txp_filename = f"{base_name}s.txp"
                            old_file_path = os.path.join(directory, new_filename)
                            new_file_path = os.path.join(directory, new_txp_filename)

                            if os.path.exists(old_file_path):
                                shutil.move(old_file_path, new_file_path)
                                print(f"Reverted: {new_filename} -> {new_txp_filename}")
                            else:
                                print(f"ファイルが見つかりません: {old_file_path}")

                            old_pl3_filename = f"{base_name}.pl3"
                            new_pl3_filename = f"{base_name}s.pl3"
                            old_pl3_path = os.path.join(directory, old_pl3_filename)
                            new_pl3_path = os.path.join(directory, new_pl3_filename)

                            if os.path.exists(old_pl3_path):
                                shutil.move(old_pl3_path, new_pl3_path)
                                print(f"Renamed: {old_pl3_filename} -> {new_pl3_filename}")
                            else:
                                print(f"ファイルが見つかりません: {old_pl3_path}")
                except Exception as e:
                    print(f"行の処理中にエラーが発生しました: {line}, エラー: {e}")

    except Exception as e:
        messagebox.showerror("エラー", f"'s'の再追加に失敗しました: {e}")

class FileRenamingTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Renaming Tool for TXP and PL3")
        self.geometry("400x200")
        self.directory = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # ディレクトリ選択ラベルとエントリ
        tk.Label(self, text="ディレクトリ:").pack(pady=5)
        tk.Entry(self, textvariable=self.directory, width=50).pack(pady=5)
        tk.Button(self, text="参照", command=self.browse_directory).pack(pady=5)

        # 's'を削除するボタンと's'を追加するボタン
        tk.Button(self, text=".txpファイルから's'を削除", command=self.remove_s).pack(pady=5)
        tk.Button(self, text=".txpファイルと.pl3ファイルに's'を追加", command=self.add_s).pack(pady=5)

    def browse_directory(self):
        # ディレクトリ選択ダイアログを開く
        dir_name = filedialog.askdirectory()
        if dir_name:
            self.directory.set(dir_name)

    def remove_s(self):
        directory = self.directory.get()
        if directory:
            try:
                remove_s_from_txp_files(directory)
                messagebox.showinfo("完了", ".txpファイルから's'を削除しました。")
            except Exception as e:
                messagebox.showerror("エラー", f"操作に失敗しました: {e}")
        else:
            messagebox.showerror("エラー", "ディレクトリを選択してください。")

    def add_s(self):
        directory = self.directory.get()
        if directory:
            try:
                if not os.path.exists(os.path.join(directory, "rename_log.txt")):
                    messagebox.showerror("エラー", "ログファイルが見つかりません。操作が実行されませんでした。")
                    return

                add_s_to_txp_and_pl3_files(directory)
                messagebox.showinfo("完了", ".txpファイルと.pl3ファイルに's'を追加しました。")
            except Exception as e:
                messagebox.showerror("エラー", f"操作に失敗しました: {e}")
        else:
            messagebox.showerror("エラー", "ディレクトリを選択してください。")

if __name__ == "__main__":
    app = FileRenamingTool()
    app.mainloop()
