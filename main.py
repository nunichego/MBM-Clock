import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QFontDatabase, QLinearGradient, QPainter, QColor, QPen, QBrush
from settings_window import SettingsWindow, PhaseSettings
from notes_window import NotesWindow
from settings_manager import SettingsManager

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

        # Initialize settings manager
        self.settings_manager = SettingsManager()
    
        # Load saved settings
        self.load_saved_settings()
        
        # Initialize timer variable (but don't start the timer yet)
        self.seconds = 0  # Will be set properly later
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        
        # Initialize blinking variables for phase completion
        self.is_blinking = False
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.toggle_blink_state)
        self.blink_state = False
        self.original_colors = (QColor(0, 255, 255), QColor(255, 0, 255))  # Store original gradient colors
        
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
        
        # Create gradient label for the timer (with an empty initial value)
        self.time_label = GradientLabel("")
        self.time_label.setFont(custom_font)
        
        # Create horizontal layout for buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)  # Space between buttons
        
        # Create three gradient icon buttons
        self.note_button = GradientIconButton("resources/icons/notes_300.png")
        self.settings_button = GradientIconButton("resources/icons/settings_300.png")
        self.close_app_button = GradientIconButton("resources/icons/close_300.png")
        
        # Make them square-shaped
        button_size = 40
        for button in [self.note_button, self.settings_button, self.close_app_button]:
            button.setFixedSize(button_size, button_size)
            button.setIconScale(0.125)  # Scale icon to 40% of original size
        
        # Connect the buttons
        self.close_app_button.clicked.connect(QApplication.quit)
        self.settings_button.clicked.connect(self.open_settings)
        self.note_button.clicked.connect(self.open_notes)
        
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
        
        # Store original UI metrics for scaling
        self.original_button_size = 40
        self.original_font_size = 50
        self.original_spacing = 10
        self.original_width = 200
        self.original_height = 80
        
        # Now apply the initial scale from loaded settings
        self.apply_initial_scale()
        
        # Now that UI is created, set up the timer for the current phase
        self.reset_timer_for_current_phase()
        
        # Start the timer
        self.timer.start(1000)  # Update every second
        
        # Variable to track if buttons are visible
        self.buttons_visible = True
        
        # Create a timer for hiding buttons
        self.hide_buttons_timer = QTimer(self)
        self.hide_buttons_timer.timeout.connect(self.hide_buttons)
        self.hide_buttons_timer.setSingleShot(True)  # Run only once when started
        
        # Hide buttons after 5 seconds initially
        self.show_buttons_temporarily()
        
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
    
    def update_gradient_colors(self, start_color, end_color):
        """Update the gradient colors for all gradient elements"""
        # Update the timer label gradient
        self.time_label.setGradientColors(start_color, end_color)
        
        # Update all button gradients
        for button in [self.note_button, self.settings_button, self.close_app_button]:
            button.setGradientColors(start_color, end_color)
        
    def mousePressEvent(self, event):
        # Reset the timer and show buttons whenever the user clicks
        self.show_buttons_temporarily()
        
        # Keep your existing dragging code
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

    def open_settings(self):
        """Open the settings window"""
        # Calculate current scale based on font size compared to default
        current_scale = self.time_label.font().pointSize() / 50
        
        # Create and show settings window with current phases
        self.settings_dialog = SettingsWindow(self, current_scale, self.phases)
        
        # Connect the settings changed signal
        self.settings_dialog.settingsChanged.connect(self.apply_settings_changes)
        
        # Show the dialog
        self.settings_dialog.show()

    def apply_size_change(self, scale_factor):
        """Apply size changes from settings"""
        # Update font size based on original size
        font = self.time_label.font()
        new_size = int(self.original_font_size * scale_factor)
        font.setPointSize(new_size)
        self.time_label.setFont(font)
        
        # Update button sizes based on original size
        button_size = int(self.original_button_size * scale_factor)
        for button in [self.note_button, self.settings_button, self.close_app_button]:
            button.setFixedSize(button_size, button_size)
            # Adjust icon scale proportionally
            button.setIconScale(0.125 * scale_factor)
        
        # Update layout margins and spacing based on original spacing
        layout = self.centralWidget().layout()
        buttons_layout = layout.itemAt(1).layout()
        buttons_layout.setSpacing(int(self.original_spacing * scale_factor))
        
        # Adjust window size based on original dimensions
        new_width = int(self.original_width * scale_factor)
        new_height = int(self.original_height * scale_factor)
        self.resize(new_width, new_height)
        
        # Store the current scale factor for future reference
        self.current_scale = scale_factor

    def show_buttons_temporarily(self):
        """Show buttons for 5 seconds then hide them"""
        # Show the buttons
        self.set_buttons_visibility(True)
        
        # Start the timer to hide buttons after 5 seconds
        self.hide_buttons_timer.start(5000)  # 5000 ms = 5 seconds

    def hide_buttons(self):
        """Hide the buttons"""
        self.set_buttons_visibility(False)

    def set_buttons_visibility(self, visible):
        """Set the visibility of all buttons"""
        self.buttons_visible = visible
        
        # Apply visibility to all buttons
        for button in [self.note_button, self.settings_button, self.close_app_button]:
            button.setVisible(visible)

    def reset_timer_for_current_phase(self):
        """Reset the timer based on the current phase"""
        if self.current_phase_index < len(self.phases):
            phase = self.phases[self.current_phase_index]
            if self.in_break_mode:
                # Set timer to break duration
                self.seconds = phase.get_break_total_seconds()
            else:
                # Set timer to phase duration
                self.seconds = phase.get_total_seconds()
            
            # Update the display
            self.update_time_display()

    def update_time(self):
        """Updated timer tick function"""
        if self.seconds > 0:
            self.seconds -= 1
            self.update_time_display()
        else:
            # Timer reached zero
            if not self.is_blinking:
                self.start_blinking()

    def update_time_display(self):
        """Update the timer display"""
        minutes = self.seconds // 60
        seconds = self.seconds % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.time_label.setText(time_str)
        
        # Show the current phase name or break status
        if self.current_phase_index < len(self.phases):
            phase = self.phases[self.current_phase_index]
            if self.in_break_mode:
                self.setWindowTitle(f"Break - {phase.name}")
            else:
                self.setWindowTitle(f"{phase.name}")

    def start_blinking(self):
        """Start the timer blinking when phase is complete"""
        self.is_blinking = True
        self.blink_timer.start(750)  # Blink every 0.75 seconds
        
        # Stop the main timer
        self.timer.stop()

    def toggle_blink_state(self):
        """Toggle the blinking state"""
        self.blink_state = not self.blink_state
        
        if self.blink_state:
            # Change to red color scheme
            self.time_label.setGradientColors(QColor(255, 0, 0), QColor(255, 100, 0))
        else:
            # Change back to original color scheme
            self.time_label.setGradientColors(self.original_colors[0], self.original_colors[1])

    def stop_blinking(self):
        """Stop the timer blinking"""
        if self.is_blinking:
            self.is_blinking = False
            self.blink_timer.stop()
            
            # Restore original colors
            self.time_label.setGradientColors(self.original_colors[0], self.original_colors[1])

    def open_notes(self):
        """Open the notes window"""
        # If blinking, handle phase completion
        if self.is_blinking:
            self.stop_blinking()
            
            # Record the current phase status
            if self.current_phase_index < len(self.phases):
                phase = self.phases[self.current_phase_index]
                phase_entry = {
                    'name': phase.name,
                    'status': 'Finished'  # Default to finished
                }
                
                # Add to history if not already there
                if len(self.phase_history) <= self.current_phase_index:
                    self.phase_history.append(phase_entry)
                else:
                    self.phase_history[self.current_phase_index] = phase_entry
            
            # Show notes window
            self.show_notes_window()
        else:
            # Just show the notes window
            self.show_notes_window()

    def show_notes_window(self):
        """Show the notes window"""
        # Create and show notes window
        self.notes_dialog = NotesWindow(
            self, 
            phase_history=self.phase_history,
            current_phase=self.current_phase_index
        )
        
        # Connect signal for next phase
        self.notes_dialog.nextPhaseRequested.connect(self.go_to_next_phase)
        
        # Show the dialog
        self.notes_dialog.show()

    def go_to_next_phase(self):
        """Move to the next phase or break"""
        if self.in_break_mode:
            # If in break mode, move to the next phase
            self.in_break_mode = False
            self.current_phase_index += 1
            
            # Check if we've completed all phases
            if self.current_phase_index >= len(self.phases):
                # Reset to first phase
                self.current_phase_index = 0
        else:
            # If in phase mode, move to break mode if break duration > 0
            phase = self.phases[self.current_phase_index]
            if phase.get_break_total_seconds() > 0:
                self.in_break_mode = True
            else:
                # No break for this phase, move to next phase
                self.current_phase_index += 1
                if self.current_phase_index >= len(self.phases):
                    self.current_phase_index = 0
        
        # Reset the timer for the new phase/break
        self.reset_timer_for_current_phase()
        
        # Start the timer again
        self.timer.start(1000)

    def load_saved_settings(self):
        """Load settings from file"""
        settings = self.settings_manager.load_settings()
        
        # Load scale but don't apply yet (need UI elements first)
        self.current_scale = settings.get('scale', 1.0)
        
        # Create phase objects from loaded data
        phase_data = settings.get('phases', [])
        if phase_data:
            self.phases = []
            for phase_dict in phase_data:
                self.phases.append(PhaseSettings(
                    name=phase_dict.get('name', 'Phase'),
                    minutes=phase_dict.get('minutes', 30),
                    seconds=phase_dict.get('seconds', 0),
                    break_minutes=phase_dict.get('break_minutes', 5),
                    break_seconds=phase_dict.get('break_seconds', 0)
                ))
        else:
            # Default single phase if no phases found
            self.phases = [PhaseSettings()]
        
        # Set the current phase to the first one
        self.current_phase_index = 0
        self.phase_history = []
        self.in_break_mode = False

    def save_current_settings(self):
        """Save current settings to file"""
        settings = {
            'scale': self.current_scale,
            'phases': self.phases
        }
        
        # Save to file
        self.settings_manager.save_settings(settings)

    def apply_settings_changes(self, scale_factor, phases):
        """Apply changes from settings dialog"""
        # Apply size changes
        self.apply_size_change(scale_factor)
        
        # Update phases
        self.phases = phases
        
        # Reset the timer for the current phase
        self.reset_timer_for_current_phase()
        
        # Save settings to file
        self.save_current_settings()

    def apply_initial_scale(self):
        """Apply the loaded scale after UI elements are created"""
        if hasattr(self, 'current_scale') and self.current_scale != 1.0:
            self.apply_size_change(self.current_scale)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    timer_window = TimerWindow()
    
    # Example of updating gradient colors
    # timer_window.update_gradient_colors(QColor(0, 255, 128), QColor(128, 0, 255))
    
    timer_window.show()
    
    sys.exit(app.exec_())