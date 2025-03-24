import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from timer_window import TimerWindow
from platform_handler import PlatformHandler, IS_WINDOWS, IS_MACOS, IS_LINUX

if __name__ == "__main__":
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Disable the context help button on dialogs (Windows-specific)
    if hasattr(Qt, 'AA_DisableWindowContextHelpButton'):
        QApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton)

    app = QApplication(sys.argv)
    
    # Platform-specific initialization
    if IS_WINDOWS:
        print("Running on Windows")
    elif IS_MACOS:
        print("Running on macOS")
    elif IS_LINUX:
        print("Running on Linux")
    else:
        print(f"Running on unknown platform")
    
    # Create and show the main timer window
    timer_window = TimerWindow()
    timer_window.show()
    
    # Start the application event loop
    sys.exit(app.exec_())