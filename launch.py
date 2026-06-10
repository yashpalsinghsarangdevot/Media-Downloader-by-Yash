# launch.py - Application Entry Point and Environment Setup

import sys
import os
from PyQt6.QtWidgets import QApplication
from app_interface import MediaDownloaderApp

def setup_environment():
    """
    Hard-coded os.environ["PATH"] injection at boot to force-append 
    the root project directory. This ensures worker threads never lose 
    visibility of local ffmpeg.exe, ffprobe.exe, or deno.exe binaries.
    """
    # Get the absolute path of the directory containing launch.py
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Append to PATH
    if project_root not in os.environ["PATH"]:
        os.environ["PATH"] = project_root + os.pathsep + os.environ["PATH"]
        
    # Optional: Print for debugging (uncomment if needed)
    # print(f"Environment Path Updated: {os.environ['PATH']}")

def main():
    # 1. Initialize environment
    setup_environment()
    
    # 2. Create high-DPI aware application
    app = QApplication(sys.argv)
    app.setApplicationName("Media Downloader by Yash")
    
    # 3. Launch the main interface
    window = MediaDownloaderApp()
    window.show()
    
    # 4. Execute application loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
