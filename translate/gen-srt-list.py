import whisper
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tqdm import tqdm

# Cấu hình đường dẫn FFmpeg (nếu cần)
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg-7.1.1-full_build-shared\bin"


def select_audio_files():
    """Hiển thị hộp thoại chọn nhiều file .wav"""
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ chính
    file_paths = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.wav")], title="Chọn tệp WAV")
    return file_paths


def transcribe_audio(audio_path):
    """Nhận diện giọng nói từ file âm thanh với thanh tiến trình"""
    model = whisper.load_model("small")  # Có thể đổi sang 'base', 'medium', 'large'

    print(f"📝 Đang nhận diện giọng nói từ: {os.path.basename(audio_path)}...")
    result = model.transcribe(audio_path, verbose=False)  # Tắt log chi tiết

    segments = result["segments"]

    for _ in tqdm(range(len(segments)), desc="Đang xử lý...", unit=" segment"):
        pass  # Hiển thị tiến trình

    return segments


def format_time(seconds):
    """Chuyển đổi thời gian thành định dạng SRT"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"


def save_srt(segments, audio_path):
    """Lưu phụ đề dưới dạng file .srt"""
    srt_path = os.path.splitext(audio_path)[0] + ".srt"

    if not segments:
        print(f"❌ Không có phụ đề nào được nhận diện cho {os.path.basename(audio_path)}!")
        return

    try:
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, segment in enumerate(segments, start=1):
                start_time = format_time(segment["start"])
                end_time = format_time(segment["end"])
                text = segment["text"].strip()

                f.write(f"{i}\n{start_time} --> {end_time}\n{text}\n\n")

        print(f"✅ Phụ đề đã lưu tại: {srt_path}")
    except Exception as e:
        print(f"❌ Lỗi khi lưu tệp SRT: {e}")


if __name__ == "__main__":
    audio_files = select_audio_files()

    if not audio_files:
        print("❌ Không có tệp nào được chọn!")
        exit()

    for audio_file in audio_files:
        if not os.path.exists(audio_file):
            print(f"❌ File không tồn tại: {audio_file}")
            continue

        segments = transcribe_audio(audio_file)
        print("💾 Đang lưu phụ đề...")
        save_srt(segments, audio_file)
        print(f"🎉 Hoàn tất! Phụ đề cho {os.path.basename(audio_file)} đã được tạo.")

    messagebox.showinfo("Hoàn tất", "Tất cả các tệp đã được xử lý xong!")
