import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from deep_translator import GoogleTranslator
import re
from tqdm import tqdm

os.environ["PATH"] += os.pathsep + r"C:\ffmpeg-7.1.1-full_build-shared\bin"

def select_srt_files():
    """Chọn nhiều file .srt"""
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilenames(filetypes=[("SRT Files", "*.srt")], title="Chọn tệp SRT để dịch")

def translate_text(text, source_lang="en", target_lang="vi"):
    """Dịch văn bản"""
    try:
        return GoogleTranslator(source=source_lang, target=target_lang).translate(text)
    except Exception:
        return text  # Nếu lỗi, giữ nguyên văn bản gốc

def translate_srt(srt_path, progress_bars, index):
    """Dịch file .srt và cập nhật tiến trình"""
    translated_srt_path = os.path.splitext(srt_path)[0] + "_vi.srt"

    with open(srt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    translated_lines = []
    text_lines = [line.strip() for line in lines if line.strip() and not re.match(r"^\d+$", line) and "-->" not in line]
    total_lines = len(text_lines)

    # Khởi tạo progress bar
    progress_bars[index] = tqdm(
        total=total_lines,
        unit=" dòng",
        position=index,
        leave=True,
        dynamic_ncols=True
    )
    progress_bars[index].set_description(f"🔄 {os.path.basename(srt_path)}")

    for line in lines:
        if re.match(r"^\d+$", line.strip()) or "-->" in line:
            translated_lines.append(line)
        else:
            translated_text = translate_text(line.strip())
            translated_lines.append(translated_text + "\n")
            progress_bars[index].update(1)
            progress_bars[index].refresh()

    # Xóa progress bar và in kết quả hoàn tất
    progress_bars[index].close()
    tqdm.write(f"✅ {os.path.basename(translated_srt_path)} hoàn tất!")

    with open(translated_srt_path, "w", encoding="utf-8") as f:
        f.writelines(translated_lines)

if __name__ == "__main__":
    srt_files = select_srt_files()

    if not srt_files:
        print("❌ Không có tệp nào được chọn!")
        exit()

    max_threads = min(4, len(srt_files))  # Chạy tối đa 4 luồng hoặc số tệp có sẵn
    threads = []
    progress_bars = [None] * len(srt_files)

    for i, file in enumerate(srt_files):
        thread = threading.Thread(target=translate_srt, args=(file, progress_bars, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    messagebox.showinfo("Hoàn tất", "Tất cả các tệp SRT đã được dịch xong!")
