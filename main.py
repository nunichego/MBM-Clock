import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QFontDatabase, QLinearGradient, QPainter, QColor, QPen, QBrush

try:
    import win32gui
    import win32con
    USING_WINDOWS = True
except ImportError:
    USING_WINDOWS = False
    print("PyWin32 not found. Install with: pip install pywin32")

# Import the GradientIconButton class
from gradient_icon_button import GradientIconButton

class GradientLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.start_color = QColor(0, 255, 255)  # Cyan
        self.end_color = QColor(255, 0, 255)    # Magenta
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, self.start_color)
        gradient.setColorAt(1.0, self.end_color)
        
        painter.setFont(self.font())
        pen = QPen(QBrush(gradient), 1)
        painter.setPen(pen)
        
        # Get the text size that would be natural for this font
        text_rect = painter.fontMetrics().boundingRect(self.text())
        
        # Center it in our widget
        text_rect.moveCenter(self.rect().center())
        
        # Draw the text in its natural dimensions
        painter.drawText(text_rect, Qt.AlignCenter, self.text())
    
    def setGradientColors(self, start_color, end_color):
        """Update the gradient colors"""
        self.start_color = start_color
        self.end_color = end_color
        self.update()  # Trigger repaint


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
        self.time_label = GradientLabel("30:00")
        self.time_label.setFont(custom_font)

        # Create horizontal layout for buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)  # Space between buttons

        # Create three gradient icon buttons
        self.note_button = GradientIconButton("resources/icons/button_prototype.png")
        self.settings_button = GradientIconButton("resources/icons/button_prototype.png")
        self.close_app_button = GradientIconButton("resources/icons/button_prototype.png")

        # Make them square-shaped
        button_size = 40
        for button in [self.note_button, self.settings_button, self.close_app_button]:
            button.setFixedSize(button_size, button_size)
            button.setIconScale(0.4)  # Scale icon to 40% of original size

        # Connect the close button
        self.close_app_button.clicked.connect(QApplication.quit)
        
        # Add buttons to the horizontal layout
        buttons_layout.addWidget(self.note_button)
        buttons_layout.addWidget(self.settings_button)
        buttons_layout.addWidget(self.close_app_button)
        
        # Add label and buttons to layout
        layout.addWidget(self.time_label)
        layout.addLayout(buttons_layout)
        
        # Set up initial position and size
        self.setGeometry(50, 900, 200, 80)
        
        # Variables for dragging
        self.dragging = False
        self.offset = None
        
        # Initialize timer
        self.seconds = 1500
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
        self.seconds -= 1
        minutes = self.seconds // 60
        seconds = self.seconds % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.time_label.setText(time_str)
    
    def update_gradient_colors(self, start_color, end_color):
        """Update the gradient colors for all gradient elements"""
        # Update the timer label gradient
        self.time_label.setGradientColors(start_color, end_color)
        
        # Update all button gradients
        for button in [self.note_button, self.settings_button, self.close_app_button]:
            button.setGradientColors(start_color, end_color)
        
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
    
    # Example of updating gradient colors
    # timer_window.update_gradient_colors(QColor(0, 255, 128), QColor(128, 0, 255))
    
    timer_window.show()
    
    sys.exit(app.exec_())