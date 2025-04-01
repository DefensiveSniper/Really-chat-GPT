import azure.cognitiveservices.speech as speechsdk
import os

recognized_text = ""
recognizer_active = False
# Azure语音识别
def recognize_from_microphone():
    global recognized_text, recognizer_active, continue_screenshot
    speech_config = speechsdk.SpeechConfig(subscription=os.environ['SPEECH_KEY'], region=os.environ['SPEECH_REGION'])
    speech_config.speech_recognition_language = "zh-CN"
    auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["en-US", "zh-CN"])
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, auto_detect_source_language_config=auto_detect_source_language_config, audio_config=audio_config)

    def recognized_handler(event):
        global recognized_text, recognizer_active, continue_screenshot
        if event.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            recognized_text += event.result.text
            continue_screenshot = False

    def start_recognition():
        global recognizer_active, recognized_text
        recognized_text = ""
        if not recognizer_active:
            print("\n开始语音识别...")
            speech_recognizer.start_continuous_recognition()
            recognizer_active = True

    def stop_recognition():
        global recognizer_active
        if recognizer_active:
            print("停止语音识别...")
            speech_recognizer.stop_continuous_recognition()
            recognizer_active = False

    speech_recognizer.recognized.connect(recognized_handler)# 连接事件处理程序
    return start_recognition, stop_recognition, recognized_text
