import os
import time
import pyautogui
import base64

def auto_capture_screenshots(screenshot_path, screenshot_interval, stop_event, shared_data, lock):
    if not os.path.exists(screenshot_path):
        os.makedirs(screenshot_path)

    while not stop_event.is_set():
        timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
        screenshot_filename = f'{screenshot_path}/{timestamp}.png'
        pyautogui.screenshot().save(screenshot_filename)
        print(f'自动截图保存至路径: {screenshot_filename}')

        with open(screenshot_filename, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        with lock:
            shared_data['base64_image'] = encoded_image
            print("自动截图 base64_image 已更新")

        stop_event.wait(screenshot_interval)

    print("自动截图线程已退出。")
