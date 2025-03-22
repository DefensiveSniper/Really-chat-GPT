import json

def chat_respond(client, recognized_text, screenshot_base64, current_model, message, Temperature, Max_tokens):
    response_content = ""
    print(current_model + "：", end="")
    if recognized_text and screenshot_base64:
        try:
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
            return response_content, client, message
        except Exception as e:
            print(e)
            return "抱歉，我无法识别这张图片。", client, message
    
    if recognized_text:
        try :
            message.append({"role": "user", "content": recognized_text})
            response = client.chat.completions.create(
                model = current_model,
                messages = message,
                temperature = Temperature, max_tokens=Max_tokens,
                stream = True,
            )
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content is not None:
                    response_content += content
                    print(content, end="", flush=True) #flush强制刷新输出
            print()
            message.append({"role": "assistant", "content": response_content})
            return response_content, client, message
        except Exception as e:
            print(e)
            return "抱歉，我无法识别您的语音。", client, message

def save_chat_history(messages, filename="chat_history.json"):
    with open(filename, "w") as f:
        json.dump(messages, f)
        
def load_chat_history(filename="chat_history.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []