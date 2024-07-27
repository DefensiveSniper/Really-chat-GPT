import openai
import io
import threading
import soundfile as sf
import sounddevice as sd

is_playing = False # 播放状态，用于判断是否正在播放音频，并控制音频播放
playback_thread = None

# 生成音频流
def generate_audio_stream(response_content):
    global is_playing, playback_thread
    client = openai.OpenAI()
    spoken_response = client.audio.speech.create(
        model = "tts-1",# 语音模型：tts-1 or tts-1-hd，中文建议使用tts-1
        voice = "onyx", # 声音选择：alloy、echo、fable、onyx、nova、shimmer
        response_format = "opus", # 音频格式：opus、aac、flac、pcm、mp3
        input = response_content
    )
    # 将音频流写入缓冲区，二进制流
    buffer = io.BytesIO()
    for chunk in spoken_response.iter_bytes(chunk_size=4096):
        buffer.write(chunk)
    buffer.seek(0, 0)# 将文件指针移动到文件开头

    with sf.SoundFile(buffer, 'r') as sound_file:
        data = sound_file.read(dtype='int16')
        is_playing = True
        playback_thread = threading.Thread(target=play_audio_openai, args=(data, sound_file.samplerate))
        playback_thread.start()

def play_audio_openai(data, samplerate):
    global is_playing
    sd.play(data, samplerate)
    sd.wait()#等待音频播放完成
    is_playing = False#设置播放状态为False
def stop_audio_openai():
    global is_playing
    is_playing = False
    sd.stop()
