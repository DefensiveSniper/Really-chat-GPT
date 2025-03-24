import sys
import os
import time
import yaml
from openai import OpenAI
from pyqtkeybind import keybinder
from func.gpt_model_list import gpt_model_list
from func.capture_screenshot import capture_screenshot
from func.recognize_from_microphone import recognize_from_microphone
from func.chat_respond import chat_respond
from func.tts_openai import generate_audio_stream, stop_audio_openai
from func.tts_xunfei import tts_xunfei, stop_audio_xunfei
from func.audio_play import play_mp3
from func.message_json import get_message_json, save_message_json
from gui.resizable_gui import *
from gui.chat_setting import *

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QFrame, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect,
    QTextEdit, QDesktopWidget
)
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import QSize, Qt, QPoint, QTimer

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
    tts_bot = config["tts_bot"]
    APPID = config['xunfei']['APPID']
    APISecret = config['xunfei']['APISecret']
    APIKey = config['xunfei']["APIKey"]
    openai_api_key = config['openai']['api_key']
    current_model = config["model"]

# 初始化
client = OpenAI(api_key = os.environ["OPENAI_API_KEY"])
screenshot_path = "./screenshots"# 截图保存路径
screenshot_base64 = ""# 截图的base64编码
chathistory_path = "./chathistory"# 聊天记录保存路径
timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
chathistory_filename = f'{chathistory_path}/{timestamp}.json'
message = get_message_json(chathistory_filename, chathistory_path)
model_list = gpt_model_list()
current_model_name = current_model
recognized_text = ""
response = ""
start_recognition, stop_recognition, recognized_text = recognize_from_microphone()



# TTS模型选择
def text_to_speech(response):
    match tts_bot:
        case "openai":
            generate_audio_stream(response)
        case "xunfei":
            tts_xunfei(APPID, APIKey, APISecret, response)

def stop_audio():
    match tts_bot:
        case "openai":
            stop_audio_openai()
        case "xunfei":
            stop_audio_xunfei()

# gpt回复
def gpt_reply(current_model_name):
    global recognized_text, client, message, screenshot_base64, response
    response, client, message = chat_respond(client, recognized_text, screenshot_base64, current_model_name, message)
    text_to_speech(response)
    screenshot_base64 = ""

# 获取截图的base64编码
def capture(screenshot_path):
    global screenshot_base64
    screenshot_base64 = capture_screenshot(screenshot_path)
    
# 开始和停止语音识别
def start_voice_recognition():
    stop_audio()# 停止播放音频，为了更好的语音识别
    play_mp3('./media/success.mp3')
    start_recognition()
def stop_voice_recognition(current_model_name):
    stop_recognition()
    global recognized_text, screenshot_base64
    recognized_text = recognize_from_microphone()[2]
    print(f"已识别语音: {recognized_text}")
    if recognized_text:
        flag = reconize_recognized_text()
        if flag:
            gpt_reply(current_model_name)

