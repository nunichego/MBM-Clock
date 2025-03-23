from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QFrame, QListWidget, QListWidgetItem,
                           QApplication, QDateEdit, QWidget, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtGui import QFont, QColor
import datetime

class NotesWindow(QDialog):
    # Signal to emit when the user wants to proceed to the next phase
    nextPhaseRequested = pyqtSignal()
    # Signal for task completion
    taskCompletedRequested = pyqtSignal()
    # Signal for new task
    newTaskRequested = pyqtSignal()
    
    def __init__(self, parent=None, current_phase=0, is_last_phase=False, timer_completed=False, 
                 history_manager=None, task_active=False, current_task_name=""):
        super().__init__(parent)
        # Remove default window frame and set always on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Initialize phase history and current phase
        self.current_phase = current_phase
        self.is_last_phase = is_last_phase
        self.timer_completed = timer_completed
        self.history_manager = history_manager
        self.task_active = task_active
        self.current_task_name = current_task_name
        
        # Initialize dragPos for mouse events
        self.dragPos = None
        
        # Apply dark theme stylesheet
        self.apply_dark_stylesheet()
        
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
    
    def apply_dark_stylesheet(self):
        """Apply a modern minimalist theme"""
        self.setStyleSheet("""
            QDialog {
                background-color: transparent;
            }
            QFrame#notesContainer {
                background-color: rgb(40, 40, 40);
                border-radius: 15px;
                border: none;
            }
            QLabel {
                color: rgb(240, 240, 240);
                background-color: transparent;
                border: none;
            }
            QListWidget {
                background-color: rgb(50, 50, 50);
                border-radius: 8px;
                color: white;
                padding: 8px;
                border: none;
                selection-background-color: rgb(60, 60, 60);
            }
            QListWidget::item {
                padding: 4px;
                border-bottom: 1px solid rgb(70, 70, 70);
            }
            QListWidget::item:selected {
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
            QPushButton:disabled {
                background-color: rgb(45, 45, 45);
                color: rgb(130, 130, 130);
            }
            QPushButton#nextPhaseButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                        stop:0 rgb(0, 150, 200), 
                                        stop:1 rgb(120, 0, 170));
                color: white;
            }
            QPushButton#nextPhaseButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                        stop:0 rgb(0, 170, 220), 
                                        stop:1 rgb(140, 0, 190));
            }
            QPushButton#completeTaskButton {
                background-color: rgb(40, 120, 40);
                color: white;
            }
            QPushButton#completeTaskButton:hover {
                background-color: rgb(45, 135, 45);
            }
            QPushButton#newTaskButton {
                background-color: rgb(60, 105, 160);
                color: white;
            }
            QPushButton#newTaskButton:hover {
                background-color: rgb(65, 115, 175);
            }
            QDateEdit {
                background-color: rgb(55, 55, 55);
                color: white;
                border-radius: 8px;
                padding: 6px;
                border: none;
            }
        """)
    
    def setup_ui(self):
        # Initialize fonts
        self.setup_fonts()
        
        # Main layout with margins for shadow effect
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Create a frame with rounded corners
        container = QFrame(self)
        container.setObjectName("notesContainer")
        container.setGraphicsEffect(self.create_shadow_effect())
        
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(20)
        
        # Current phase/task info
        phase_info_layout = QHBoxLayout()
        
        # Create different UI based on whether a task is active
        if self.task_active:
            # Show current task name and phase
            task_label = QLabel(f"Current Task: {self.current_task_name}")
            task_label.setFont(self.bold_font)
            phase_info_layout.addWidget(task_label)
            
            # Current phase label
            current_phase_label = QLabel(f"Phase: {self.current_phase + 1}")
            current_phase_label.setFont(self.regular_font)
            phase_info_layout.addWidget(current_phase_label)
            
            # Status label
            status_label = QLabel()
            if self.timer_completed:
                status_label.setText("Status: Phase Complete")
                status_label.setStyleSheet("color: #64FF64;")
            else:
                status_label.setText("Status: Phase Running")
            status_label.setFont(self.regular_font)
            
            phase_info_layout.addStretch()
            phase_info_layout.addWidget(status_label)
        else:
            # No active task
            task_label = QLabel("No Active Task")
            task_label.setFont(self.bold_font)
            phase_info_layout.addWidget(task_label)
        
        container_layout.addLayout(phase_info_layout)
        
        # Title for task history
        title_label = QLabel("Tasks:")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(self.title_font)
        container_layout.addWidget(title_label)
        
        # Date selector
        date_layout = QHBoxLayout()
        
        date_label = QLabel("Date:")
        date_label.setFont(self.regular_font)
        
        today = datetime.date.today()
        self.date_selector = QDateEdit()
        self.date_selector.setDate(QDate(today.year, today.month, today.day))
        self.date_selector.setCalendarPopup(True)
        self.date_selector.dateChanged.connect(self.date_changed)
        
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_selector)
        date_layout.addStretch()
        
        container_layout.addLayout(date_layout)
        
        # Tasks list
        tasks_label = QLabel("Completed Tasks:")
        tasks_label.setFont(self.regular_font)
        container_layout.addWidget(tasks_label)
        
        self.tasks_list = QListWidget()
        container_layout.addWidget(self.tasks_list)
        
        # Task details list
        task_details_label = QLabel("Task Details:")
        task_details_label.setFont(self.regular_font)
        container_layout.addWidget(task_details_label)
        
        self.task_details_list = QListWidget()
        container_layout.addWidget(self.task_details_list)
        
        # Connect task selection
        self.tasks_list.currentRowChanged.connect(self.task_selected)
        
        # Load today's task history
        self.load_current_date_history()
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Create the appropriate action button based on state
        if not self.task_active:
            # New Task button (when no task is active)
            self.action_button = QPushButton("New Task")
            self.action_button.setObjectName("newTaskButton")
            self.action_button.clicked.connect(self.request_new_task)
        else:
            # Complete Task button (when a task is active)
            self.action_button = QPushButton("Complete Task")
            self.action_button.setObjectName("completeTaskButton")
            self.action_button.clicked.connect(self.request_task_completion)
        
        # Set font for action button
        self.action_button.setFont(self.bold_font)
        
        # Next Phase button
        self.next_phase_button = QPushButton("Next Phase")
        self.next_phase_button.setObjectName("nextPhaseButton")
        self.next_phase_button.setFont(self.bold_font)
        
        # Disable Next Phase button if:
        # - No task is active, or
        # - We're on the last phase and timer is completed
        if not self.task_active or (self.is_last_phase and self.timer_completed):
            self.next_phase_button.setEnabled(False)
            if not self.task_active:
                self.next_phase_button.setToolTip("Start a task first")
            else:
                self.next_phase_button.setToolTip("You're on the last phase. Complete the task instead.")
        
        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.setFont(self.regular_font)
        
        # Add all buttons
        buttons_layout.addWidget(self.action_button)
        buttons_layout.addWidget(self.next_phase_button)
        buttons_layout.addWidget(self.close_button)
        
        container_layout.addLayout(buttons_layout)
        main_layout.addWidget(container)
        
        # Connect remaining buttons
        self.next_phase_button.clicked.connect(self.request_next_phase)
        self.close_button.clicked.connect(self.reject)
        
        # Set size for dialog
        self.setMinimumSize(500, 600)
    
    def load_current_date_history(self):
        """Load history for the currently selected date"""
        # Skip if no history manager
        if not self.history_manager:
            return
            
        # Clear the lists
        self.tasks_list.clear()
        self.task_details_list.clear()
        
        # Get the selected date
        qdate = self.date_selector.date()
        date_str = f"{qdate.year()}-{qdate.month():02d}-{qdate.day():02d}"
        
        # Load history for this date
        history = self.history_manager.load_daily_history(date_str)
        
        # Add tasks to the list
        for i, task in enumerate(history):
            timestamp = task.get('timestamp', 'Unknown time')
            phases = task.get('phases', [])
            status = task.get('status', 'Completed')
            task_name = task.get('task_name', f"Task {i+1}")
            
            # Create item with task name and status
            item = QListWidgetItem(f"{task_name} - {timestamp} - {status}")
            
            # Color based on status
            if status == 'Completed Clean':
                item.setForeground(QColor(100, 255, 100))  # Green
            elif status == 'Completed with Cheating':
                item.setForeground(QColor(255, 165, 0))    # Orange
            
            self.tasks_list.addItem(item)
    
    def date_changed(self, qdate):
        """Handle date selection change"""
        self.load_current_date_history()
    
    def task_selected(self, row):
        """Handle task selection"""
        if row < 0 or not self.history_manager:
            return
            
        # Clear details list
        self.task_details_list.clear()
        
        # Get the selected date
        qdate = self.date_selector.date()
        date_str = f"{qdate.year()}-{qdate.month():02d}-{qdate.day():02d}"
        
        # Load history for this date
        history = self.history_manager.load_daily_history(date_str)
        
        # Make sure row is valid
        if 0 <= row < len(history):
            task = history[row]
            phases = task.get('phases', [])
            task_status = task.get('status', 'Completed')
            task_name = task.get('task_name', f"Task {row+1}")
            
            # Add task name and status as the first items
            name_item = QListWidgetItem(f"Task Name: {task_name}")
            name_item.setForeground(QColor(255, 255, 255))  # White
            self.task_details_list.addItem(name_item)
            
            status_item = QListWidgetItem(f"Status: {task_status}")
            if task_status == 'Completed Clean':
                status_item.setForeground(QColor(100, 255, 100))  # Green
            elif task_status == 'Completed with Cheating':
                status_item.setForeground(QColor(255, 165, 0))    # Orange
            self.task_details_list.addItem(status_item)
            
            # Add separator
            self.task_details_list.addItem("------ Phase Details ------")
            
            # Add phase details
            for i, phase in enumerate(phases):
                name = phase.get('name', f"Phase {i+1}")
                status = phase.get('status', 'Unknown')
                
                # Create status text
                status_text = status
                if phase.get('cheated', False):
                    status_text += " (Cheated)"
                
                item = QListWidgetItem(f"Phase {i+1}: {name} - {status_text}")
                
                # Set color based on status
                if status == 'Finished':
                    if phase.get('cheated', False):
                        item.setForeground(QColor(255, 165, 0))  # Orange for cheated
                    else:
                        item.setForeground(QColor(100, 255, 100))  # Green for legitimate finish
                elif status == 'Failed':
                    item.setForeground(QColor(255, 100, 100))  # Red
                
                self.task_details_list.addItem(item)
    
    def request_next_phase(self):
        """Emit signal to request moving to the next phase"""
        self.nextPhaseRequested.emit()
        self.accept()
    
    def request_task_completion(self):
        """Emit signal to request completing the entire task"""
        self.taskCompletedRequested.emit()
        self.accept()
    
    def request_new_task(self):
        """Emit signal to request starting a new task"""
        self.newTaskRequested.emit()
        self.accept()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.dragPos is not None:
            self.move(event.globalPos() - self.dragPos)
            event.accept()