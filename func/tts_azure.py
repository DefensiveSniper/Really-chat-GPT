import threading
import yaml
import os
import queue
import azure.cognitiveservices.speech as speechsdk
from openai import OpenAI

with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
    chat_bot = config['chat_bot']
    Subscription = os.environ.get('SPEECH_KEY') if "SPEECH_KEY" in os.environ else config['azure']['SPEECH_KEY']
    Region = os.environ.get('SPEECH_REGION') if "SPEECH_REGION" in os.environ else config['azure']['SPEECH_REGION']
    f.close()

# setup client
if chat_bot == 'openai':
    client = OpenAI(api_key = os.environ["OPENAI_API_KEY"] if "OPENAI_API_KEY" in os.environ else config['openai']['api_key'])
    Temperature = config['openai']['temperature']
    Max_tokens = config['openai']['max_tokens']
elif chat_bot == 'deepseek':
    client = OpenAI(api_key = config['deepseek']['api_key'], base_url="https://api.deepseek.com/v1")
    Temperature = config['deepseek']['temperature']
    Max_tokens = config['deepseek']['max_tokens']

tts_running = False
tts_lock = threading.Lock()
speech_synthesizer = None

def setup_speech_synthesizer_stream():
    speech_config = speechsdk.SpeechConfig(
        endpoint=f"wss://{Region}.tts.speech.microsoft.com/cognitiveservices/websocket/v2",
        subscription=Subscription
    )
    speech_config.speech_synthesis_voice_name = 'zh-CN-XiaoxiaoMultilingualNeural'
    speech_config.speech_synthesis_rate = "2"
    speech_config.set_property(speechsdk.PropertyId.SpeechSynthesis_FrameTimeoutInterval, "100000000")
    speech_config.set_property(speechsdk.PropertyId.SpeechSynthesis_RtfTimeoutThreshold, "10")
    
    # 这里明确指定默认扬声器输出
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )
    return synthesizer

def tts_stream_worker(text_queue):
    global tts_running, speech_synthesizer
    speech_synthesizer = setup_speech_synthesizer_stream()

    tts_request = speechsdk.SpeechSynthesisRequest(
        input_type=speechsdk.SpeechSynthesisRequestInputType.TextStream
    )

    tts_task = speech_synthesizer.speak_async(tts_request)
    tts_running = True

    while tts_running:
        text_chunk = text_queue.get()
        if text_chunk is None:  # 流结束标志
            break
        tts_request.input_stream.write(text_chunk)

    tts_request.input_stream.close()
    result = tts_task.get()

    if result.reason == speechsdk.ResultReason.Canceled:
        print("[TTS Canceled]")
    # else:
    #     print("[TTS Finished]")

    tts_running = False

def interrupt_tts():
    global speech_synthesizer, tts_running
    with tts_lock:
        if tts_running and speech_synthesizer:
            speech_synthesizer.stop_speaking_async()
            tts_running = False
            print("[TTS Interrupted]")

def chat_respond_with_audio(recognized_text, screenshot_base64, current_model, message):
    global tts_running
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
    except Exception as e:
        print(e)
        return "抱歉，我无法回答这个问题。", message

    # 创建文本队列用于向TTS流式输入文本
    text_queue = queue.Queue()
    # 启动TTS线程，实时消费文本队列中的内容
    tts_thread = threading.Thread(target=tts_stream_worker, args=(text_queue,))
    tts_thread.start()

    for chunk in response:
        if len(chunk.choices) > 0:
            chunk_text = chunk.choices[0].delta.content
            if chunk_text:
                print(chunk_text, end="", flush=True)
                response_content += chunk_text
                text_queue.put(chunk_text)  # 实时推送到TTS队列

    print("[GPT END]", end="\n")
    text_queue.put(None)  # GPT流结束，通知TTS线程终止

    message.append({"role": "assistant", "content": response_content})
    return response_content, message

import keyboard

def listen_keyboard():
    while True:
        keyboard.wait('`')  # 等待"`"按键按下
        interrupt_tts()

# 启动键盘监听线程（程序启动时调用一次即可）
keyboard_thread = threading.Thread(target=listen_keyboard, daemon=True)
keyboard_thread.start()
