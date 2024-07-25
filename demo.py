import keyboard
import glob
import base64
import os
import openai
from openai import OpenAI
# from func.capture_screenshot import capture_screenshot
from func.capture_screenshot import capture_screenshot
from func.recognize_from_microphone import recognize_from_microphone
from func.chat_respond import chat_respond
from func.generate_audio_stream import generate_audio_stream
from func.audio_play import play_mp3
from func.switch_model import switch_model
from func.read_file import file_parse

# 初始化
client = OpenAI(api_key = os.environ["OPENAI_API_KEY"])
screenshot_path = "./screenshots"# 截图保存路径
current_model = "gpt-4o-mini"
current_model_name = current_model
model_list = ["gpt-4o-mini","gpt-4o"]# 模型列表，需求更多模型请参考 https://platform.openai.com/docs/models
recognized_text = ""
base64_image = ""
new_screenshot = False
start_recognition, stop_recognition, recognized_text = recognize_from_microphone()

def gpt_reply(client, current_model_name, base64_image):
    global recognized_text
    response = chat_respond(client, recognized_text, base64_image, current_model_name)
    generate_audio_stream(response)
    recognized_text = ""
    base64_image = ""

def get_base64_image(screenshot_path):
    global base64_image
    base64_image = capture_screenshot(screenshot_path)
    
def get_file_content(client, current_model_name):
    global recognized_text, base64_image
    recognized_text, base64_image = file_parse(client, current_model_name)

def start_voice_recognition(e):
    play_mp3('./audio/success.mp3')
    start_recognition()

def stop_voice_recognition(client, current_model_name, base64_image):
    stop_recognition()
    global recognize_from_microphone, recognized_text
    exited_text = recognized_text
    recognized_text = recognize_from_microphone()[2]
    if exited_text:
        recognized_text += exited_text
    if recognized_text:
        gpt_reply(client, current_model_name, base64_image)

# 绑定按键组合
keyboard.add_hotkey('alt+b', lambda: get_base64_image(screenshot_path))
keyboard.on_press_key('menu', start_voice_recognition)
keyboard.on_release_key('menu', lambda e: stop_voice_recognition(client, current_model_name, base64_image))
keyboard.add_hotkey('alt+c', lambda: switch_model(model_list, current_model_name))
keyboard.add_hotkey('alt+r', lambda: get_file_content(client, current_model_name))

# 保持程序运行
print("监听按键中...按 'alt+b' 截图，按住 'menu' 键开始语音识别，松开结束语音识别, 按 'alt+c' 切换模型，按 'alt+r' 解析文件，按 'esc' 退出")
keyboard.wait('esc')