import os
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg-7.1.1-full_build-shared\bin"

import shutil
print(shutil.which("ffmpeg"))  # Kiểm tra lại
