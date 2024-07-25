import openai
import io
import soundfile as sf
import sounddevice as sd


# OpenAI文本转语音
def generate_audio_stream(response_content):
    client = openai.OpenAI()
    spoken_response = client.audio.speech.create(
    model="tts-1",
    voice="shimmer", # 声音选择
    response_format = "opus", # 音频格式
    input = response_content
    )

    buffer = io.BytesIO()
    for chunk in spoken_response.iter_bytes(chunk_size=4096):
        buffer.write(chunk)

    buffer.seek(0)

    with sf.SoundFile(buffer, 'r') as sound_file:
        data = sound_file.read(dtype='int16')
        sd.play(data, sound_file.samplerate)
        sd.wait()