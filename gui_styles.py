# gui_styles.py - Global UI Styling and Aesthetics

def get_main_stylesheet():
    """Returns the primary Dark Mode CSS-like stylesheet for the entire application."""
    return """
    QMainWindow {
        background-color: #121212;
    }
    
    QFrame#Sidebar {
        background-color: #1e1e1e;
        border-right: 1px solid #333;
        min-width: 200px;
        max-width: 200px;
    }
    
    QLabel#SidebarTitle {
        color: #00adb5;
        font-size: 18px;
        font-weight: bold;
        padding: 20px 10px;
        margin-bottom: 10px;
    }
    
    QPushButton[class="NavButton"] {
        background-color: transparent;
        color: #b0b0b0;
        border: none;
        padding: 12px 20px;
        text-align: left;
        font-size: 14px;
        border-radius: 5px;
        margin: 2px 10px;
    }
    
    QPushButton[class="NavButton"]:hover {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    
    QPushButton[class="NavButton"]:checked {
        background-color: #00adb5;
        color: #ffffff;
        font-weight: bold;
    }
    
    QStackedWidget {
        background-color: #121212;
    }
    
    QWidget#PageContent {
        background-color: #121212;
        padding: 20px;
    }
    
    QLabel[class="HeaderLabel"] {
        color: #ffffff;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    QLabel[class="SectionLabel"] {
        color: #00adb5;
        font-size: 14px;
        font-weight: bold;
        margin-top: 10px;
    }
    
    QLineEdit {
        background-color: #252525;
        color: #ffffff;
        border: 1px solid #333;
        padding: 8px;
        border-radius: 4px;
        selection-background-color: #00adb5;
    }
    
    QLineEdit:focus {
        border: 1px solid #00adb5;
    }
    
    QComboBox {
        background-color: #252525;
        color: #ffffff;
        border: 1px solid #333;
        padding: 8px;
        border-radius: 4px;
    }
    
    QComboBox::drop-down {
        border: none;
    }
    
    QProgressBar {
        border: 1px solid #333;
        border-radius: 5px;
        text-align: center;
        color: #ffffff;
        background-color: #252525;
        height: 20px;
    }
    
    QProgressBar::chunk {
        background-color: #00adb5;
        border-radius: 4px;
    }
    
    QTableWidget {
        background-color: #1e1e1e;
        color: #ffffff;
        gridline-color: #333;
        border: 1px solid #333;
        selection-background-color: #2d2d2d;
    }
    
    QHeaderView::section {
        background-color: #252525;
        color: #b0b0b0;
        padding: 5px;
        border: 1px solid #333;
    }
    
    QPushButton#ActionBtn {
        background-color: #00adb5;
        color: #ffffff;
        border: none;
        padding: 10px 20px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    QPushButton#ActionBtn:hover {
        background-color: #00cfd8;
    }
    
    QPushButton#ActionBtn:disabled {
        background-color: #444;
        color: #888;
    }

    QLabel#GreetingLabel {
        color: #666;
        font-size: 11px;
        margin-bottom: 15px;
        padding: 0 10px;
        font-style: italic;
    }

    QLabel#ThumbnailPreview {
        border: 1px solid #333;
        background-color: #000;
        border-radius: 4px;
    }
    
    QScrollArea {
        border: none;
        background-color: transparent;
    }
    
    QScrollBar:vertical {
        border: none;
        background: #1e1e1e;
        width: 10px;
        margin: 0px;
    }
    
    QScrollBar::handle:vertical {
        background: #333;
        min-height: 20px;
        border-radius: 5px;
    }
    
    QScrollBar::handle:vertical:hover {
        background: #444;
    }
    
    QCheckBox {
        color: #ffffff;
        spacing: 5px;
    }
    """

def get_light_stylesheet():
    """Returns a Light Mode CSS-like stylesheet."""
    return """
    QMainWindow {
        background-color: #f5f5f5;
    }
    
    QFrame#Sidebar {
        background-color: #ffffff;
        border-right: 1px solid #ddd;
        min-width: 200px;
        max-width: 200px;
    }
    
    QLabel#SidebarTitle {
        color: #00adb5;
        font-size: 18px;
        font-weight: bold;
        padding: 20px 10px;
        margin-bottom: 10px;
    }
    
    QPushButton[class="NavButton"] {
        background-color: transparent;
        color: #555555;
        border: none;
        padding: 12px 20px;
        text-align: left;
        font-size: 14px;
        border-radius: 5px;
        margin: 2px 10px;
    }
    
    QPushButton[class="NavButton"]:hover {
        background-color: #eeeeee;
        color: #000000;
    }
    
    QPushButton[class="NavButton"]:checked {
        background-color: #00adb5;
        color: #ffffff;
        font-weight: bold;
    }
    
    QStackedWidget {
        background-color: #f5f5f5;
    }
    
    QWidget#PageContent {
        background-color: #f5f5f5;
        padding: 20px;
    }
    
    QLabel[class="HeaderLabel"] {
        color: #222222;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    QLabel[class="SectionLabel"] {
        color: #00adb5;
        font-size: 14px;
        font-weight: bold;
        margin-top: 10px;
    }
    
    QLineEdit {
        background-color: #ffffff;
        color: #222222;
        border: 1px solid #ccc;
        padding: 8px;
        border-radius: 4px;
        selection-background-color: #00adb5;
    }
    
    QLineEdit:focus {
        border: 1px solid #00adb5;
    }
    
    QComboBox {
        background-color: #ffffff;
        color: #222222;
        border: 1px solid #ccc;
        padding: 8px;
        border-radius: 4px;
    }
    
    QProgressBar {
        border: 1px solid #ccc;
        border-radius: 5px;
        text-align: center;
        color: #222222;
        background-color: #ffffff;
        height: 20px;
    }
    
    QProgressBar::chunk {
        background-color: #00adb5;
        border-radius: 4px;
    }
    
    QTableWidget {
        background-color: #ffffff;
        color: #222222;
        gridline-color: #ddd;
        border: 1px solid #ccc;
        selection-background-color: #eeeeee;
    }
    
    QHeaderView::section {
        background-color: #f9f9f9;
        color: #555555;
        padding: 5px;
        border: 1px solid #ccc;
    }
    
    QPushButton#ActionBtn {
        background-color: #00adb5;
        color: #ffffff;
        border: none;
        padding: 10px 20px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    QCheckBox {
        color: #222222;
        spacing: 5px;
    }
    """
