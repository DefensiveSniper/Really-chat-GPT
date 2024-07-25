import os
import keyboard
from openai import OpenAI
from func.capture_screenshot import capture_screenshot
from func.recognize_from_microphone import recognize_from_microphone
from func.chat_respond import chat_respond
from func.generate_audio_stream import generate_audio_stream
from func.generate_audio_stream import stop_audio
from func.generate_audio_stream import play_audio
from func.audio_play import play_mp3
from func.switch_model import switch_model
from func.read_file import file_parse
from func.generate_image import generate_image

# 初始化
client = OpenAI(api_key = os.environ["OPENAI_API_KEY"])
screenshot_path = "./screenshots"# 截图保存路径
current_model = "gpt-4o-mini"
current_model_name = current_model
model_list = ["gpt-4o-mini","gpt-4o"]# 模型列表，需求更多模型请参考 https://platform.openai.com/docs/models
recognized_text = ""
base64_image = "" # 截图的base64编码
new_screenshot = False
create_flag = False
start_recognition, stop_recognition, recognized_text = recognize_from_microphone()

def gpt_reply(current_model_name, base64_image):
    global recognized_text, create_flag, client
    if create_flag: # 图片生成
        generate_image(recognized_text, client, current_model_name)
        create_flag = False
        return
    response, client = chat_respond(client, recognized_text, base64_image, current_model_name)
    generate_audio_stream(response)
    recognized_text = ""
    base64_image = ""

def get_base64_image(screenshot_path):
    global base64_image
    base64_image = capture_screenshot(screenshot_path)
    
def get_file_content(current_model_name):
    global recognized_text, base64_image
    recognized_text, base64_image = file_parse(current_model_name)

def start_voice_recognition(_):
    stop_audio()
    play_mp3('./audio/success.mp3')
    start_recognition()

def stop_voice_recognition(current_model_name, base64_image):
    stop_recognition()
    global recognized_text, voice_input_received
    exited_text = recognized_text
    recognized_text = recognize_from_microphone()[2]
    if exited_text:
        recognized_text += exited_text
    if recognized_text:
        gpt_reply(current_model_name, base64_image)

def create_image(current_model_name):
    global recognized_text, create_flag
    create_flag = True
    print(current_model_name + "：请描述你要生成的图片")

# 绑定按键组合
keyboard.on_press_key('menu', start_voice_recognition)
keyboard.on_release_key('menu', lambda _: stop_voice_recognition(current_model_name, base64_image))
keyboard.add_hotkey('alt+b', lambda: get_base64_image(screenshot_path))
keyboard.add_hotkey('alt+c', lambda: switch_model(model_list, current_model_name))
keyboard.add_hotkey('alt+r', lambda: get_file_content(current_model_name))
keyboard.add_hotkey('alt+p', lambda: create_image(current_model_name))

# 保持程序运行
print(" 'alt+b' 截图，按住 'menu' 键开始语音识别,  'alt+c' 切换模型， 'alt+r' 解析文件， 'esc' 退出")
keyboard.wait('esc')
print("程序退出")
