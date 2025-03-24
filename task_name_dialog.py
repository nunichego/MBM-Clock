from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QFrame, QLineEdit, QApplication)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor

class TaskNameDialog(QDialog):

    taskNameSubmitted = pyqtSignal(str)
    
    def __init__(self, parent=None, style_manager=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.style_manager = style_manager
        
        self.dragPos = None

        self.setup_fonts()
        
        self.apply_modern_stylesheet()
        
        self.setup_ui()
        
        desktop = QApplication.desktop()
        screen_rect = desktop.availableGeometry(self)
        self.move(screen_rect.center() - self.rect().center())
    
    def setup_fonts(self):
        self.regular_font = QFont("Calibri", 10)
        self.bold_font = QFont("Calibri", 11)
        self.bold_font.setBold(True)
        self.title_font = QFont("Calibri", 14)
        self.title_font.setBold(True)
        
    def apply_modern_stylesheet(self):
        self.setStyleSheet("""
            QDialog {
                background-color: transparent;
            }
            QFrame#mainContainer {
                background-color: rgb(32, 32, 32);
                border-radius: 15px;
                border: none;
            }
            QLabel {
                color: rgb(240, 240, 240);
                background-color: transparent;
                border: none;
            }
            QLineEdit {
                background-color: rgb(45, 45, 45);
                color: white;
                border-radius: 8px;
                padding: 6px 10px;
                border: none;
                selection-background-color: rgb(70, 130, 180);
            }
            QLineEdit:focus {
                background-color: rgb(50, 50, 50);
            }
            QPushButton {
                background-color: rgb(45, 45, 45);
                color: white;
                border-radius: 8px;
                padding: 6px 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgb(55, 55, 55);
            }
            QPushButton:pressed {
                background-color: rgb(40, 40, 40);
            }
            QPushButton#startButton {
                background-color: rgb(40, 120, 40);
                color: white;
            }
            QPushButton#startButton:hover {
                background-color: rgb(45, 135, 45);
            }
            QPushButton#startButton:pressed {
                background-color: rgb(35, 105, 35);
            }
        """)
    
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        container = QFrame(self)
        container.setObjectName("mainContainer")
        container.setGraphicsEffect(self.create_shadow_effect())
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(24, 24, 24, 24)
        container_layout.setSpacing(16)
        
        title_label = QLabel("New Task")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(self.title_font)
        container_layout.addWidget(title_label)

        task_name_label = QLabel("Enter Task Name:")
        task_name_label.setFont(self.regular_font)
        container_layout.addWidget(task_name_label)
        
        self.task_name_input = QLineEdit()
        self.task_name_input.setPlaceholderText("e.g., Study Session, Work Project, etc.")
        self.task_name_input.setFont(self.regular_font)
        self.task_name_input.returnPressed.connect(self.submit_task_name)
        container_layout.addWidget(self.task_name_input)

        container_layout.addSpacing(8)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)

        self.start_button = QPushButton("Start Task")
        self.start_button.setObjectName("startButton")
        self.start_button.setFont(self.bold_font)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFont(self.regular_font)
        
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.start_button)
        
        container_layout.addLayout(buttons_layout)
        main_layout.addWidget(container)

        self.start_button.clicked.connect(self.submit_task_name)
        self.cancel_button.clicked.connect(self.reject)

        self.task_name_input.setFocus()

        self.setFixedSize(450, 240)
    
    def create_shadow_effect(self):
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 0)
        return shadow
    
    def submit_task_name(self):
        task_name = self.task_name_input.text().strip()
        if task_name:
            self.taskNameSubmitted.emit(task_name)
            self.accept()
        else:
            self.task_name_input.setStyleSheet("""
                background-color: rgb(45, 45, 45);
                color: white;
                border-radius: 8px;
                padding: 6px 10px;
                border: 1px solid rgb(200, 70, 70);
            """)
            self.task_name_input.setPlaceholderText("Please enter a task name")
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.dragPos is not None:
            self.move(event.globalPos() - self.dragPos)
            event.accept()