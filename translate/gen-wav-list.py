import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from tqdm import tqdm

# Cấu hình đường dẫn FFmpeg
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg-7.1.1-full_build-shared\bin"


def select_files():
    """Hiển thị hộp thoại chọn nhiều tệp MP4"""
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(filetypes=[("MP4 Files", "*.mp4")], title="Chọn tệp MP4")
    return file_paths


def convert_mp4_to_wav(mp4_paths):
    """Chuyển đổi danh sách tệp MP4 sang WAV bằng FFmpeg"""
    for mp4_path in tqdm(mp4_paths, desc="Chuyển đổi MP4 → WAV", unit=" file"):
        wav_path = os.path.splitext(mp4_path)[0] + ".wav"
        ffmpeg_cmd = ["ffmpeg", "-i", mp4_path, "-ac", "1", "-ar", "16000", "-y", wav_path]

        try:
            subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"✅ Đã tạo WAV: {wav_path}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Lỗi FFmpeg: {e}")


if __name__ == "__main__":
    # Chọn nhiều file MP4
    mp4_files = select_files()

    if not mp4_files:
        print("❌ Không có file nào được chọn!")
        exit()

    # Bắt đầu chuyển đổi
    convert_mp4_to_wav(mp4_files)
    print("🎉 Hoàn tất chuyển đổi!")
    messagebox.showinfo("Hoàn tất", "Tất cả các tệp MP4 đã được chuyển đổi thành WAV.")
