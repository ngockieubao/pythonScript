import pyautogui
import time

print("Di chuyển chuột đến vị trí bạn muốn. Thời gian chờ 5 giây...")
time.sleep(5)

# Lấy vị trí hiện tại của con trỏ chuột
x, y = pyautogui.position()
print(f"Vị trí con trỏ chuột hiện tại: X: {x}, Y: {y}")
