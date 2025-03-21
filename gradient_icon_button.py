from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QPainter, QPixmap, QLinearGradient, QColor
from PyQt5.QtCore import QSize, Qt

class GradientIconButton(QPushButton):
    def __init__(self, icon_path, parent=None):
        super().__init__(parent)
        self.original_pixmap = QPixmap(icon_path)
        self.start_color = QColor(255, 0, 255)    # Default magenta
        self.end_color = QColor(0, 255, 255)  # Default cyan
        
        # Set button properties
        self.setFlat(True)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid rgba(128, 128, 128, 50);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 30);
            }
        """)
        
        # Generate and apply the gradient icon
        self.update_gradient_icon()
    
    def update_gradient_icon(self):
        """Apply the current gradient to the icon"""
        if self.original_pixmap.isNull():
            return  # Guard against invalid pixmap
            
        # Create a copy of the original pixmap to apply the gradient
        pixmap = self.original_pixmap.copy()
        
        # Create a painter for the pixmap
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create gradient
        gradient = QLinearGradient(0, 0, 0, pixmap.height())
        gradient.setColorAt(0.0, self.start_color)
        gradient.setColorAt(1.0, self.end_color)
        
        # Apply the gradient using composition mode to preserve transparency
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), gradient)
        painter.end()
        
        # Set the gradient-applied icon
        self.setIcon(QIcon(pixmap))
        self.setIconSize(QSize(pixmap.width() // 9, pixmap.height() // 9))  # Scale down by default
    
    def setGradientColors(self, start_color, end_color):
        """Update the gradient colors and refresh the icon"""
        self.start_color = start_color
        self.end_color = end_color
        self.update_gradient_icon()
    
    def setIconScale(self, scale_factor):
        """Set icon size relative to original pixmap size"""
        if not self.original_pixmap.isNull():
            new_width = int(self.original_pixmap.width() * scale_factor)
            new_height = int(self.original_pixmap.height() * scale_factor)
            self.setIconSize(QSize(new_width, new_height))

# Example modifications to your TimerWindow class:
"""
# Replace your button creation with:
self.note_button = GradientIconButton("resources/icons/button_prototype.png")
self.settings_button = GradientIconButton("resources/icons/button_prototype.png")
self.close_app_button = GradientIconButton("resources/icons/button_prototype.png")

# Set custom sizes if needed
button_size = 40
for button in [self.note_button, self.settings_button, self.close_app_button]:
    button.setFixedSize(button_size, button_size)
    button.setIconScale(0.4)  # Scale icon to 40% of original size

# Connect the close button
self.close_app_button.clicked.connect(QApplication.quit)
"""