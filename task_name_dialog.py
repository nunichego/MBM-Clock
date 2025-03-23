from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QFrame, QLineEdit, QApplication)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor

class TaskNameDialog(QDialog):
    # Signal to emit when the user submits a task name
    taskNameSubmitted = pyqtSignal(str)
    
    def __init__(self, parent=None, style_manager=None):
        super().__init__(parent)
        # Remove default window frame and set always on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Store style manager reference
        self.style_manager = style_manager
        
        # Initialize dragPos for mouse events
        self.dragPos = None
        
        # Set up fonts
        self.setup_fonts()
        
        # Apply modern theme stylesheet
        self.apply_modern_stylesheet()
        
        # Set up the UI
        self.setup_ui()
        
        # Position the dialog in the center of the screen
        desktop = QApplication.desktop()
        screen_rect = desktop.availableGeometry(self)
        self.move(screen_rect.center() - self.rect().center())
    
    def setup_fonts(self):
        """Set up custom fonts for the application"""
        # Try to use Calibri if available, otherwise fall back to system sans-serif
        self.regular_font = QFont("Calibri", 10)
        self.bold_font = QFont("Calibri", 11)
        self.bold_font.setBold(True)
        self.title_font = QFont("Calibri", 14)
        self.title_font.setBold(True)
        
    def apply_modern_stylesheet(self):
        """Apply a modern minimalist theme"""
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
        # Main layout with some margin for shadow effect
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Create a frame with rounded corners
        container = QFrame(self)
        container.setObjectName("mainContainer")
        container.setGraphicsEffect(self.create_shadow_effect())
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(24, 24, 24, 24)
        container_layout.setSpacing(16)
        
        # Title
        title_label = QLabel("New Task")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(self.title_font)
        container_layout.addWidget(title_label)
        
        # Task name input
        task_name_label = QLabel("Enter Task Name:")
        task_name_label.setFont(self.regular_font)
        container_layout.addWidget(task_name_label)
        
        self.task_name_input = QLineEdit()
        self.task_name_input.setPlaceholderText("e.g., Study Session, Work Project, etc.")
        self.task_name_input.setFont(self.regular_font)
        self.task_name_input.returnPressed.connect(self.submit_task_name)
        container_layout.addWidget(self.task_name_input)
        
        # Add some space
        container_layout.addSpacing(8)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        
        # Start Task button
        self.start_button = QPushButton("Start Task")
        self.start_button.setObjectName("startButton")
        self.start_button.setFont(self.bold_font)
        
        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFont(self.regular_font)
        
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.start_button)
        
        container_layout.addLayout(buttons_layout)
        main_layout.addWidget(container)
        
        # Connect buttons
        self.start_button.clicked.connect(self.submit_task_name)
        self.cancel_button.clicked.connect(self.reject)
        
        # Set focus on the input field
        self.task_name_input.setFocus()
        
        # Set size for dialog - slightly bigger for better proportions on high-res displays
        self.setFixedSize(450, 240)
    
    def create_shadow_effect(self):
        """Create a shadow effect for the main frame"""
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 0)
        return shadow
    
    def submit_task_name(self):
        """Submit the task name and close the dialog"""
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