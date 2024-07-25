import os
import openai
from openai import OpenAI

# OpenAI 非流式输出
# def chat_respond(client, recognized_text, base64_image):
#     if recognized_text and base64_image:
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant that responds in Markdown."},
#                 {"role": "user", "content": [
#                     {"type": "text", "text": recognized_text},
#                     {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}", "detail": "high"}} # "detail"可选"low"或"high"，low detail模式每张图像固定消耗85 tokens，无视图像分辨率；high detail模型下，1024x1024图像消耗765 tokens，2048x4096图像消耗1105 tokens，递增
#                 ]}
#             ],
#             temperature=0.0, max_tokens=300,
#         )
#         response_content = response.choices[0].message.content
#         return response_content
#     elif recognized_text:
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant that responds in Markdown."},
#                 {"role": "user", "content": [
#                     {"type": "text", "text": recognized_text},
#                 ]}
#             ],
#             temperature=0.0, max_tokens=300,
#         )
#         response_content = response.choices[0].message.content
#         return response_content

# OpenAI 流式输出
def chat_respond(client, recognized_text, base64_image, current_model):
    response_content = ""
    if recognized_text and base64_image:
        response = client.chat.completions.create(
            model = current_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that responds in Markdown."},
                {"role": "user", "content": [
                    {"type": "text", "text": recognized_text},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}", "detail": "high"}} # "detail"可选"low"或"high"，low detail模式每张图像固定消耗85 tokens，无视图像分辨率；high detail模型下，1024x1024图像消耗765 tokens，2048x4096图像消耗1105 tokens，递增
                ]}
            ],
            temperature=0.0, max_tokens=4096,
            stream = True,
        )
        for chunk in response:
            response_content += chunk.choices[0].delta.content or ""
            print(chunk.choices[0].delta.content or "", end="", flush=True) #flush强制刷新输出
        print()
        return response_content
    elif recognized_text:
        response = client.chat.completions.create(
            model = current_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that responds in Markdown."},
                {"role": "user", "content": [
                    {"type": "text", "text": recognized_text},
                ]}
            ],
            temperature=0.0, max_tokens=4096,
            stream = True,
        )
        
        for chunk in response:
            response_content += chunk.choices[0].delta.content or ""
            print(chunk.choices[0].delta.content or "", end="", flush=True) #flush强制刷新输出
        print()
        return response_content