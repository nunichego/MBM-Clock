import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

class TimerWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Remove window border and make it stay on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        # Make the window background transparent
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Set up the main layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Create time display label
        self.time_label = QLabel("00:00:00")
        self.time_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.time_label.setStyleSheet("color: white;")  # White text
        self.time_label.setAlignment(Qt.AlignCenter)
        
        # Add the label to the layout
        layout.addWidget(self.time_label)
        
        # Set up initial position
        self.setGeometry(100, 100, 150, 50)
        
        # Variable to track mouse position for dragging
        self.dragging = False
        self.offset = None
        
        # For now, the timer doesn't actually count
        # We'll implement that in the next step

    # Enable dragging the window with the mouse
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging and self.offset:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

# Create the application
app = QApplication(sys.argv)

# Create and show the timer window
timer_window = TimerWindow()
timer_window.show()

# Start the application event loop
sys.exit(app.exec_())