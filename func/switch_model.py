def switch_model(model_list, current_model_name):
    print(current_model_name + "：请输入模型名称，目前支持的模型有以下几种", end="\n")
    print(', '.join(model_list) + "->若没有您想要的模型，可以自行在主程序中切换", end="\n")
    new_model = input()
    if new_model in model_list:
        current_model = new_model
        current_model_name = current_model
        print(f"模型已切换到 {current_model}")
        return current_model_name
    else:
        print("无效的模型名称")
