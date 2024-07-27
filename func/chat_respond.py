import json

def chat_respond(client, recognized_text, base64_image, current_model, message):
    response_content = ""
    message.append({"role": "user", "content": recognized_text})
    print(current_model + "：", end="")
    if recognized_text and base64_image:
        response = client.chat.completions.create(
            model = current_model,
            messages = message,
            temperature = 0.4, max_tokens=4096,
            stream = True,
        )
        for chunk in response:
            response_content += chunk.choices[0].delta.content or ""
            print(chunk.choices[0].delta.content or "", end="", flush=True) #flush强制刷新输出
        print()
        message.append({"role": "assistant", "content": response_content})
        return response_content, client, message
    
    if recognized_text:
        response = client.chat.completions.create(
            model = current_model,
            messages = message,
            temperature = 0.4, max_tokens=4096,
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

def save_chat_history(messages, filename="chat_history.json"):
    with open(filename, "w") as f:
        json.dump(messages, f)
        
def load_chat_history(filename="chat_history.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []