import json
import yaml
import os
from openai import OpenAI

# 加载配置文件
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)
    chat_bot = config['chat_bot']
    file.close()
    
if chat_bot == 'openai':
    client = OpenAI(api_key = os.environ["OPENAI_API_KEY"] if "OPENAI_API_KEY" in os.environ else config['openai']['api_key'])
    Temperature = config['openai']['temperature']
    Max_tokens = config['openai']['max_tokens']
elif chat_bot == 'deepseek':
    client = OpenAI(api_key = config['deepseek']['api_key'], base_url="https://api.deepseek.com/v1")
    Temperature = config['deepseek']['temperature']
    Max_tokens = config['deepseek']['max_tokens']

def chat_respond(recognized_text, screenshot_base64, current_model, message):
    response_content = ""
    print(current_model + "：", end="")
    if recognized_text and screenshot_base64:
        if chat_bot != 'openai':
            return "抱歉，我无法识别这张图片。", message
        
        message.append(
            {"role": "user", "content": [
                {"type": "text", "text": recognized_text},
                {"type": "image_url", 
                    "image_url": {
                    "url": f"data:image/png;base64,{screenshot_base64}",
                    "detail": "high"}
                }
            ]
        })
    elif recognized_text:
        message.append({"role": "user", "content": recognized_text})
            
    try:
        response = client.chat.completions.create(
            model = current_model,
            messages = message,
            temperature = Temperature, max_tokens=Max_tokens,
            stream = True,
        )
        for chunk in response:
            response_content += chunk.choices[0].delta.content or ""
            print(chunk.choices[0].delta.content or "", end="", flush=True) #flush强制刷新输出
        print()
        message.append({"role": "assistant", "content": response_content})
        return response_content, message
    except Exception as e:
        print(e)
        return "抱歉，我无法识别这张图片。", message

def save_chat_history(messages, filename="chat_history.json"):
    with open(filename, "w") as f:
        json.dump(messages, f)
        
def load_chat_history(filename="chat_history.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []