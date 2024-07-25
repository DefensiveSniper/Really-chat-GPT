"""
This module checks the microphone functionality using the sounddevice library.
该模块使用 sounddevice 库检查麦克风功能。
"""
import sounddevice as sd

def callback(indata, status):
    if status:
        print(status)
    sd.play(indata)
    pass
# 采样频率
fs_ = 44100

print("正在从麦克风录制音频...")
with sd.InputStream(callback=callback, channels=1, samplerate=fs_):
    sd.sleep(10000)  # Record for 10 seconds
