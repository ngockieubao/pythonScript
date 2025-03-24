import whisper
import os
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg-7.1.1-full_build-shared\bin"

def select_audio_file():
    """Hiển thị hộp thoại chọn file .wav"""
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ chính
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
    return file_path


def transcribe_audio(audio_path):
    """Nhận diện giọng nói từ file âm thanh với thanh tiến trình"""
    model = whisper.load_model("small")  # Có thể đổi sang 'base', 'medium', 'large'

    print("📝 Đang nhận diện giọng nói...")
    result = model.transcribe(audio_path, verbose=True)  # Bật log chi tiết

    segments = result["segments"]

    for i in tqdm(range(len(segments)), desc="Đang xử lý...", unit=" segment"):
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
        print("❌ Không có phụ đề nào được nhận diện!")
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
    audio_file = select_audio_file()

    if not audio_file:
        print("❌ Không có file nào được chọn!")
    elif not os.path.exists(audio_file):
        print("❌ File không tồn tại!")
    else:
        segments = transcribe_audio(audio_file)
        print("💾 Đang lưu phụ đề...")
        save_srt(segments, audio_file)
        print("🎉 Hoàn tất! Phụ đề đã được tạo.")
