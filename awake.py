import azure.cognitiveservices.speech as speechsdk
import os
import time
import keyboard

recognized_text = None

def recognize_from_microphone():
    global recognized_text
    speech_config = speechsdk.SpeechConfig(subscription=os.environ['SPEECH_KEY'], region=os.environ['SPEECH_REGION'])
    speech_config.speech_recognition_language = "zh-CN"
    auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["en-US", "zh-CN"])
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, auto_detect_source_language_config=auto_detect_source_language_config, audio_config=audio_config)

    def recognized_handler(event):
        global recognized_text
        if event.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            recognized_text = event.result.text
            print(f"已识别语音: {recognized_text}")
            speech_recognizer.stop_continuous_recognition()

    speech_recognizer.recognized.connect(recognized_handler)
    speech_recognizer.start_continuous_recognition()

    while recognized_text is None:
        time.sleep(0.5)
    

while True:
    recognize_from_microphone()
    if recognized_text:
        
        if recognized_text.startswith("你滚吧"):
            print("好的，我滚了")
            break
        recognized_text = None
    
exit()