import os
import time
import json
import glob

def get_message_json(chathistory_filename, chathistory_path):
    if not os.path.exists(chathistory_path):
        os.makedirs(chathistory_path)
    data = [
        {"role": "system", "content": "你是一个乐于助人的助手。"},
        {"role": "user", "content": "你好！"},
        {"role": "system", "content": "你好！有什么可以帮助您？"},
    ]
    with open(chathistory_filename, 'w') as json_file:
        json.dump(data, json_file)
    
    files = glob.glob(os.path.join(chathistory_path, '*.json'))
    latest_file = max(files, key=os.path.getmtime)
    with open(latest_file, 'r') as json_file:
        message = json.load(json_file)
    return message

def save_message_json(chathistory_filename, message):
    with open(chathistory_filename, 'w') as json_file:
        json.dump(message, json_file)
        print(f"温馨提示：程序退出，聊天记录已保存至 {chathistory_filename}")
