import pyautogui
import time

def click_at_position(x, y):
    # Di chuyển đến vị trí (x, y)
    pyautogui.moveTo(x, y)
    # Click chuột trái
    pyautogui.click()

# Thời gian chờ trước khi bắt đầu
print("Bạn có 5 giây để chuyển đến cửa sổ trình duyệt...")
time.sleep(5)

# Vị trí cố định mà bạn muốn click (thay đổi theo nhu cầu)
# Bạn có thể sử dụng hàm get_mouse_position.py để xác định tọa độ này
x = 1868  # Ví dụ tọa độ X
y = 917  # Ví dụ tọa độ Y

try:
    while True:
        click_at_position(x, y)
        time.sleep(0.001)  # Thời gian chờ giữa các lần click
except KeyboardInterrupt:
    print("Đã dừng chương trình.")
