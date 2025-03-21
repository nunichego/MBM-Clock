from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QSlider, QPushButton, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor

class SettingsWindow(QDialog):
    # Signal to emit when settings change
    settingsChanged = pyqtSignal(float)
    
    def __init__(self, parent=None, current_scale=1.0):
        super().__init__(parent)
        # Remove default window frame and set always on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Track current scale
        self.current_scale = current_scale
        
        # Set up the UI
        self.setup_ui()
        
        # Position the dialog relative to the parent
        if parent:
            parent_pos = parent.pos()
            parent_size = parent.size()
            self.move(parent_pos.x() + parent_size.width() + 10, parent_pos.y())
    
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Create a frame with rounded corners and semi-transparent background
        container = QFrame(self)
        container.setObjectName("settingsContainer")
        container.setStyleSheet("""
            #settingsContainer {
                background-color: rgba(30, 30, 30, 220);
                border-radius: 10px;
                border: 1px solid rgba(120, 120, 120, 100);
            }
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Settings")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        container_layout.addWidget(title_label)
        
        # Size adjustment section
        size_layout = QVBoxLayout()
        
        # Size label
        size_label = QLabel("Timer Size")
        size_label.setStyleSheet("color: white;")
        size_layout.addWidget(size_label)
        
        # Size slider and value
        slider_value_layout = QHBoxLayout()
        
        # Create the slider
        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setRange(50, 150)  # 0.5 to 1.5 (x100 for integer steps)
        self.size_slider.setValue(int(self.current_scale * 100))
        self.size_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                           stop:0 rgba(0, 255, 255, 150), 
                                           stop:1 rgba(255, 0, 255, 150));
                border-radius: 4px;
            }
            
            QSlider::handle:horizontal {
                background: white;
                border: 1px solid #777;
                width: 16px;
                margin-top: -5px;
                margin-bottom: -5px;
                border-radius: 8px;
            }
        """)
        
        # Value label
        self.size_value = QLabel(f"{self.current_scale:.1f}x")
        self.size_value.setStyleSheet("color: white; min-width: 40px;")
        
        slider_value_layout.addWidget(self.size_slider)
        slider_value_layout.addWidget(self.size_value)
        
        size_layout.addLayout(slider_value_layout)
        container_layout.addLayout(size_layout)
        
        # Connect slider to update value label
        self.size_slider.valueChanged.connect(self.update_size_value)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Apply button
        self.apply_button = QPushButton("Apply")
        self.apply_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(60, 60, 60, 180);
                color: white;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: rgba(80, 80, 80, 180);
            }
        """)
        
        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(60, 60, 60, 180);
                color: white;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: rgba(80, 80, 80, 180);
            }
        """)
        
        buttons_layout.addWidget(self.apply_button)
        buttons_layout.addWidget(self.cancel_button)
        
        container_layout.addLayout(buttons_layout)
        main_layout.addWidget(container)
        
        # Connect buttons
        self.apply_button.clicked.connect(self.apply_settings)
        self.cancel_button.clicked.connect(self.reject)
        
        # Set fixed size for dialog
        self.setFixedSize(300, 200)
    
    def update_size_value(self):
        """Update the size value label when the slider changes"""
        value = self.size_slider.value() / 100.0
        self.size_value.setText(f"{value:.1f}x")
    
    def apply_settings(self):
        """Apply the selected settings and emit signal"""
        new_scale = self.size_slider.value() / 100.0
        self.settingsChanged.emit(new_scale)
        self.accept()
    
    def __init__(self, parent=None, current_scale=1.0):
        super().__init__(parent)
        # Remove default window frame and set always on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Track current scale
        self.current_scale = current_scale
        
        # Initialize dragPos for mouse events
        self.dragPos = None
        
        # Set up the UI
        self.setup_ui()
        
        # Position the dialog relative to the parent
        if parent:
            parent_pos = parent.pos()
            parent_size = parent.size()
            self.move(parent_pos.x() + parent_size.width() + 10, parent_pos.y())
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.dragPos is not None:
            self.move(event.globalPos() - self.dragPos)
            event.accept()