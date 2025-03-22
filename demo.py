import os
import threading
import keyboard
import time
from openai import OpenAI
from func.gpt_model_list import gpt_model_list
from func.capture_screenshot import capture_screenshot
from func.auto_capture_screenshots import auto_capture_screenshots
from func.recognize_from_microphone import recognize_from_microphone
from func.chat_respond import chat_respond
from func.tts_openai import generate_audio_stream, stop_audio_openai
from func.audio_play import play_mp3
from func.switch_model import switch_model
from func.read_file import file_parse
from func.generate_image import generate_image
from func.message_json import get_message_json, save_message_json

# 初始化
client = OpenAI(api_key = os.environ["OPENAI_API_KEY"])
Temperature = 0.8
Max_tokens = 4096
current_model = "gpt-4o-mini"
prompt = "你是一个私人的AI语音助手，请根据用户给的信息，回答用户的问题。回答要简洁明了，不要重复用户的问题，使用txt格式回答，不得出现其它格式，不得出现其它字符。"
continue_screenshot = False # 自动截图开关，默认关闭
screenshot_interval = 5 # 自动截图间隔
#############################################################################################
#############################################################################################
screenshot_path = "./screenshots"# 截图保存路径
chathistory_path = "./chathistory"# 聊天记录保存路径
timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
chathistory_filename = f'{chathistory_path}/{timestamp}.json'
message = get_message_json(chathistory_filename, chathistory_path)
message.append({"role": "system", "content": prompt})
model_list = gpt_model_list()
current_model_name = current_model
recognized_text = ""
base64_image = "" # 截图的base64编码
new_screenshot = False
create_flag = False
screenshot_thread = None
shared_data = {'base64_image': None}
image_lock = threading.Lock()
stop_auto_capture_event = threading.Event()
start_recognition, stop_recognition, recognized_text = recognize_from_microphone()

# gpt回复
def gpt_reply(current_model_name, base64_image):
    global recognized_text, create_flag, client, message
    if create_flag: # 图片生成
        generate_image(recognized_text, client, current_model_name)
        create_flag = False
        return
    response, client, message = chat_respond(client, recognized_text, base64_image, current_model_name, message, Temperature, Max_tokens)
    generate_audio_stream(response)
    recognized_text = ""
    base64_image = ""

# 获取截图的base64编码（手动）
def capture(screenshot_path):
    global shared_data, base64_image
    encoded_image = capture_screenshot(screenshot_path)
    if encoded_image:
        with image_lock:
            shared_data['base64_image'] = encoded_image
            base64_image = encoded_image  # 同步全局变量
            print("手动截图 base64_image 已更新")
    
# 语音识别
def start_voice_recognition(_):
    stop_audio_openai()# 停止播放音频，为了更好的语音识别
    play_mp3('./media/success.mp3')
    start_recognition()
def stop_voice_recognition(current_model_name, base64_image):
    stop_recognition()
    global recognized_text, create_flag
    exited_text = recognized_text
    recognized_text = recognize_from_microphone()[2]
    if exited_text:
        recognized_text += exited_text
    if recognized_text:
        print(f"已识别语音: {recognized_text}")
        gpt_reply(current_model_name, base64_image)
    create_flag = False

# 解析文件返回文本和base64编码（如果是图片）
def get_file_content(current_model_name):
    global recognized_text, base64_image
    recognized_text, base64_image = file_parse(current_model_name)

def create_image():
    global recognized_text, create_flag, current_model_name
    create_flag = True
    print(current_model_name + "：请描述你要生成的图片")
    print(current_model_name + "：等待语音输入...")

def switch_model_():
    global current_model_name
    current_model_name = switch_model(model_list, current_model_name)

# 切换自动截图状态
def switch_continue_screenshot():
    global screenshot_thread, continue_screenshot, stop_auto_capture_event

    continue_screenshot = not continue_screenshot
    if continue_screenshot:
        stop_auto_capture_event.clear()
        screenshot_thread = threading.Thread(
            target=auto_capture_screenshots,
            args=(screenshot_path, screenshot_interval, stop_auto_capture_event, shared_data, image_lock),
            daemon=True
        )
        screenshot_thread.start()
        keyboard.clear_hotkey('alt+b')
        print("自动截图已开启")
    else:
        stop_auto_capture_event.set()
        keyboard.add_hotkey('alt+b', lambda: capture(screenshot_path))
        print("自动截图已关闭")
        print("请按 alt+b 手动截图")

# 同步函数（持续自动同步base64_image）
def sync_base64_image():
    global base64_image
    while True:
        with image_lock:
            base64_image = shared_data['base64_image']
        time.sleep(0.1)  # 每隔0.1秒同步一次，频率可自行调整

def main():
    threading.Thread(target=sync_base64_image, daemon=True).start()
    # 绑定按键组合
    keyboard.on_press_key('`', start_voice_recognition)
    keyboard.on_release_key('`', lambda _: stop_voice_recognition(current_model_name, base64_image))
    keyboard.add_hotkey('alt+a', switch_continue_screenshot)
    keyboard.add_hotkey('alt+b', lambda: capture(screenshot_path))
    keyboard.add_hotkey('alt+c', lambda: switch_model_())
    keyboard.add_hotkey('alt+r', lambda: get_file_content(current_model_name))
    keyboard.add_hotkey('alt+p', lambda: create_image())
    # 提示信息
    ps = "温馨提示："
    print(ps + "按下 'alt+a' 可切换自动截图的启动与停止")
    print(ps + "'alt+b' 截图，'alt+c' 切换模型，'alt+r' 解析文件，'alt+p' 生成图片")
    print(ps + "按住 '`' 键开始语音识别, 'esc' 退出")
    print(ps + "当前模型：" + current_model_name)

    # 等待退出
    keyboard.wait('esc')
    save_message_json(chathistory_filename, message)
    
    
if __name__ == "__main__":
    main()
