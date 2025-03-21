from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QFrame, QListWidget, QListWidgetItem,
                           QApplication)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor

class NotesWindow(QDialog):
    # Signal to emit when the user wants to proceed to the next phase
    nextPhaseRequested = pyqtSignal()
    
    def __init__(self, parent=None, phase_history=None, current_phase=0):
        super().__init__(parent)
        # Remove default window frame and set always on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Initialize phase history and current phase
        self.phase_history = phase_history if phase_history else []
        self.current_phase = current_phase
        
        # Initialize dragPos for mouse events
        self.dragPos = None
        
        # Apply dark theme stylesheet
        self.apply_dark_stylesheet()
        
        # Set up the UI
        self.setup_ui()
        
        # Position the dialog in the center of the screen
        desktop = QApplication.desktop()
        screen_rect = desktop.availableGeometry(self)
        self.move(screen_rect.center() - self.rect().center())
    
    def apply_dark_stylesheet(self):
        """Apply a consistent dark theme to all widgets"""
        self.setStyleSheet("""
            QDialog {
                background-color: transparent;
            }
            QFrame {
                background-color: rgba(30, 30, 30, 220);
                border-radius: 10px;
                border: 1px solid rgba(120, 120, 120, 100);
            }
            QWidget {
                background-color: transparent;
            }
            QLabel {
                color: white;
            }
            QListWidget {
                background-color: rgba(40, 40, 40, 150);
                border-radius: 5px;
                color: white;
                padding: 5px;
                border: 1px solid rgba(60, 60, 60, 100);
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid rgba(100, 100, 100, 80);
            }
            QListWidget::item:selected {
                background-color: rgba(60, 60, 60, 200);
            }
            QPushButton {
                background-color: rgba(60, 60, 60, 180);
                color: white;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: rgba(80, 80, 80, 180);
            }
            QPushButton#nextPhaseButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                           stop:0 rgba(0, 255, 255, 150), 
                                           stop:1 rgba(255, 0, 255, 150));
                color: white;
                font-weight: bold;
            }
            QPushButton#nextPhaseButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                           stop:0 rgba(0, 255, 255, 200), 
                                           stop:1 rgba(255, 0, 255, 200));
            }
        """)
    
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Create a frame with rounded corners and semi-transparent background
        container = QFrame(self)
        container.setObjectName("notesContainer")
        
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Phase Completion")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        container_layout.addWidget(title_label)
        
        # Current phase label
        current_phase_label = QLabel(f"Current Phase: {self.current_phase + 1}")
        current_phase_label.setStyleSheet("color: white; font-size: 14px;")
        container_layout.addWidget(current_phase_label)
        
        # Phase history list
        history_label = QLabel("Phase History:")
        history_label.setStyleSheet("color: white; font-size: 14px;")
        container_layout.addWidget(history_label)
        
        # List widget for phase history
        self.history_list = QListWidget()
        
        # Add phase history items
        for i, entry in enumerate(self.phase_history):
            item = QListWidgetItem(f"Phase {i+1}: {entry['name']} - {entry['status']}")
            
            # Set color based on status
            if entry['status'] == 'Finished':
                item.setForeground(QColor(100, 255, 100))  # Green
            elif entry['status'] == 'Failed':
                item.setForeground(QColor(255, 100, 100))  # Red
            
            self.history_list.addItem(item)
        
        container_layout.addWidget(self.history_list)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Next Phase button
        self.next_phase_button = QPushButton("Next Phase")
        self.next_phase_button.setObjectName("nextPhaseButton")
        
        # Close button
        self.close_button = QPushButton("Close")
        
        buttons_layout.addWidget(self.next_phase_button)
        buttons_layout.addWidget(self.close_button)
        
        container_layout.addLayout(buttons_layout)
        main_layout.addWidget(container)
        
        # Connect buttons
        self.next_phase_button.clicked.connect(self.request_next_phase)
        self.close_button.clicked.connect(self.reject)
        
        # Set fixed size for dialog
        self.setFixedSize(400, 500)
    
    def request_next_phase(self):
        """Emit signal to request moving to the next phase"""
        self.nextPhaseRequested.emit()
        self.accept()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.dragPos is not None:
            self.move(event.globalPos() - self.dragPos)
            event.accept()