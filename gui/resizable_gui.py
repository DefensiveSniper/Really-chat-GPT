from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtWidgets import QTextEdit, QPushButton, QWidget, QFrame, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

# 可调整高度的 QTextEdit
class ResizableTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(20)
        self.setMaximumHeight(80)
        self.document().contentsChanged.connect(self.adjust_height)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet('''
            QTextEdit {
                border-radius: 15px;
                background-color: #2E2E2E;
                border-bottom: 2px solid green;
                color: white;
                font-size: 20px;
                padding-right: 40px; /* 为按钮留出空间 */
            }
        ''')

        # 创建按钮
        self.button = QPushButton(self)
        self.button.setFixedSize(30, 30)  # 设置按钮大小
        self.button.setStyleSheet('''
            QPushButton {
                background: transparent;
                border-radius: 15px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')
        icon = QIcon("./media/delete.png")
        self.button.setIcon(icon)
        self.button.setIconSize(QSize(20, 20))  # 设置图标大小

        # 调用 adjust_height 来设置初始高度
        self.adjust_height()

    def adjust_height(self):
        # 立即调整高度
        doc_height = self.document().size().height()
        new_height = min(max(20, doc_height + 10), 80)
        self.setFixedHeight(int(new_height))
        
        # 调整按钮位置
        self.update_button_position()
        
        # 启动定时器以处理后续内容变化
        self.adjust_timer = QTimer(self)
        self.adjust_timer.setSingleShot(True)
        self.adjust_timer.timeout.connect(self.delayed_adjust)
        self.adjust_timer.start(10)  # 10ms 延迟

    def delayed_adjust(self):
        doc_height = self.document().size().height()
        new_height = min(max(20, doc_height + 10), 80)
        self.setFixedHeight(int(new_height))
        self.update_button_position()

    def update_button_position(self):
        # 更新按钮位置到右上角
        self.button.move(self.width() - self.button.width() - 5, 5)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_button_position()

# 添加阴影效果
def add_shadow_effect(widget):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(4)
    shadow.setOffset(0, 0)
    shadow.setColor(QColor(0, 0, 0, 90))
    widget.setGraphicsEffect(shadow)