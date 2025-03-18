import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QFontDatabase, QLinearGradient, QPainter, QColor, QPen, QBrush

try:
    import win32gui
    import win32con
    USING_WINDOWS = True
except ImportError:
    USING_WINDOWS = False
    print("PyWin32 not found. Install with: pip install pywin32")

class GradientLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0.0, QColor(0, 255, 255))   # Cyan
        gradient.setColorAt(1.0, QColor(255, 0, 255))   # Magenta
        
        painter.setFont(self.font())
        pen = QPen(QBrush(gradient), 1)
        painter.setPen(pen)
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())


class TimerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set window flags
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Set up layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Load font
        try:
            font_id = QFontDatabase.addApplicationFont("resources/fonts/RobotoCondensed-Bold.ttf")
            if font_id != -1:
                font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
                custom_font = QFont(font_family, 50)
            else:
                custom_font = QFont("Arial", 50, QFont.Bold)
        except:
            custom_font = QFont("Arial", 50, QFont.Bold)
        
        # Create gradient label for the timer
        self.time_label = GradientLabel("00:00")
        self.time_label.setFont(custom_font)
        
        # Add label to layout
        layout.addWidget(self.time_label)
        
        # Add a close button
        self.close_button = QPushButton("×")
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: gray;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                color: red;
            }
        """)
        self.close_button.clicked.connect(QApplication.quit)
        self.close_button.setFixedSize(20, 20)
        
        # Add close button to a corner
        self.close_button.setParent(central_widget)
        self.close_button.move(180, 0)
        
        # Set up initial position and size
        self.setGeometry(50, 900, 200, 80)
        
        # Variables for dragging
        self.dragging = False
        self.offset = None
        
        # Initialize timer
        self.seconds = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second
        
        # Set up Windows-specific topmost behavior
        if USING_WINDOWS:
            self.topmost_timer = QTimer(self)
            self.topmost_timer.timeout.connect(self.ensure_topmost)
            self.topmost_timer.start(500)  # Check every 500ms
    
    def ensure_topmost(self):
        """Force window to stay on top using Windows API"""
        if USING_WINDOWS:
            hwnd = int(self.winId())
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 
                               win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    
    def update_time(self):
        self.seconds += 1
        minutes = self.seconds // 60
        seconds = self.seconds % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.time_label.setText(time_str)
        
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
            # Ensure topmost after dragging
            if USING_WINDOWS:
                self.ensure_topmost()

    def showEvent(self, event):
        super().showEvent(event)
        # Ensure topmost when first shown
        if USING_WINDOWS:
            self.ensure_topmost()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    timer_window = TimerWindow()
    timer_window.show()
    
    sys.exit(app.exec_())