def reconize_recognized_text():
    if recognized_text.startswith("你滚吧"):
        generate_audio_stream("好的，我滚了")
        print("好的，我滚了")
        save_message_json(chathistory_filename, message)
        sys.exit()
    if recognized_text.startswith("截图"):
        capture(screenshot_path)
        return False
    return True

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.menu_key_pressed = False  # 初始化标志位
        self.chat_settings = chat_Settings()

    def initUI(self):
        # 设置无边框窗口
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 设置窗口标题和大小
        self.setWindowTitle('GTP Computer Assistant')
        # 获取屏幕的尺寸
        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        # 窗口的尺寸
        self.window_width = 400
        self.window_height = 530
        # 计算窗口的中心位置
        self.center_x = (screen_width - self.window_width) // 2
        self.center_y = (screen_height - self.window_height) // 2
        self.setGeometry(self.center_x, self.center_y, self.window_width, self.window_height)
        
        # 设置应用程序图标
        app_icon = QIcon()
        app_icon.addFile('./media/icon_16.png', QSize(16, 16))
        app_icon.addFile('./media/icon_24.png', QSize(24, 24))
        app_icon.addFile('./media/icon_32.png', QSize(32, 32))
        app_icon.addFile('./media/icon_48.png', QSize(48, 48))
        app_icon.addFile('./media/icon_256.png', QSize(256, 256))
        self.setWindowIcon(app_icon)
        QApplication.setWindowIcon(app_icon)  # 设置应用程序图标
        
        # 创建标题栏
        titleBar = QFrame(self)
        titleBar.setFrameShape(QFrame.NoFrame)
        titleBar.setFixedHeight(50)

        # 添加标题和按钮到标题栏
        titleLayout = QHBoxLayout()
        titleLabel = QLabel('GTP Computer Assistant', self)
        titleLabel.setStyleSheet('font-size: 20px; color: white;')
        titleLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        minimizeButton = QPushButton(self)
        minimizeButton.setFixedSize(30, 30)  # 设置按钮大小
        minimizeButton.setStyleSheet('''
            QPushButton {
                background: transparent;
                border-radius: 15px;
                color: white;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')
        minimizeButton.setFixedWidth(30)
        icon = QIcon("./media/minimize.png")
        minimizeButton.setIcon(icon)
        minimizeButton.setIconSize(QSize(20, 20))  # 设置图标大小
        minimizeButton.clicked.connect(self.showMinimized)

        closeButton = QPushButton(self)
        closeButton.setFixedSize(30, 30)  # 设置按钮大小
        closeButton.setStyleSheet('''
            QPushButton {
                background: transparent;
                border-radius: 15px;
                color: white;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')
        closeButton.setFixedWidth(30)
        icon = QIcon("./media/shutdown.png")
        closeButton.setIcon(icon)
        closeButton.setIconSize(QSize(20, 20))  # 设置图标大小
        closeButton.clicked.connect(self.close)

        # 添加空间占位符小部件
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        titleLayout.addWidget(titleLabel)
        titleLayout.addItem(spacer)
        titleLayout.addWidget(minimizeButton)
        titleLayout.addWidget(closeButton)

        titleBar.setLayout(titleLayout)

        # 高度占位符
        height_60 = QSpacerItem(20, 60, QSizePolicy.Expanding, QSizePolicy.Minimum)
        height_40 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        height_20 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # 创建中间的圆按钮
        circleButton = QPushButton('Button', self)
        circleButton.setFixedSize(150, 150)
        circleButton.setStyleSheet('border-radius: 75px; background-color: black; border: 3px solid green;')
        
        # 创建文本输入框
        self.textBox = ResizableTextEdit(self)
        add_shadow_effect(self.textBox)
        self.textBox.setPlaceholderText("请输入指令...")
        self.textBox.button.clicked.connect(self.clear_text)
        
        # 创建底部的四个按钮
        bottomLayout = QGridLayout()
        
        button1 = QPushButton('发送', self)
        button1.setStyleSheet("background-color: #2E2E2E; color: white;")
        button1.clicked.connect(self.send_message)
        
        button2 = QPushButton('截图', self)
        button2.setStyleSheet("background-color: #2E2E2E; color: white;")
        button2.clicked.connect(self.capture)
        
        button3 = QPushButton('聊天设置', self)
        button3.setStyleSheet("background-color: #2E2E2E; color: white;")
        button3.clicked.connect(self.chat_setting)
        
        button4 = QPushButton('模型设置', self)
        button4.setStyleSheet("background-color: #2E2E2E; color: white;")
        button4.clicked.connect(self.model_setting)

        bottomLayout.addWidget(button1, 0, 0)
        bottomLayout.addWidget(button2, 0, 1)
        bottomLayout.addWidget(button3, 1, 0)
        bottomLayout.addWidget(button4, 1, 1)

        # 创建主布局
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(titleBar)
        mainLayout.addItem(height_60)
        mainLayout.addWidget(circleButton, 0, Qt.AlignCenter)
        mainLayout.addItem(height_20)
        mainLayout.addWidget(self.textBox)
        mainLayout.addStretch(1)
        mainLayout.addLayout(bottomLayout)

        # 设置窗口内容小部件并应用样式表
        contentWidget = QWidget(self)
        contentWidget.setLayout(mainLayout)
        contentWidget.setStyleSheet('''
            QWidget#contentWidget {
                background-color: #2E2E2E;
                border-radius: 20px;
            }
            QFrame#titleBar {
                background-color: #2E2E2E;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
            }
        ''')
        contentWidget.setObjectName('contentWidget')
        titleBar.setObjectName('titleBar')

        layout = QVBoxLayout(self)
        layout.addWidget(contentWidget)
        self.setLayout(layout)
        
        # 使标题栏可拖动窗口
        titleBar.mousePressEvent = self.mousePressEvent
        titleBar.mouseMoveEvent = self.mouseMoveEvent


#### 定义功能 ####
    
    # 拖动窗口
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
            event.accept()

    # 清空文本框
    def clear_text(self):
        self.textBox.clear()

    # "截图" 按钮
    def capture(self):
        global screenshot_base64
        screenshot_base64 = capture_screenshot(screenshot_path)

    # "发送" 按钮
    def send_message(self):
        global recognized_text, screenshot_base64
        try :
            recognized_text = self.textBox.toPlainText()
            print(f"已发送指令: {recognized_text}")
            if recognized_text:
                flag = reconize_recognized_text()
                if flag:
                    gpt_reply(current_model_name)
            self.textBox.clear()
            # 显示回复
            self.textBox.setText(response)
        except Exception as e:
            print(e)

    # "聊天设置" 按钮
    def chat_setting(self):
        try:
            self.chat_settings = show_settings_dialog(self.chat_settings)
        except Exception as e:
            print(e)
    
    # "模型设置" 按钮
    def model_setting(self):
        pass
    
    # 语音识别
    def on_menu_key_typed(self):
        try :
            start_voice_recognition()
        except Exception as e:
            print(e)
    def on_menu_key_typed_again(self):
        try :
            stop_voice_recognition(current_model_name)
            self.textBox.clear()
            # 显示回复
            self.textBox.setText(response)
        except Exception as e:
            print(e)
        
    # 键盘监听
    def key_type_event(self, event):
        if event.key() == Qt.Key_Menu and not self.menu_key_pressed:  # 语音识别键对应的键码
            self.menu_key_pressed = True
            self.on_menu_key_typed()
        elif event.key() == Qt.Key_Menu and self.menu_key_pressed:
            self.menu_key_pressed = False
            self.on_menu_key_typed_again()
        elif event.key() == Qt.Key_C and event.modifiers() == Qt.AltModifier:
            self.capture()
        super().keyPressEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
