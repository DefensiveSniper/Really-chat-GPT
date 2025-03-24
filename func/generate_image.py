from openai import OpenAI
from func.chat_respond import chat_respond
from func.audio_play import play_mp3
import base64
import requests
import os
import yaml

# 加载配置文件
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

client = OpenAI(api_key = os.environ["OPENAI_API_KEY"] if "OPENAI_API_KEY" in os.environ else config['openai']['api_key'])

def generate_image(recognized_text):
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
    try:
        image = requests.get(image_url).content
        base64_image = base64.b64encode(image).decode("utf-8")
    except requests.exceptions.RequestException as e:
        print(f"请求失败，错误信息: {e}")
        return None
    
    # 使用GPT模型总结图片内容，生成图片名称
    user_input = recognized_text + "\n" +"对以上用于给的信息进行提炼，作为图片的命名，要求简洁明了，不超过10个汉字" + "\n" + "example: {'user':'生成一张白人持枪抢劫银行的图片';'assistant':'抢劫银行的白人'}"
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "developer", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    summary = completion.choices[0].message.content
    filename = "".join(summary) + ".png"

    # 确保 image 文件夹存在
    folder_path = 'image'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 保存图片到 image 文件夹
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'wb') as f:
        f.write(image)

    print(f"图片已保存为 {file_path}")
    play_mp3('./media/success.mp3')