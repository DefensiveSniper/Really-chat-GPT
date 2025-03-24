import os
import yaml
import json
import glob

with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
    system_prompt = config['system_prompt']
    chat_bot = config['chat_bot']
    f.close()

screenshot_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=="

def get_message_json(chathistory_filename, chathistory_path):
    if not os.path.exists(chathistory_path):
        os.makedirs(chathistory_path)
    if chat_bot == "openai":
        data = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "你好！"},
            {"role": "assistant", "content": "你好！有什么可以帮助您？"},
            {"role": "user", "content": [
                {"type": "text", 
                "text": "从这张图片中你能获取哪些信息？"
                },
                {"type": "image_url",
                "image_url": {
                    "url": f"data:image/png; base64,{screenshot_base64}",
                    "detail": "high",
                    }
                }]
            },
            {"role": "assistant", "content": "好的，这是我从图片中获取的信息。"},
        ]
    else:
        data = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "你好！"},
            {"role": "assistant", "content": "你好！有什么可以帮助您？"},
        ]
        
    with open(chathistory_filename, 'w') as json_file:
        json.dump(data, json_file)
    
    files = glob.glob(os.path.join(chathistory_path, '*.json'))
    latest_file = max(files, key=os.path.getmtime)
    with open(latest_file, 'r') as json_file:
        message = json.load(json_file)
    return message

def save_message_json(chathistory_filename, message):
    with open(chathistory_filename, 'w', encoding='utf-8') as json_file:
        json.dump(message, json_file, ensure_ascii=False, indent=2)
        print(f"温馨提示：程序退出，聊天记录已保存至 {chathistory_filename}")

