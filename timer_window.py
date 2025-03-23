from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QFontDatabase, QColor

from settings_window import SettingsWindow, PhaseSettings
from notes_window import NotesWindow
from settings_manager import SettingsManager
from history_manager import HistoryManager
from task_name_dialog import TaskNameDialog
from gradient_icon_button import GradientIconButton
from gradient_label import GradientLabel
from platform_handler import PlatformHandler

class TimerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set window flags
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Initialize settings manager and history manager
        self.settings_manager = SettingsManager()
        self.history_manager = HistoryManager()
    
        # Load saved settings
        self.load_saved_settings()
        
        # Initialize timer variable (but don't start the timer yet)
        self.seconds = 0  # Will be set properly later
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)


        # Phases
        self.phase_cheated = [False] * 5

        # Add variable to track if task is active
        self.task_active = False
        self.current_task_name = ""
        
        # Initialize blinking variables for phase completion and initial state
        self.is_blinking = True  # Start in blinking state
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.toggle_blink_state)
        self.blink_state = False
        self.original_colors = (QColor(0, 255, 255), QColor(255, 0, 255))  # Store original gradient colors
        self.initial_state = True  # Track if this is initial app start
        
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

         # Update time display to show 00:00
        self.update_time_display()

        # Start in blinking green state
        self.start_blinking(initial=True)
        
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
        
        # Set up platform-specific topmost behavior
        self.topmost_timer = QTimer(self)
        self.topmost_timer.timeout.connect(self.ensure_topmost)
        self.topmost_timer.start(500)  # Check every 500ms
    
    def ensure_topmost(self):
        """Force window to stay on top using platform-specific handler"""
        PlatformHandler.ensure_window_topmost(self)
    
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
            self.ensure_topmost()

    def showEvent(self, event):
        super().showEvent(event)
        # Ensure topmost when first shown
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
            self.setWindowTitle(f"{phase.name}")

    def start_blinking(self, initial=False):
        """Start the timer blinking when phase is complete or at startup"""
        self.is_blinking = True
        self.blink_timer.start(750)  # Blink every 0.75 seconds
        self.initial_state = initial
        
        # Stop the main timer
        self.timer.stop()

    def toggle_blink_state(self):
        """Toggle the blinking state"""
        self.blink_state = not self.blink_state
        
        if self.initial_state:
            # Blinking green for new task
            if self.blink_state:
                # Change to green color scheme
                self.time_label.setGradientColors(QColor(0, 200, 0), QColor(100, 255, 100))
            else:
                # Change back to original color scheme
                self.time_label.setGradientColors(self.original_colors[0], self.original_colors[1])
        else:
            # Blinking red for phase completion
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
            self.initial_state = False
            
            # Restore original colors
            self.time_label.setGradientColors(self.original_colors[0], self.original_colors[1])

    def open_notes(self):
        """Open the notes window"""
        # If blinking, handle phase completion
        timer_completed = False
        if self.is_blinking:
            self.stop_blinking()
            timer_completed = True
            
            # Record the current phase status as completed legitimately
            if self.current_phase_index < len(self.phases):
                phase = self.phases[self.current_phase_index]
                phase_entry = {
                    'name': phase.name,
                    'status': 'Finished',
                    'cheated': self.phase_cheated[self.current_phase_index]
                }
                
                # Add to history if not already there
                if len(self.phase_history) <= self.current_phase_index:
                    self.phase_history.append(phase_entry)
                else:
                    self.phase_history[self.current_phase_index] = phase_entry
        else:
            # Phase timer not completed yet - this is considered cheating
            if self.current_phase_index < len(self.phases) and self.seconds > 0:
                # Mark this phase as cheated
                self.phase_cheated[self.current_phase_index] = True
        
        # Show notes window
        self.show_notes_window(timer_completed)

    def show_notes_window(self, timer_completed=False):
        """Show the notes window"""
        # Check if this is the last phase
        is_last_phase = (self.current_phase_index == len(self.phases) - 1)
        
        # Create and show notes window
        self.notes_dialog = NotesWindow(
            self, 
            current_phase=self.current_phase_index,
            is_last_phase=is_last_phase,
            timer_completed=timer_completed,
            history_manager=self.history_manager,
            task_active=self.task_active,
            current_task_name=self.current_task_name
        )
        
        # Connect signals
        self.notes_dialog.nextPhaseRequested.connect(self.go_to_next_phase)
        self.notes_dialog.taskCompletedRequested.connect(self.complete_task)
        self.notes_dialog.newTaskRequested.connect(self.start_new_task)
        
        # Show the dialog
        self.notes_dialog.show()

    def start_new_task(self):
        """Start a new task by showing the task name dialog"""
        self.task_name_dialog = TaskNameDialog(self)
        self.task_name_dialog.taskNameSubmitted.connect(self.initialize_task)
        self.task_name_dialog.show()

    def initialize_task(self, task_name):
        """Initialize a new task with the given name"""
        self.current_task_name = task_name
        self.task_active = True
        
        # Reset phase history and status
        self.phase_history = []
        self.current_phase_index = 0
        self.phase_cheated = [False] * 5
        
        # Stop blinking and start the timer
        self.stop_blinking()
        self.reset_timer_for_current_phase()
        self.timer.start(1000)
        
        # Update window title to show task name
        self.setWindowTitle(f"{task_name} - Phase 1")
        
        # Show confirmation message
        print(f"New task started: {task_name}")

    def complete_task(self):
        """Handle task completion"""
        try:
            # Make sure we have at least one entry in the phase history
            if not self.phase_history and self.current_phase_index < len(self.phases):
                # Create an entry for the current phase
                phase = self.phases[self.current_phase_index]
                phase_entry = {
                    'name': phase.name,
                    'status': 'Finished',
                    'cheated': False  # Completing via Complete Task button is NOT cheating
                }
                self.phase_history.append(phase_entry)
            
            # Determine if any phase was cheated using Next Phase button
            # (we only count "cheated" if it was marked that way from the Next Phase button)
            task_was_cheated = any(
                phase.get('cheated', False) 
                for phase in self.phase_history
            )
                
            # Save the task history to the daily history file with task status
            task_entry = {
                'phases': self.phase_history,
                'status': 'Completed with Cheating' if task_was_cheated else 'Completed Clean',
                'task_name': self.current_task_name  # Save the task name
            }
            
            # Debug print
            print(f"Completing task '{self.current_task_name}' with status: {task_entry['status']}")
            print(f"Phase history: {self.phase_history}")
            
            success = self.history_manager.save_daily_history(task_entry)
            print(f"History save result: {success}")
            
            # Reset for a new task
            self.current_phase_index = 0
            self.phase_history = []
            self.phase_cheated = [False] * 5
            
            # Set task as inactive
            self.task_active = False
            self.current_task_name = ""
            
            # Reset timer and start blinking green for new task
            self.reset_timer_for_current_phase()
            self.start_blinking(initial=True)
            
            # Show a temporary status message
            self.setWindowTitle(f"Task completed! Click Notes to start a new one")
            
            # Create a temporary timer to reset the window title
            reset_title_timer = QTimer(self)
            reset_title_timer.timeout.connect(lambda: self.setWindowTitle("Timer"))
            reset_title_timer.setSingleShot(True)
            reset_title_timer.start(3000)  # Reset title after 3 seconds
        except Exception as e:
            print(f"Error in complete_task: {e}")

    def go_to_next_phase(self):
        """Move to the next phase"""
        # If timer is still running, mark this as cheating
        if not self.is_blinking and self.seconds > 0:
            # The user clicked Next Phase before timer reached 00:00
            # This is considered cheating!
            self.phase_cheated[self.current_phase_index] = True
            
            # If we don't have an entry for this phase yet, create one
            if len(self.phase_history) <= self.current_phase_index:
                phase = self.phases[self.current_phase_index]
                phase_entry = {
                    'name': phase.name,
                    'status': 'Finished',
                    'cheated': True  # Mark as cheated
                }
                self.phase_history.append(phase_entry)
            else:
                # Update existing entry
                self.phase_history[self.current_phase_index]['cheated'] = True
        
        # Move to the next phase
        self.current_phase_index += 1
            
        # Check if we've completed all phases
        if self.current_phase_index >= len(self.phases):
            # Reset to first phase
            self.current_phase_index = 0
            # Reset the cheated status for a new cycle
            self.phase_cheated = [False] * 5
        
        # Reset the timer for the new phase
        self.reset_timer_for_current_phase()
        
        # Start the timer again
        self.timer.start(1000)
        
        # Stop blinking if it was blinking
        if self.is_blinking:
            self.stop_blinking()

    def update_time_display(self):
        """Update the timer display"""
        minutes = self.seconds // 60
        seconds = self.seconds % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.time_label.setText(time_str)
        
        # Show the current task name and phase name in the window title
        if self.task_active:
            phase = self.phases[self.current_phase_index]
            self.setWindowTitle(f"{self.current_task_name} - {phase.name}")

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
                    seconds=phase_dict.get('seconds', 0)
                ))
        else:
            # Default single phase if no phases found
            self.phases = [PhaseSettings()]
        
        # Set the current phase to the first one
        self.current_phase_index = 0
        self.phase_history = []

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