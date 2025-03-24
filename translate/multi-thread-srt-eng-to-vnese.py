import os
import tkinter as tk
from tkinter import filedialog, messagebox
from deep_translator import GoogleTranslator
import re
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def select_srt_files():
    """Hiển thị hộp thoại chọn nhiều file .srt"""
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(filetypes=[("SRT Files", "*.srt")], title="Chọn tệp SRT để dịch")
    return file_paths

def translate_text(text, source_lang="en", target_lang="vi"):
    """Dịch văn bản từ tiếng Anh sang tiếng Việt"""
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        return translator.translate(text)
    except Exception as e:
        print(f"❌ Lỗi khi dịch: {e}")
        return text  # Trả về nguyên văn nếu lỗi

def translate_srt(srt_path):
    """Dịch nội dung của file .srt hiện có và lưu thành tệp mới"""
    translated_srt_path = os.path.splitext(srt_path)[0] + "_vi.srt"

    try:
        with open(srt_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        translated_lines = []
        text_lines = [line.strip() for line in lines if line.strip() and not re.match(r"^\d+$", line) and "-->" not in line]

        print(f"📄 Đang dịch: {os.path.basename(srt_path)} ({len(text_lines)} dòng cần dịch)")

        for line in tqdm(lines, desc=f"🔄 Dịch {os.path.basename(srt_path)}", unit=" dòng"):
            if re.match(r"^\d+$", line.strip()) or "-->" in line:
                translated_lines.append(line)  # Giữ nguyên số thứ tự & timestamp
            else:
                translated_text = translate_text(line.strip())  # Dịch nội dung
                translated_lines.append(translated_text + "\n")

        with open(translated_srt_path, "w", encoding="utf-8") as f:
            f.writelines(translated_lines)

        print(f"✅ Đã dịch xong: {translated_srt_path}")
    except Exception as e:
        print(f"❌ Lỗi khi xử lý tệp {srt_path}: {e}")

if __name__ == "__main__":
    srt_files = select_srt_files()

    if not srt_files:
        print("❌ Không có tệp nào được chọn!")
        exit()

    max_threads = min(4, len(srt_files))  # Chạy tối đa 4 luồng hoặc số tệp có sẵn

    with ThreadPoolExecutor(max_threads) as executor:
        executor.map(translate_srt, srt_files)

    messagebox.showinfo("Hoàn tất", "Tất cả các tệp SRT đã được dịch xong!")
