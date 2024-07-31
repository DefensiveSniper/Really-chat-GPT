from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, 
    QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QFrame, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect,
    QTextEdit, QDialog, QFormLayout, QDesktopWidget
)
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import QSize, Qt, QPoint, QTimer

from gui.resizable_gui import add_shadow_effect

class chat_Settings:
    def __init__(self, api='', bot='', tts=''):
        self.api = api
        self.bot = bot
        self.tts = tts

    def __str__(self):
        return f'API: {self.api}, Bot: {self.bot}, TTS: {self.tts}'

class SettingsDialog(QDialog):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.initUI()
        
    def initUI(self):
        # 设置无边框窗口
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 设置窗口标题和大小
        self.setWindowTitle('聊天设置')
        # 获取屏幕的尺寸
        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        # 窗口的尺寸
        self.window_width = 400
        self.window_height = 300
        # 计算窗口的中心位置
        self.center_x = (screen_width - self.window_width) // 2
        self.center_y = (screen_height - self.window_height) // 2
        self.setGeometry(self.center_x, self.center_y, self.window_width, self.window_height)
        
        # 创建标题栏
        titleBar = QFrame(self)
        titleBar.setFrameShape(QFrame.NoFrame)
        titleBar.setFixedHeight(50)
        
        titleLayout = QHBoxLayout()
        titleLabel = QLabel('聊天设置', self)
        titleLabel.setStyleSheet('font-size: 20px; color: white;')
        titleLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
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

        # 将标题栏小部件添加到标题栏布局中
        titleLayout.addWidget(titleLabel)
        titleLayout.addItem(spacer)
        titleLayout.addWidget(closeButton)
        titleBar.setLayout(titleLayout)

        self.api_input = QLineEdit(self.settings.api)
        add_shadow_effect(self.api_input)
        self.bot_input = QLineEdit(self.settings.bot)
        add_shadow_effect(self.bot_input)
        self.tts_input = QLineEdit(self.settings.tts)
        add_shadow_effect(self.tts_input)

        # 创建保存按钮
        save_button = QPushButton('保存')
        save_button.clicked.connect(self.save_settings)
        save_button.setFixedSize(100, 30)
        save_button.setStyleSheet('''
            QPushButton {
                color: white;
                background-color: #2E2E2E;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')

        # 创建主布局
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(titleBar)
        
        # 创建 API 输入行布局
        apiLayout = QHBoxLayout()
        apiLabel = QLabel('API:')
        apiLabel.setStyleSheet('color: white; font-size: 20px;')
        apiLayout.addWidget(apiLabel)
        apiLayout.addWidget(self.api_input)
        
        # 创建 Bot 输入行布局
        botLayout = QHBoxLayout()
        botLabel = QLabel('Bot:')
        botLabel.setStyleSheet('color: white; font-size: 20px;')
        botLayout.addWidget(botLabel)
        botLayout.addWidget(self.bot_input)
        
        # 创建 TTS 输入行布局
        ttsLayout = QHBoxLayout()
        ttsLabel = QLabel('TTS:')
        ttsLabel.setStyleSheet('color: white; font-size: 20px;')
        ttsLayout.addWidget(ttsLabel)
        ttsLayout.addWidget(self.tts_input)
        
        # 创建一个水平布局来居中保存按钮
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(save_button)
        buttonLayout.addStretch()
        
        # 将输入行布局添加到主布局中
        mainLayout.addLayout(apiLayout)
        mainLayout.addLayout(botLayout)
        mainLayout.addLayout(ttsLayout)
        mainLayout.addLayout(buttonLayout)  # 添加水平布局
        
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
            QLabel{
                color: white;
                font-size: 20px;
            }
            QLineEdit{
                border-radius: 10px;
                background-color: #2E2E2E;
                border-bottom: 2px solid green;
                color: white;
                font-size: 20px;
                padding: 5px;
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
        
    def save_settings(self):
        self.settings.api = self.api_input.text()
        self.settings.bot = self.bot_input.text()
        self.settings.tts = self.tts_input.text()
        self.accept()
    
    # 拖动窗口
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
            event.accept()



def show_settings_dialog(settings):
    dialog = SettingsDialog(settings)
    if dialog.exec_() == QDialog.Accepted:
        print(settings)
    return settings