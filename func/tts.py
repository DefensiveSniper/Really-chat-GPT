from func.tts_openai import generate_audio_stream, stop_audio_openai
from func.tts_xunfei import tts_xunfei, stop_audio_xunfei

def text_to_speech(response, tts_bot):
    match tts_bot:
        case "openai":
            generate_audio_stream(response)
        case "xunfei":
            tts_xunfei(response)

def stop_audio(tts_bot):
    match tts_bot:
        case "openai":
            stop_audio_openai()
        case "xunfei":
            stop_audio_xunfei()