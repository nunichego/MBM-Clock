from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QPainter, QPixmap, QLinearGradient, QColor
from PyQt5.QtCore import QSize, Qt

class GradientIconButton(QPushButton):
    def __init__(self, icon_path, parent=None):
        super().__init__(parent)
        self.original_pixmap = QPixmap(icon_path)
        self.start_color = QColor(255, 0, 255)    # Default magenta
        self.end_color = QColor(0, 255, 255)      # Default cyan
        
        # Set button properties
        self.setFlat(True)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;  /* Remove the border */
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 10);  /* Very subtle hover effect */
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 10);  /* Very subtle pressed effect */
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
        
        # Set a fixed size for the button that matches the icon size to ensure click area
        # preserves the intended rectangular area
        if not self.original_pixmap.isNull():
            iconSize = self.iconSize()
            self.setFixedSize(iconSize.width() + 10, iconSize.height() + 10)  # Add padding
    
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
            # Update the button size to match icon size plus padding
            self.setFixedSize(new_width + 10, new_height + 10)