from openai import OpenAI
import requests
import os

def generate_image(prompt, client):
    client = OpenAI()
    current_model_name = "dall-e-3" #dall-e-3, dall-e-2

    # 生成图片
    response = client.images.generate(
        model=current_model_name,
        prompt=prompt,
        size="1024x1024", #1024x1024, 1024x1792, 1792x1024
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    # 下载图片
    image = requests.get(image_url)

    # 使用GPT模型生成总结
    user_input = prompt + ", 请简要总结以上内容当作图片名称, 并将总结内容中的空格换为下划线。"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_input}],
        max_tokens=4096,
    )
    summary = response.choices[0].message.content

    # 提炼总结内容为图片文件名称
    filename = summary + ".jpg"

    # 确保 image 文件夹存在
    folder_path = 'image'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 保存图片到 image 文件夹
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'wb') as f:
        f.write(image.content)

    print(f"图片已保存为 {file_path}")
