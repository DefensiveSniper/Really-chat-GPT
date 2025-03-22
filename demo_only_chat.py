<<<<<<< HEAD
import os
import sys
import keyboard
import time
from openai import OpenAI
from func.gpt_model_list import gpt_model_list
from func.capture_screenshot import capture_screenshot
from func.recognize_from_microphone import recognize_from_microphone
from func.chat_respond import chat_respond
from func.tts_openai import generate_audio_stream, stop_audio_openai
from func.tts_xunfei import tts_xunfei, stop_audio_xunfei
from func.audio_play import play_mp3
from func.message_json import get_message_json, save_message_json


# 讯飞开放平台的APPID、APISecret和APIKey
APPID = ""
APISecret = ""
APIKey = ""

# 初始化
client = OpenAI(api_key = os.environ["OPENAI_API_KEY"])
screenshot_path = "./screenshots"# 截图保存路径
chathistory_path = "./chathistory"# 聊天记录保存路径
timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
chathistory_filename = f'{chathistory_path}/{timestamp}.json'
message = get_message_json(chathistory_filename, chathistory_path)
model_list = gpt_model_list()
current_model = "gpt-4o-mini"
current_model_name = current_model
recognized_text = ""
base64_image = "" # 截图的base64编码
start_recognition, stop_recognition, recognized_text = recognize_from_microphone()

# TTS模型选择
tts_bot = "openai" # 选择TTS模型：openai or xunfei

# 提示信息
# ps = "温馨提示："
# print(ps + "'alt+b' 截图")
# print(ps + "按住 'menu' 键开始语音识别, 'esc' 退出")
# print(ps + "当前模型：" + current_model_name)

# TTS模型选择
def text_to_speech(response):
    match tts_bot:
        case "openai":
            generate_audio_stream(response)
        case "xunfei":
            tts_xunfei(APPID, APIKey, APISecret, response)

def stop_audio():
    match tts_bot:
        case "openai":
            stop_audio_openai()
        case "xunfei":
            stop_audio_xunfei()

# gpt回复
def gpt_reply(current_model_name):
    global recognized_text, client, message, ps, base64_image
    response, client, message = chat_respond(client, recognized_text, base64_image, current_model_name, message)
    text_to_speech(response)
    base64_image = ""

# 获取截图的base64编码
def capture(screenshot_path):
    global base64_image
    base64_image = capture_screenshot(screenshot_path)
    
# 开始和停止语音识别
def start_voice_recognition(_):
    stop_audio()# 停止播放音频，为了更好的语音识别
    play_mp3('./media/success.mp3')
    start_recognition()
def stop_voice_recognition(current_model_name):
    stop_recognition()
    global recognized_text, base64_image
    recognized_text = recognize_from_microphone()[2]
    print(f"已识别语音: {recognized_text}")
    if recognized_text:
        flag = reconize_recognized_text()
        if flag:
            gpt_reply(current_model_name)

def reconize_recognized_text():
    if recognized_text.startswith("你滚吧"):
        generate_audio_stream("好的，我滚了")
        print("好的，我滚了")
        save_message_json(chathistory_filename, message)
        sys.exit()
    if recognized_text.startswith("截图"):
        capture(screenshot_path)
        return False
    return True

def main():
    # 绑定按键组合
    keyboard.on_press_key('menu', start_voice_recognition)
    keyboard.on_release_key('menu', lambda _: stop_voice_recognition(current_model_name))
    keyboard.add_hotkey('alt+b', lambda: capture(screenshot_path))
    
    # 等待退出
    keyboard.wait('esc')
    save_message_json(chathistory_filename, message)

if __name__ == "__main__":
    main()
=======
import os
import sys
import keyboard
import time
from openai import OpenAI
from func.gpt_model_list import gpt_model_list
from func.capture_screenshot import capture_screenshot
from func.recognize_from_microphone import recognize_from_microphone
from func.chat_respond import chat_respond
from func.tts_openai import generate_audio_stream, stop_audio_openai
from func.tts_xunfei import tts_xunfei, stop_audio_xunfei
from func.audio_play import play_mp3
from func.message_json import get_message_json, save_message_json


# 讯飞开放平台的APPID、APISecret和APIKey
APPID = ""
APISecret = ""
APIKey = ""

# 初始化
client = OpenAI(api_key = os.environ["OPENAI_API_KEY"])
Temperature = 0.8
Max_tokens = 4096
screenshot_path = "./screenshots"# 截图保存路径
chathistory_path = "./chathistory"# 聊天记录保存路径
timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
chathistory_filename = f'{chathistory_path}/{timestamp}.json'
message = get_message_json(chathistory_filename, chathistory_path)
model_list = gpt_model_list()
current_model = "gpt-4o-mini"
current_model_name = current_model
recognized_text = ""
base64_image = "" # 截图的base64编码
start_recognition, stop_recognition, recognized_text = recognize_from_microphone()

# TTS模型选择
tts_bot = "openai" # 选择TTS模型：openai or xunfei

# 提示信息
# ps = "温馨提示："
# print(ps + "'alt+b' 截图")
# print(ps + "按住 'menu' 键开始语音识别, 'esc' 退出")
# print(ps + "当前模型：" + current_model_name)

# TTS模型选择
def text_to_speech(response):
    match tts_bot:
        case "openai":
            generate_audio_stream(response)
        case "xunfei":
            tts_xunfei(APPID, APIKey, APISecret, response)

def stop_audio():
    match tts_bot:
        case "openai":
            stop_audio_openai()
        case "xunfei":
            stop_audio_xunfei()

# gpt回复
def gpt_reply(current_model_name):
    global recognized_text, client, message, ps, base64_image
    response, client, message = chat_respond(client, recognized_text, base64_image, current_model_name, message, Temperature, Max_tokens)
    text_to_speech(response)
    base64_image = ""

# 获取截图的base64编码
def capture(screenshot_path):
    global base64_image
    base64_image = capture_screenshot(screenshot_path)
    
# 开始和停止语音识别
def start_voice_recognition(_):
    stop_audio()# 停止播放音频，为了更好的语音识别
    play_mp3('./media/success.mp3')
    start_recognition()
def stop_voice_recognition(current_model_name):
    stop_recognition()
    global recognized_text, base64_image
    recognized_text = recognize_from_microphone()[2]
    print(f"已识别语音: {recognized_text}")
    if recognized_text:
        flag = reconize_recognized_text()
        if flag:
            gpt_reply(current_model_name)

def reconize_recognized_text():
    if recognized_text.startswith("你滚吧"):
        generate_audio_stream("好的，我滚了")
        print("好的，我滚了")
        save_message_json(chathistory_filename, message)
        sys.exit()
    if recognized_text.startswith("截图"):
        capture(screenshot_path)
        return False
    return True

def main():
    # 绑定按键组合
    keyboard.on_press_key('menu', start_voice_recognition)
    keyboard.on_release_key('menu', lambda _: stop_voice_recognition(current_model_name))
    keyboard.add_hotkey('alt+b', lambda: capture(screenshot_path))
    
    # 等待退出
    keyboard.wait('esc')
    save_message_json(chathistory_filename, message)

if __name__ == "__main__":
    main()
>>>>>>> 01232ab (增添了实时屏幕识别的功能)
