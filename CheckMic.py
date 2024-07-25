import sounddevice as sd

def callback(indata, frames, time, status):
    if status:
        print(status)
    # Mirror input to output
    sd.play(indata)

# Sampling frequency
fs = 44100

print("正在从麦克风录制音频...")
with sd.InputStream(callback=callback, channels=1, samplerate=fs):
    sd.sleep(10000)  # Record for 10 seconds
