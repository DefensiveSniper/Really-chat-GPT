from func.audio_play import play_mp3
import os
import time
import glob
import base64
import pyautogui

# 手动截屏
def hand_capture_screenshot(screenshot_path):
    try:
        if not os.path.exists(screenshot_path):
            os.makedirs(screenshot_path)

        timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
        screenshot_filename = f'{screenshot_path}/{timestamp}.png'
        pyautogui.screenshot().save(screenshot_filename)
        print(f'截图保存至路径: {screenshot_filename}')
    except Exception as e:
        print(f"An error occurred while taking a screenshot: {e}")

# 截图并返回Base64编码的图像
def capture_screenshot(screenshot_path):
    try:
        play_mp3('./media/success.mp3')  # 确保这行代码没有问题
        hand_capture_screenshot(screenshot_path)  # 截图并保存
        files = glob.glob(os.path.join(screenshot_path, '*.png'))
        latest_file = max(files, key=os.path.getmtime)
        with open(latest_file, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        print(f"An error occurred while capturing the screenshot: {e}")
        return ""
