from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QSlider, QPushButton, QFrame, QComboBox,
                           QLineEdit, QScrollArea, QWidget, QSpinBox,
                           QGridLayout, QApplication)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QIntValidator

class PhaseSettings:
    """Class to store phase settings"""
    def __init__(self, name="Phase", minutes=30, seconds=0, break_minutes=5, break_seconds=0):
        self.name = name
        self.minutes = minutes
        self.seconds = seconds
        self.break_minutes = break_minutes
        self.break_seconds = break_seconds
    
    def get_total_seconds(self):
        """Get total seconds for this phase"""
        return self.minutes * 60 + self.seconds
    
    def get_break_total_seconds(self):
        """Get total seconds for the break of this phase"""
        return self.break_minutes * 60 + self.break_seconds


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
        
        # Apply global stylesheet
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
            QComboBox, QLineEdit, QSpinBox {
                background-color: rgba(60, 60, 60, 180);
                color: white;
                border-radius: 5px;
                padding: 5px;
                selection-background-color: rgba(70, 130, 180, 150);
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                background-color: rgba(45, 45, 45, 230);
                border: 1px solid rgba(80, 80, 80, 120);
                selection-background-color: rgba(0, 255, 255, 50);
                color: white;
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
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: rgba(40, 40, 40, 120);
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 rgba(0, 255, 255, 150), 
                                          stop:1 rgba(255, 0, 255, 150));
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
    
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Create a frame with rounded corners and semi-transparent background
        container = QFrame(self)
        container.setObjectName("settingsContainer")
        
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Settings")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
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
        size_layout.addWidget(size_label)
        
        # Size slider and value
        slider_value_layout = QHBoxLayout()
        
        # Create the slider
        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setRange(50, 150)  # 0.5 to 1.5 (x100 for integer steps)
        self.size_slider.setValue(int(self.current_scale * 100))
        
        # Value label
        self.size_value = QLabel(f"{self.current_scale:.1f}x")
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
        phases_layout.addWidget(phases_label)
        
        # Combo box for number of phases
        self.phases_combo = QComboBox()
        self.phases_combo.addItems(["1", "2", "3", "4", "5"])
        self.phases_combo.setCurrentIndex(len(self.phases) - 1)  # Set based on current phases
        
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
        
        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        
        buttons_layout.addWidget(self.apply_button)
        buttons_layout.addWidget(self.cancel_button)
        
        container_layout.addLayout(buttons_layout)
        main_layout.addWidget(container)
        
        # Connect buttons
        self.apply_button.clicked.connect(self.apply_settings)
        self.cancel_button.clicked.connect(self.reject)
        
        # Set dynamic size for dialog
        self.setMinimumSize(400, 500)
        self.setMaximumSize(500, 800)
    
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
            
            # Layout for this phase
            phase_layout = QVBoxLayout(phase_frame)
            
            # Phase title with name field
            title_layout = QHBoxLayout()
            ordinal = ["1st", "2nd", "3rd", "4th", "5th"][i]
            phase_title = QLabel(f"{ordinal} Phase Name:")
            
            name_edit = QLineEdit(phase.name)
            name_edit.setProperty("phaseIndex", i)
            name_edit.textChanged.connect(lambda text, idx=i: self.update_phase_name(idx, text))
            
            title_layout.addWidget(phase_title)
            title_layout.addWidget(name_edit)
            phase_layout.addLayout(title_layout)
            
            # Duration settings
            duration_layout = QGridLayout()
            
            # Work duration
            duration_label = QLabel("Length:")
            
            minutes_spin = QSpinBox()
            minutes_spin.setRange(0, 180)
            minutes_spin.setValue(phase.minutes)
            minutes_spin.setProperty("phaseIndex", i)
            minutes_spin.setProperty("timeType", "work")
            minutes_spin.valueChanged.connect(
                lambda value, idx=i: self.update_phase_time(idx, "minutes", value)
            )
            
            minutes_label = QLabel("min")
            
            seconds_spin = QSpinBox()
            seconds_spin.setRange(0, 59)
            seconds_spin.setValue(phase.seconds)
            seconds_spin.setProperty("phaseIndex", i)
            seconds_spin.valueChanged.connect(
                lambda value, idx=i: self.update_phase_time(idx, "seconds", value)
            )
            
            seconds_label = QLabel("sec")
            
            duration_layout.addWidget(duration_label, 0, 0)
            duration_layout.addWidget(minutes_spin, 0, 1)
            duration_layout.addWidget(minutes_label, 0, 2)
            duration_layout.addWidget(seconds_spin, 0, 3)
            duration_layout.addWidget(seconds_label, 0, 4)
            
            # Break duration
            break_label = QLabel("Break:")
            
            break_min_spin = QSpinBox()
            break_min_spin.setRange(0, 60)
            break_min_spin.setValue(phase.break_minutes)
            break_min_spin.setProperty("phaseIndex", i)
            break_min_spin.valueChanged.connect(
                lambda value, idx=i: self.update_phase_time(idx, "break_minutes", value)
            )
            
            break_min_label = QLabel("min")
            
            break_sec_spin = QSpinBox()
            break_sec_spin.setRange(0, 59)
            break_sec_spin.setValue(phase.break_seconds)
            break_sec_spin.setProperty("phaseIndex", i)
            break_sec_spin.valueChanged.connect(
                lambda value, idx=i: self.update_phase_time(idx, "break_seconds", value)
            )
            
            break_sec_label = QLabel("sec")
            
            duration_layout.addWidget(break_label, 1, 0)
            duration_layout.addWidget(break_min_spin, 1, 1)
            duration_layout.addWidget(break_min_label, 1, 2)
            duration_layout.addWidget(break_sec_spin, 1, 3)
            duration_layout.addWidget(break_sec_label, 1, 4)
            
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