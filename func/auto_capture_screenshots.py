import os
import time
import pyautogui

# 自动截屏
def auto_capture_screenshots(screenshot_path, screenshot_interval):
    global continue_screenshot, screenshot_filename
    if not os.path.exists(screenshot_path):
        os.makedirs(screenshot_path)

    while continue_screenshot:
        timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
        screenshot_filename = f'{screenshot_path}/{timestamp}.png'
        pyautogui.screenshot().save(screenshot_filename)
        print(f'截图保存至路径 saved: {screenshot_filename}')
        time.sleep(screenshot_interval)