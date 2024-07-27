import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import ssl
from wsgiref.handlers import format_date_time
from time import mktime
import _thread as thread
import pyaudio
import io
import threading

audio_data = io.BytesIO()
stop_playback = False

class Ws_Param:
    def __init__(self, APPID, APIKey, APISecret, Text):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text
        self.CommonArgs = {"app_id": self.APPID}
        self.BusinessArgs = {"aue": "raw", 
                             "auf": "audio/L16;rate=16000", 
                             "vcn": "x4_yezi", # 发音人：x4_yezi，更多发音人请参考：https://www.xfyun.cn/doc/tts/online_tts/API.html#tts-service
                             "tte": "utf8"},# 文本编码格式，utf8或gb2312
        self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-8')), "UTF8")}

    def create_url(self):
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        now = datetime.datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        signature_origin = f"host: ws-api.xfyun.cn\ndate: {date}\nGET /v2/tts HTTP/1.1"
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'), digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode('utf-8')
        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')
        v = {"authorization": authorization, "date": date, "host": "ws-api.xfyun.cn"}
        return url + '?' + urlencode(v)

def on_message(ws, message):
    try:
        message = json.loads(message)
        code = message["code"]
        if code != 0:
            print(f"Error: {message['message']}")
            ws.close()
        else:
            audio = base64.b64decode(message["data"]["audio"])
            audio_data.write(audio)
            if message["data"]["status"] == 2:
                ws.close()
    except Exception as e:
        print(f"Exception: {e}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    global stop_playback
    stop_playback = False
    threading.Thread(target=play_audio_xunfei, args=(audio_data.getvalue(),)).start()

def on_open(ws):
    def run(*args):
        data = json.dumps({"common": wsParam.CommonArgs,
                           "business": wsParam.BusinessArgs,
                           "data": wsParam.Data})
        ws.send(data)
    thread.start_new_thread(run, ())

def play_audio_xunfei(audio_data):
    global stop_playback
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    output=True)
    chunk_size = 1024
    for i in range(0, len(audio_data), chunk_size):
        if stop_playback:
            break
        stream.write(audio_data[i:i+chunk_size])
    stream.stop_stream()
    stream.close()
    p.terminate()

def tts_xunfei(appid, apikey, apisecret, text):
    global wsParam, audio_data
    audio_data = io.BytesIO()  # 清空音频数据
    wsParam = Ws_Param(appid, apikey, apisecret, text)
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(wsParam.create_url(),
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

def stop_audio_xunfei():
    global stop_playback
    stop_playback = True

# # 示例调用
# if __name__ == "__main__":
#     APPID = ""
#     APISecret = ""
#     APIKey = ""
#     TEXT = "这是一个测试，将文字转换为语音并直接播放。"
#     tts_xunfei(APPID, APIKey, APISecret, TEXT)