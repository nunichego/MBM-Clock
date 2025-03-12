import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QFontDatabase

class TimerWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Load the custom font
        font_id = QFontDatabase.addApplicationFont("resources/fonts/TickingTimebombBB.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        custom_font = QFont(font_family, 50)  # font size 42
        
        # Set up the window...
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Set up layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Create time display label with custom font
        self.time_label = QLabel("00:00:00")
        self.time_label.setFont(custom_font)
        self.time_label.setStyleSheet("color: white;")
        self.time_label.setAlignment(Qt.AlignCenter)
        
        # Add label to layout
        layout.addWidget(self.time_label)
        
        # Set up initial position
        self.setGeometry(50, 900, 150, 50)
        
        # Variables for dragging
        self.dragging = False
        self.offset = None
        
    # Mouse event handlers for dragging...
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