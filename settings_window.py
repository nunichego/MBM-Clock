from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QSlider, QPushButton, QFrame, QComboBox,
                           QLineEdit, QScrollArea, QWidget, QSpinBox,
                           QGridLayout, QApplication, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QIntValidator

class PhaseSettings:
    """Class to store phase settings"""
    def __init__(self, name="Phase", minutes=30, seconds=0):
        self.name = name
        self.minutes = minutes
        self.seconds = seconds
    
    def get_total_seconds(self):
        """Get total seconds for this phase"""
        return self.minutes * 60 + self.seconds


class SettingsWindow(QDialog):
    # Signal to emit when settings change
    settingsChanged = pyqtSignal(float, list)  # scale factor, list of phase settings
    
    def __init__(self, parent=None, current_scale=1.0, phases=None):
        super().__init__(parent)
        # Remove default window frame and set always on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Track current scale
        self.current_scale = current_scale
        
        # Initialize dragPos for mouse events
        self.dragPos = None
        
        # Initialize phases
        if phases is None:
            self.phases = [PhaseSettings()]
        else:
            self.phases = phases
        
        # Set up fonts
        self.setup_fonts()
        
        # Apply modern stylesheet
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
        self.regular_font = QFont("Calibri", 11)
        self.bold_font = QFont("Calibri", 12)
        self.bold_font.setBold(True)
        self.title_font = QFont("Calibri", 16)
        self.title_font.setBold(True)
    
    def create_shadow_effect(self):
        """Create a shadow effect for the main frame"""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 0)
        return shadow
    
    def apply_modern_stylesheet(self):
        """Apply a modern minimalist theme"""
        self.setStyleSheet("""
            QDialog {
                background-color: transparent;
            }
            QFrame#settingsContainer {
                background-color: rgb(40, 40, 40);
                border-radius: 15px;
                border: none;
            }
            QWidget {
                background-color: transparent;
            }
            QLabel {
                color: rgb(240, 240, 240);
                background-color: transparent;
                border: none;
            }
            QLineEdit, QComboBox, QSpinBox {
                background-color: rgb(55, 55, 55);
                color: white;
                border-radius: 8px;
                padding: 6px 10px;
                border: none;
                selection-background-color: rgb(70, 130, 180);
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                background-color: rgb(60, 60, 60);
            }
            QPushButton {
                background-color: rgb(55, 55, 55);
                color: white;
                border-radius: 8px;
                padding: 6px 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgb(65, 65, 65);
            }
            QPushButton:pressed {
                background-color: rgb(50, 50, 50);
            }
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: rgb(45, 45, 45);
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                           stop:0 rgb(0, 255, 255), 
                                           stop:1 rgb(255, 0, 255));
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                           stop:0 rgb(0, 255, 255), 
                                           stop:1 rgb(255, 0, 255));
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: white;
                border: none;
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: rgb(50, 50, 50);
                border: none;
                selection-background-color: rgb(70, 130, 180);
                color: white;
            }
            QFrame#phaseFrame {
                background-color: rgb(45, 45, 45);
                border-radius: 10px;
                border: none;
            }
        """)
    
    def setup_ui(self):
        # Main layout with margins for shadow effect
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Create a frame with rounded corners
        container = QFrame(self)
        container.setObjectName("settingsContainer")
        container.setGraphicsEffect(self.create_shadow_effect())
        
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(20)
        container_layout.setContentsMargins(24, 24, 24, 24)
        
        # Title
        title_label = QLabel("Settings")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(self.title_font)
        container_layout.addWidget(title_label)
        
        # Create a scroll area for settings
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Create a widget to hold all settings
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        settings_layout.setSpacing(20)
        
        # Size adjustment section
        size_layout = QVBoxLayout()
        
        # Size label
        size_label = QLabel("Timer Size")
        size_label.setFont(self.bold_font)
        size_layout.addWidget(size_label)
        
        # Size slider and value
        slider_value_layout = QHBoxLayout()
        
        # Create the slider
        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setRange(50, 150)  # 0.5 to 1.5 (x100 for integer steps)
        self.size_slider.setValue(int(self.current_scale * 100))
        
        # Value label
        self.size_value = QLabel(f"{self.current_scale:.1f}x")
        self.size_value.setFont(self.regular_font)
        self.size_value.setMinimumWidth(40)
        
        slider_value_layout.addWidget(self.size_slider)
        slider_value_layout.addWidget(self.size_value)
        
        size_layout.addLayout(slider_value_layout)
        settings_layout.addLayout(size_layout)
        
        # Connect slider to update value label
        self.size_slider.valueChanged.connect(self.update_size_value)
        
        # Number of phases section
        phases_layout = QVBoxLayout()
        
        # Label
        phases_label = QLabel("Number of Phases")
        phases_label.setFont(self.bold_font)
        phases_layout.addWidget(phases_label)
        
        # Combo box for number of phases
        self.phases_combo = QComboBox()
        self.phases_combo.addItems(["1", "2", "3", "4", "5"])
        self.phases_combo.setCurrentIndex(len(self.phases) - 1)  # Set based on current phases
        self.phases_combo.setFont(self.regular_font)
        
        phases_layout.addWidget(self.phases_combo)
        settings_layout.addLayout(phases_layout)
        
        # Connect combo box to update phases
        self.phases_combo.currentIndexChanged.connect(self.update_phase_count)
        
        # Create a container for phase settings
        self.phases_container = QVBoxLayout()
        self.phase_widgets = []  # Store references to phase widgets
        
        # Create phase settings based on current phase count
        self.create_phase_settings()
        
        settings_layout.addLayout(self.phases_container)
        
        # Add the settings widget to the scroll area
        scroll_area.setWidget(settings_widget)
        container_layout.addWidget(scroll_area)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Apply button
        self.apply_button = QPushButton("Apply")
        self.apply_button.setFont(self.bold_font)
        
        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFont(self.regular_font)
        
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.apply_button)
        
        container_layout.addLayout(buttons_layout)
        main_layout.addWidget(container)
        
        # Connect buttons
        self.apply_button.clicked.connect(self.apply_settings)
        self.cancel_button.clicked.connect(self.reject)
        
        # Set dynamic size for dialog
        self.setMinimumSize(450, 600)
        self.setMaximumSize(550, 800)
    
    def create_phase_settings(self):
        """Create UI elements for each phase"""
        # Clear existing phase widgets
        for widget in self.phase_widgets:
            # Remove widget from layout
            self.phases_container.removeWidget(widget)
            # Mark for deletion
            widget.deleteLater()
        
        self.phase_widgets = []
        
        # Add phase settings for each phase
        for i, phase in enumerate(self.phases):
            # Create a frame for this phase
            phase_frame = QFrame()
            phase_frame.setObjectName("phaseFrame")
            
            # Layout for this phase
            phase_layout = QVBoxLayout(phase_frame)
            phase_layout.setContentsMargins(15, 15, 15, 15)
            phase_layout.setSpacing(15)
            
            # Phase title with name field
            title_layout = QHBoxLayout()
            ordinal = ["1st", "2nd", "3rd", "4th", "5th"][i]
            phase_title = QLabel(f"{ordinal} Phase Name:")
            phase_title.setFont(self.bold_font)
            
            name_edit = QLineEdit(phase.name)
            name_edit.setFont(self.regular_font)
            name_edit.setProperty("phaseIndex", i)
            name_edit.textChanged.connect(lambda text, idx=i: self.update_phase_name(idx, text))
            
            title_layout.addWidget(phase_title)
            title_layout.addWidget(name_edit)
            phase_layout.addLayout(title_layout)
            
            # Duration settings
            duration_layout = QGridLayout()
            duration_layout.setVerticalSpacing(10)
            duration_layout.setHorizontalSpacing(5)
            
            # Work duration
            duration_label = QLabel("Length:")
            duration_label.setFont(self.regular_font)
            
            minutes_spin = QSpinBox()
            minutes_spin.setRange(0, 180)
            minutes_spin.setValue(phase.minutes)
            minutes_spin.setFont(self.regular_font)
            minutes_spin.setProperty("phaseIndex", i)
            minutes_spin.valueChanged.connect(
                lambda value, idx=i: self.update_phase_time(idx, "minutes", value)
            )
            
            minutes_label = QLabel("min")
            minutes_label.setFont(self.regular_font)
            
            seconds_spin = QSpinBox()
            seconds_spin.setRange(0, 59)
            seconds_spin.setValue(phase.seconds)
            seconds_spin.setFont(self.regular_font)
            seconds_spin.setProperty("phaseIndex", i)
            seconds_spin.valueChanged.connect(
                lambda value, idx=i: self.update_phase_time(idx, "seconds", value)
            )
            
            seconds_label = QLabel("sec")
            seconds_label.setFont(self.regular_font)
            
            duration_layout.addWidget(duration_label, 0, 0)
            duration_layout.addWidget(minutes_spin, 0, 1)
            duration_layout.addWidget(minutes_label, 0, 2)
            duration_layout.addWidget(seconds_spin, 0, 3)
            duration_layout.addWidget(seconds_label, 0, 4)
            
            phase_layout.addLayout(duration_layout)
            
            # Add the phase frame to the container
            self.phases_container.addWidget(phase_frame)
            self.phase_widgets.append(phase_frame)
    
    def update_phase_count(self, index):
        """Update the number of phases based on combo box selection"""
        num_phases = index + 1  # Index 0 = 1 phase, etc.
        
        # Adjust the phases list
        if num_phases > len(self.phases):
            # Add new phases
            for _ in range(num_phases - len(self.phases)):
                self.phases.append(PhaseSettings())
        else:
            # Remove phases
            self.phases = self.phases[:num_phases]
        
        # Recreate the UI elements
        self.create_phase_settings()
    
    def update_phase_name(self, index, name):
        """Update the name of a phase"""
        if 0 <= index < len(self.phases):
            self.phases[index].name = name
    
    def update_phase_time(self, index, time_type, value):
        """Update a time value for a phase"""
        if 0 <= index < len(self.phases):
            setattr(self.phases[index], time_type, value)
    
    def update_size_value(self):
        """Update the size value label when the slider changes"""
        value = self.size_slider.value() / 100.0
        self.size_value.setText(f"{value:.1f}x")
    
    def apply_settings(self):
        """Apply the selected settings and emit signal"""
        new_scale = self.size_slider.value() / 100.0
        self.settingsChanged.emit(new_scale, self.phases)
        self.accept()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.dragPos is not None:
            self.move(event.globalPos() - self.dragPos)
            event.accept()