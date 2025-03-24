from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QLinearGradient, QPainter, QColor, QPen, QBrush


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
        
        text_rect = painter.fontMetrics().boundingRect(self.text())
        
        # Center text in widget
        text_rect.moveCenter(self.rect().center())
        
        painter.drawText(text_rect, Qt.AlignCenter, self.text())
    
    def setGradientColors(self, start_color, end_color):
        self.start_color = start_color
        self.end_color = end_color
        self.update()  # Trigger repaint