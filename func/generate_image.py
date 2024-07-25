from openai import OpenAI
from func.chat_respond import chat_respond
from func.audio_play import play_mp3
import base64
import requests
import os

def generate_image(recognized_text, client, current_model_name):
    
    current_model_name = "dall-e-3"# dall-e-3, dall-e-2

    # 生成图片
    response = client.images.generate(
        model = current_model_name,
        prompt = recognized_text,
        size = "1024x1024", #1024x1024, 1024x1792, 1792x1024
        quality = "standard",
        n=1, #生成图片数量
    )

    image_url = response.data[0].url
    
    # 检查请求是否成功
    if requests.get(image_url).status_code == 200:
        # 获取图像的字节内容
        image = requests.get(image_url).content
        # 将图像内容进行 base64 编码
        base64_image = base64.b64encode(image).decode("utf-8")
    else:
        print(f"请求失败，状态码: {response.status_code}")
    
    
    # 使用GPT模型总结图片内容，生成图片名称
    summary_client = OpenAI(api_key = os.environ["OPENAI_API_KEY"])# 新建一个OpenAI对象
    user_input = "为这个图片起一个简练的名字,不要有任何的符号或者特殊字符。"
    summary = chat_respond(summary_client, user_input, base64_image, "gpt-4o-mini")
    filename = summary + ".png"

    # 确保 image 文件夹存在
    folder_path = 'image'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 保存图片到 image 文件夹
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'wb') as f:
        f.write(image)

    print(f"图片已保存为 {file_path}")
    play_mp3('./audio/success.mp3')
    
    return client
