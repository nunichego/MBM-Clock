"""
Platform-specific functionality handler for the timer application.
This module abstracts OS-specific operations to make the application more portable.
"""
import platform
import sys

# Determine current platform
CURRENT_OS = platform.system().lower()
IS_WINDOWS = CURRENT_OS == 'windows'
IS_MACOS = CURRENT_OS == 'darwin'
IS_LINUX = CURRENT_OS == 'linux'

# Import platform-specific modules
if IS_WINDOWS:
    try:
        import win32gui
        import win32con
        WINDOWS_MODULES_AVAILABLE = True
    except ImportError:
        print("PyWin32 not found. Install with: pip install pywin32")
        WINDOWS_MODULES_AVAILABLE = False
else:
    WINDOWS_MODULES_AVAILABLE = False

class PlatformHandler:
    """Handler for platform-specific functionality"""
    
    @staticmethod
    def ensure_window_topmost(window):
        """Ensure the window stays on top of other windows
        
        Args:
            window: The window object to make topmost
        """
        if IS_WINDOWS and WINDOWS_MODULES_AVAILABLE:
            # Windows implementation using win32gui
            hwnd = int(window.winId())
            win32gui.SetWindowPos(
                hwnd, 
                win32con.HWND_TOPMOST, 
                0, 0, 0, 0, 
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
            )
        elif IS_MACOS:
            # macOS implementation
            # Note: Qt's WindowStaysOnTopHint flag is usually sufficient for macOS
            # but additional specific implementations could be added here if needed
            pass
        elif IS_LINUX:
            # Linux implementation
            # Note: Similar to macOS, Qt's flags usually work, but specific window
            # manager interactions could be added here if needed
            pass
    
    @staticmethod
    def set_window_attributes(window):
        """Apply platform-specific window attributes
        
        Args:
            window: The window object to configure
        """
        # This method can be expanded with platform-specific window configurations
        # such as transparency, rounded corners, etc.
        if IS_MACOS:
            # macOS specific window attributes
            pass
        elif IS_WINDOWS:
            # Windows specific window attributes
            pass
        elif IS_LINUX:
            # Linux specific window attributes
            pass
    
    @staticmethod
    def get_resources_path():
        """Get the appropriate path for resources based on platform
        
        Returns:
            str: Path to resources directory
        """
        # Get base directory
        if getattr(sys, 'frozen', False):
            # Running in a bundled executable
            base_dir = sys._MEIPASS
        else:
            # Running in a normal Python environment
            base_dir = sys.path[0]
        
        # Platform-specific resource path handling
        if IS_MACOS and getattr(sys, 'frozen', False):
            # macOS app bundles have a specific resource structure
            return os.path.join(os.path.dirname(base_dir), 'Resources')
        else:
            # Default resources path
            return os.path.join(base_dir, 'resources')