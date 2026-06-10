# app_interface.py - Main User Interface and Logic Orchestration

import os
import sys
import urllib.request
import json

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, 
    QPushButton, QStackedWidget, QLabel, QLineEdit, QComboBox,
    QProgressBar, QScrollArea, QFileDialog, QMessageBox, QTableWidget,
    QTableWidgetItem, QCheckBox, QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QPixmap, QImage, QIcon, QColor
from gui_styles import get_main_stylesheet
from core_engine import DownloadThread, InfoFetcherThread

class MediaDownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Downloader by Yash")
        
        logo_path = resource_path("assets/logo.png")
        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))

        self.setMinimumSize(1100, 700)
        self.setStyleSheet(get_main_stylesheet())
        
        self.is_pipeline_running = False
        self.current_worker = None
        self.info_fetcher = None
        
        self.current_video_formats = []
        self.current_audio_formats = []
        
        self.history_file = os.path.join(os.path.expanduser("~"), ".media_downloader_history_v2.json")
        self.download_history = []

        self.init_ui()
        self.load_history()

    def init_ui(self):
        """Creates the modern sidenav sidebar workspace."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Sidebar ---
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        logo_path = resource_path("assets/logo.png")
        if os.path.exists(logo_path):
            logo_label = QLabel()
            logo_label.setPixmap(QPixmap(logo_path).scaled(180, 180, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo_label.setStyleSheet("margin-top: 15px;")
            sidebar_layout.addWidget(logo_label)

        title_label = QLabel("Media Download\nby Yash")
        title_label.setObjectName("SidebarTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #00adb5; font-size: 16px; font-weight: bold; padding: 10px 0; line-height: 1.8;")
        sidebar_layout.addWidget(title_label)

        self.nav_buttons = []
        # Removed Control Panel
        nav_items = [
            ("Link Analyzer", 0),
            ("Finished Clips", 1),
            ("User Manual", 2)
        ]

        for text, index in nav_items:
            btn = QPushButton(text)
            btn.setProperty("index", index)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.setProperty("class", "NavButton")
            btn.clicked.connect(self.switch_page)
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)
        
        self.nav_buttons[0].setChecked(True)
        sidebar_layout.addStretch()

        gh_btn = QPushButton(" GitHub")
        gh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        gh_path = resource_path("assets/github.png")
        if os.path.exists(gh_path):
            gh_btn.setIcon(QIcon(gh_path))
        gh_btn.setStyleSheet("background: #24292e; color: white; border-radius: 3px; font-size: 10px; padding: 5px;")
        gh_btn.clicked.connect(lambda: os.startfile("https://github.com/yashpalsinghsarangdevot"))

        insta_btn = QPushButton(" Instagram")
        insta_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        insta_path = resource_path("assets/instagram.webp")
        if os.path.exists(insta_path):
            insta_btn.setIcon(QIcon(insta_path))
        insta_btn.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f09433, stop:0.25 #e6683c, stop:0.5 #dc2743, stop:0.75 #cc2366, stop:1 #bc1888); color: white; border-radius: 3px; font-size: 10px; padding: 5px;")
        insta_btn.clicked.connect(lambda: os.startfile("https://instagram.com/yashhpalsingh_sarangdevot"))
        
        social_layout = QHBoxLayout()
        social_layout.addWidget(gh_btn)
        social_layout.addWidget(insta_btn)
        sidebar_layout.addLayout(social_layout)

        # Support Button Restored
        support_btn = QPushButton("☕ Support My Work")
        support_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        support_btn.setStyleSheet("color: #00adb5; border: 1px solid #00adb5; border-radius: 3px; font-size: 11px; margin: 5px 10px; padding: 5px;")
        support_btn.clicked.connect(lambda: QMessageBox.information(self, "Support", "Thank you for your interest! You can reach out via Instagram or GitHub for support details."))
        sidebar_layout.addWidget(support_btn)

        # Footer Greeting with Design
        greeting_label = QLabel("Thank you for using Media Downloader by Yash\nCreated by Yashpal Singh")
        greeting_label.setObjectName("GreetingLabel")
        greeting_label.setWordWrap(True)
        greeting_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        greeting_label.setStyleSheet("color: #666; font-size: 10px; margin-bottom: 15px; padding: 0 10px; font-style: italic;")
        sidebar_layout.addWidget(greeting_label)

        main_layout.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        self.page_link_analyzer = self.create_analyzer_page()
        self.page_finished = self.create_finished_page()
        self.page_manual = self.create_manual_page()

        self.stack.addWidget(self.page_link_analyzer)
        self.stack.addWidget(self.page_finished)
        self.stack.addWidget(self.page_manual)
        main_layout.addWidget(self.stack)

    def switch_page(self, arg=None):
        if type(arg) is int:
            self.stack.setCurrentIndex(arg)
            if 0 <= arg < len(self.nav_buttons):
                self.nav_buttons[arg].setChecked(True)
        else:
            btn = self.sender()
            if btn:
                target_index = btn.property("index")
                if target_index is not None:
                    self.stack.setCurrentIndex(target_index)

    def create_analyzer_page(self):
        page = QWidget()
        page.setObjectName("PageContent")
        layout = QVBoxLayout(page)
        h_label = QLabel("Link Analyzer")
        h_label.setProperty("class", "HeaderLabel")
        layout.addWidget(h_label)
        
        url_h_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste link here...")
        self.analyze_btn = QPushButton("ANALYZE LINK")
        self.analyze_btn.setObjectName("ActionBtn")
        self.analyze_btn.setFixedWidth(150)
        self.analyze_btn.clicked.connect(self.fetch_metadata)
        url_h_layout.addWidget(self.url_input)
        url_h_layout.addWidget(self.analyze_btn)
        layout.addLayout(url_h_layout)

        meta_layout = QHBoxLayout()
        self.thumb_label = QLabel("Preview Thumbnail")
        self.thumb_label.setFixedSize(320, 180)
        self.thumb_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumb_label.setStyleSheet("border: 2px dashed #333; background: #0a0a0a;")
        meta_layout.addWidget(self.thumb_label)
        
        info_v_layout = QVBoxLayout()
        title_label = QLabel("File Title:")
        title_label.setProperty("class", "SectionLabel")
        info_v_layout.addWidget(title_label)
        self.title_input = QLineEdit()
        info_v_layout.addWidget(self.title_input)

        cat_label = QLabel("Extraction Category:")
        cat_label.setProperty("class", "SectionLabel")
        info_v_layout.addWidget(cat_label)
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Video", "Audio Only", "Video-Only (No Sound)"])
        self.category_combo.currentIndexChanged.connect(self.update_quality_options)
        info_v_layout.addWidget(self.category_combo)
        
        quality_label = QLabel("Preferred Quality:")
        quality_label.setProperty("class", "SectionLabel")
        info_v_layout.addWidget(quality_label)
        self.quality_combo = QComboBox()
        info_v_layout.addWidget(self.quality_combo)
        meta_layout.addLayout(info_v_layout)
        layout.addLayout(meta_layout)

        trim_layout = QHBoxLayout()
        self.trim_checkbox = QCheckBox("Enable Trimming")
        self.start_time_input = QLineEdit(); self.start_time_input.setPlaceholderText("Start HH:MM:SS")
        self.end_time_input = QLineEdit(); self.end_time_input.setPlaceholderText("End HH:MM:SS")
        trim_layout.addWidget(self.trim_checkbox)
        trim_layout.addWidget(self.start_time_input)
        trim_layout.addWidget(self.end_time_input)
        layout.addLayout(trim_layout)

        dir_layout = QHBoxLayout()
        self.dir_input = QLineEdit(os.path.join(os.path.expanduser("~"), "Downloads"))
        self.browse_btn = QPushButton("Browse"); self.browse_btn.clicked.connect(self.browse_directory)
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(self.browse_btn)
        layout.addLayout(dir_layout)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        self.status_label = QLabel("Ready...")
        self.status_label.setStyleSheet("color: #ffffff;")
        layout.addWidget(self.status_label)

        layout.addStretch()
        self.run_btn = QPushButton("DOWNLOAD NOW")
        self.run_btn.setObjectName("ActionBtn")
        self.run_btn.clicked.connect(self.start_download)
        layout.addWidget(self.run_btn)
        return page

    def create_finished_page(self):
        page = QWidget()
        page.setObjectName("PageContent")
        layout = QVBoxLayout(page)
        h_label = QLabel("Finished Clips & History")
        h_label.setProperty("class", "HeaderLabel")
        layout.addWidget(h_label)
        
        # S.No column removed as requested
        self.finished_table = QTableWidget(0, 5)
        self.finished_table.verticalHeader().setVisible(False)
        
        self.finished_table.setHorizontalHeaderLabels(["File Name", "Category", "Status", "Save Path", "Actions"])
        
        # Lock interactions
        self.finished_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.finished_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.finished_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        
        header = self.finished_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        
        # Column widths adjusted for readability without S.No
        self.finished_table.setColumnWidth(0, 450) # File Name 
        self.finished_table.setColumnWidth(1, 100) # Category 
        self.finished_table.setColumnWidth(2, 100) # Status
        self.finished_table.setColumnWidth(3, 200) # Save Path 
        self.finished_table.setColumnWidth(4, 120) # Actions
        
        layout.addWidget(self.finished_table)
        clear_btn = QPushButton("Clear History")
        clear_btn.setStyleSheet("background: #ff4d4d; color: white; padding: 5px;")
        clear_btn.clicked.connect(self.clear_history)
        layout.addWidget(clear_btn, alignment=Qt.AlignmentFlag.AlignRight)
        return page

    def create_manual_page(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content.setObjectName("PageContent")
        layout = QVBoxLayout(content)
        
        h_label = QLabel("How to Use - Detailed Guide")
        h_label.setProperty("class", "HeaderLabel")
        layout.addWidget(h_label)
        
        manual_text = (
            "<h3 style='color: #00adb5; margin-top: 0;'>1. Link Analysis</h3>"
            "<p style='color: #ffffff;'>Paste your link (YouTube, Instagram, etc.) into the <b>Media URL</b> box and click <b>ANALYZE LINK</b>. The app will fetch the thumbnail, duration, and available qualities.</p>"
                
            "<h3 style='color: #00adb5;'>2. Quality & Type</h3>"
            "<p style='color: #ffffff;'>Once analyzed, select your desired resolution (like <b>2160p/4K</b>) from the dropdown. Then, choose your category:<br>"
            "&nbsp;&bull; <b>Video:</b> Full clip with sound.<br>"
            "&nbsp;&bull; <b>Audio Only:</b> Music as a high-quality MP3.<br>"
            "&nbsp;&bull; <b>Video-Only:</b> High-res visual without sound.</p>"
                
            "<h3 style='color: #00adb5;'>3. Precision Trimming</h3>"
            "<p style='color: #ffffff;'>Check <b>Enable Trimming</b> if you only want a specific part. Enter the <b>Start</b> and <b>End</b> times in HH:MM:SS format (e.g., 00:01:30).</p>"
   
            "<h3 style='color: #00adb5;'>4. Fast Extraction</h3>"
            "<p style='color: #ffffff;'>Set your <b>Save Path</b> and click <b>DOWNLOAD NOW</b>. The progress bar and speed indicator will show live updates at the bottom of the analyzer page.</p>"
                
            "<h3 style='color: #00adb5;'>5. Tracking History</h3>"
            "<p style='color: #ffffff;'>Go to <b>Finished Clips</b> to view all past downloads. Hover over long names to see full details, or use the <b>Retry / Load</b> button to instantly reload a past link for a new download.</p>"
        )
        text_label = QLabel(manual_text)
        text_label.setWordWrap(True)
        text_label.setStyleSheet("color: #ffffff; font-size: 16px; line-height: 1.4;")
        layout.addWidget(text_label)
        
        layout.addStretch()
        scroll.setWidget(content)
        return scroll

    def browse_directory(self):
        p = QFileDialog.getExistingDirectory(self, "Select Save Folder")
        if p: self.dir_input.setText(p)

    def fetch_metadata(self):
        u = self.url_input.text().strip()
        if u:
            self.analyze_btn.setEnabled(False); self.analyze_btn.setText("Analyzing...")
            self.info_fetcher = InfoFetcherThread(u)
            self.info_fetcher.info_signal.connect(self.on_metadata_fetched)
            self.info_fetcher.error_signal.connect(self.on_metadata_error)
            self.info_fetcher.start()

    @pyqtSlot(dict)
    def on_metadata_fetched(self, d):
        self.analyze_btn.setEnabled(True); self.analyze_btn.setText("ANALYZE LINK")
        self.title_input.setText(d['title'])
        self.start_time_input.setText("00:00:00")
        self.end_time_input.setText(d['duration_str'])
        self.current_video_formats = d.get('video_formats', []); self.current_audio_formats = d.get('audio_formats', [])
        self.update_quality_options()
        if d.get('thumbnail_data'):
            img = QImage(); img.loadFromData(d['thumbnail_data'])
            self.thumb_label.setPixmap(QPixmap.fromImage(img).scaled(320, 180, Qt.AspectRatioMode.KeepAspectRatio))

    def update_quality_options(self):
        cat = self.category_combo.currentText(); self.quality_combo.clear()
        fmts = self.current_audio_formats if "Audio" in cat else self.current_video_formats
        for f in fmts:
            lbl = f"{f['abr']}kbps" if "Audio" in cat else f"{f['height']}p"
            self.quality_combo.addItem(f"{lbl} ({f['ext']})", f['format_id'])

    @pyqtSlot(str)
    def on_metadata_error(self, e):
        self.analyze_btn.setEnabled(True); QMessageBox.warning(self, "Error", e)

    def start_download(self):
        u = self.url_input.text().strip()
        if not u: return
        self.current_task = {
            'url': u, 'save_path': self.dir_input.text(), 'title': self.title_input.text().strip(),
            'category': self.category_combo.currentText(), 'trim_enabled': self.trim_checkbox.isChecked(),
            'start_time': self.start_time_input.text(), 'end_time': self.end_time_input.text(),
            'format_id': self.quality_combo.currentData()
        }
        self.run_btn.setEnabled(False); self.progress_bar.setVisible(True)
        self.current_worker = DownloadThread(self.current_task)
        self.current_worker.progress_signal.connect(self.update_progress)
        self.current_worker.finished_signal.connect(self.on_download_finished)
        self.current_worker.start()

    @pyqtSlot(dict)
    def update_progress(self, d):
        self.progress_bar.setValue(int(d['percent']))
        self.status_label.setText(f"<font color='white'>Speed: {d['speed']} | ETA: {d['eta']}</font>")

    @pyqtSlot(bool, str)
    def on_download_finished(self, s, msg):
        self.run_btn.setEnabled(True); self.progress_bar.setVisible(False)
        status = "Finished" if s else "Failed"
        self.add_to_history(self.current_task['title'], self.current_task['category'], status, self.current_task['save_path'], self.current_task['url'])
        QMessageBox.information(self, "Result", msg)

    def add_to_history(self, t, c, s, p, u):
        self.download_history.append({'title': t, 'category': c, 'status': s, 'path': p, 'url': u})
        self.save_history(); self.refresh_history_table()

    def refresh_history_table(self):
        self.finished_table.setRowCount(0)
        for i, e in enumerate(reversed(self.download_history)):
            row = self.finished_table.rowCount(); self.finished_table.insertRow(row)
            # S.No logic removed. Populating directly from col 0
            for col, val in enumerate([e['title'], e['category'], e['status'], e['path']]):
                item = QTableWidgetItem(str(val))
                item.setToolTip(str(val))
                self.finished_table.setItem(row, col, item)
            btn = QPushButton("Retry / Load"); btn.clicked.connect(lambda _, u=e['url']: self.retry_download(u))
            self.finished_table.setCellWidget(row, 4, btn)

    def retry_download(self, u): self.url_input.setText(u); self.switch_page(0); self.fetch_metadata()
    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f: self.download_history = json.load(f)
                self.refresh_history_table()
            except: pass
    def save_history(self):
        try:
            with open(self.history_file, 'w') as f: json.dump(self.download_history, f)
        except: pass
    def clear_history(self): self.download_history = []; self.save_history(); self.refresh_history_table()
