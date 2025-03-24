import wave
import tkinter as tk
from tkinter import filedialog

def select_audio_file():
    """Mở hộp thoại chọn file .wav"""
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ chính
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
    return file_path

# Chọn file thông qua hộp thoại
audio_path = select_audio_file()

if not audio_path:
    print("❌ Không có file nào được chọn!")
else:
    try:
        with wave.open(audio_path, "rb") as wav_file:
            print(f"✅ File hợp lệ: {wav_file.getnchannels()} kênh, {wav_file.getsampwidth()} byte, {wav_file.getframerate()} Hz")
    except wave.Error as e:
        print(f"❌ File bị lỗi: {e}")
