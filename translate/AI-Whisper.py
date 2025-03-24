import os
import subprocess
import whisper
import tkinter as tk
from tkinter import filedialog, messagebox
from tqdm import tqdm

os.environ["PATH"] += os.pathsep + r"C:\ffmpeg-7.1.1-full_build-shared\bin"

def select_file(file_types, title):
    """Hiển thị hộp thoại chọn file"""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=file_types, title=title)
    return file_path


def convert_mp4_to_wav(mp4_path):
    """Chuyển đổi MP4 sang WAV bằng FFmpeg"""
    wav_path = os.path.splitext(mp4_path)[0] + ".wav"
    ffmpeg_cmd = [
        "ffmpeg", "-i", mp4_path, "-ac", "1", "-ar", "16000", "-y", wav_path
    ]

    print("🎬 Đang chuyển đổi MP4 → WAV...")
    try:
        subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"✅ Đã tạo WAV: {wav_path}")
        return wav_path
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi FFmpeg: {e}")
        messagebox.showerror("Lỗi", "Không thể chuyển đổi MP4 sang WAV!")
        return None


def transcribe_audio(audio_path):
    """Nhận diện giọng nói từ file âm thanh"""
    model = whisper.load_model("small")
    print("📝 Đang nhận diện giọng nói...")
    result = model.transcribe(audio_path, verbose=True)

    segments = result["segments"]
    for _ in tqdm(range(len(segments)), desc="Đang xử lý...", unit=" segment"):
        pass

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
        #messagebox.showinfo("Hoàn tất", f"Phụ đề đã được lưu:\n{srt_path}")
    except Exception as e:
        print(f"❌ Lỗi khi lưu tệp SRT: {e}")


if __name__ == "__main__":
    # Chọn file MP4
    mp4_file = select_file([("MP4 Files", "*.mp4")], "Chọn tệp MP4")

    if not mp4_file:
        print("❌ Không có file MP4 nào được chọn!")
        exit()

    # Chuyển đổi MP4 sang WAV
    wav_file = convert_mp4_to_wav(mp4_file)

    if not wav_file:
        exit()

    # Chọn file WAV
    wav_file = select_file([("WAV Files", "*.wav")], "Chọn tệp WAV")
    if not wav_file:
        print("❌ Không có file WAV nào được chọn!")
        exit()

    # Nhận diện giọng nói và tạo SRT
    segments = transcribe_audio(wav_file)
    print("💾 Đang lưu phụ đề...")
    save_srt(segments, wav_file)
    print("🎉 Hoàn tất!")
