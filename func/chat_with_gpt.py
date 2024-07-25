def chat_with_gpt(user_input, current_model, client):
    print(current_model + "：", end="")
    stream = client.chat.completions.create(
        model = current_model,
        messages = [{"role": "user", "content": user_input}],
        max_tokens = 4096,
        stream = True,
    )
    for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="", flush=True) #flush强制刷新输出
    print()