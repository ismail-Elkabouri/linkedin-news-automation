#!/usr/bin/env python3
# gui_terminal.py - LinkedIn AI News Desktop Application (Terminal/CMD Style)

import sys
from datetime import datetime
from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QListWidget, QListWidgetItem,
    QProgressBar, QMessageBox, QFrame, QStackedWidget, QLineEdit,
    QScrollArea, QCheckBox, QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QFontDatabase, QPalette, QIcon
import html

try:
    from news_fetcher import fetch_latest_news, rank_and_sort_news
    from post_generator import generate_linkedin_post, client as groq_client
except ImportError:
    print("Warning: Could not import news modules")
    fetch_latest_news = None
    rank_and_sort_news = None
    generate_linkedin_post = None
    groq_client = None


class NewsWorker(QThread):
    """Worker thread for fetching news"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def run(self):
        """Fetch news in background"""
        try:
            if not fetch_latest_news:
                raise Exception("news_fetcher module not available")
            
            self.progress.emit("Connecting to news sources...")
            news = fetch_latest_news()
            
            self.progress.emit("Ranking by relevance...")
            ranked_news = rank_and_sort_news(news)
            
            self.progress.emit("Processing complete...")
            self.finished.emit(ranked_news)
        except Exception as e:
            self.error.emit(str(e))


class PostGeneratorWorker(QThread):
    """Worker thread for generating posts"""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, news_item):
        super().__init__()
        self.news_item = news_item
    
    def run(self):
        """Generate post in background"""
        try:
            if not generate_linkedin_post:
                raise Exception("post_generator module not available")
            
            post = generate_linkedin_post(self.news_item)
            self.finished.emit(post)
        except Exception as e:
            self.error.emit(str(e))


class ChatWorker(QThread):
    """Worker to call Groq chat API off the main thread"""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, context, user_text, groq_client):
        super().__init__()
        self.context = context
        self.user_text = user_text
        self.groq_client = groq_client

    def run(self):
        try:
            response = self.groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are an expert assistant that discusses AI news articles concisely and helpfully."},
                    {"role": "user", "content": self.context + "User: " + self.user_text}
                ],
                temperature=0.7,
                max_tokens=300
            )
            ai_reply = response.choices[0].message.content
            self.finished.emit(ai_reply)
        except Exception as e:
            self.error.emit(str(e))


class TerminalColors:
    """Terminal color scheme"""
    BG_DARK = "#0c0c0c"
    BG_HEADER = "#1a1a1a"
    BG_SIDEBAR = "#111111"
    BG_INPUT = "#0a0a0a"
    BORDER = "#333333"
    
    TEXT_GREEN = "#00ff41"
    TEXT_CYAN = "#00d4ff"
    TEXT_YELLOW = "#ffd700"
    TEXT_WHITE = "#e0e0e0"
    TEXT_GRAY = "#888888"
    TEXT_DARK_GRAY = "#555555"
    TEXT_PURPLE = "#bd93f9"
    TEXT_ORANGE = "#ffb86c"
    
    BTN_CLOSE = "#ff5f57"
    BTN_MINIMIZE = "#ffbd2e"
    BTN_MAXIMIZE = "#28ca41"
    
    ACCENT_BLUE = "#0078d4"


class WindowButton(QPushButton):
    """Traffic light window button"""
    def __init__(self, color, parent=None):
        super().__init__(parent)
        self.setFixedSize(12, 12)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: none;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                filter: brightness(1.2);
            }}
        """)


class GlowLabel(QLabel):
    """Label with glow effect"""
    def __init__(self, text="", color=TerminalColors.TEXT_GREEN, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"color: {color};")
        
        # Add glow effect
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(15)
        glow.setColor(QColor(color))
        glow.setOffset(0, 0)
        self.setGraphicsEffect(glow)


class NavButton(QPushButton):
    """Sidebar navigation button"""
    def __init__(self, number, text, parent=None):
        super().__init__(parent)
        self.number = number
        self.text_label = text
        self.is_active = False
        self.setText(f"[{number}]  {text}")
        self.setFixedHeight(45)
        self.setCursor(Qt.PointingHandCursor)
        self.setFont(QFont("JetBrains Mono", 10))
        self.update_style()
    
    def update_style(self):
        if self.is_active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {TerminalColors.BG_HEADER};
                    color: {TerminalColors.TEXT_GREEN};
                    border: none;
                    text-align: left;
                    padding-left: 20px;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {TerminalColors.TEXT_WHITE};
                    border: none;
                    text-align: left;
                    padding-left: 20px;
                }}
                QPushButton:hover {{
                    background-color: {TerminalColors.BG_HEADER};
                    color: {TerminalColors.TEXT_GREEN};
                }}
            """)
    
    def set_active(self, active):
        self.is_active = active
        self.update_style()


class TerminalButton(QPushButton):
    """Terminal-style command button"""
    def __init__(self, text, border_color=TerminalColors.TEXT_GREEN, 
                 text_color=None, bg_color=None, parent=None):
        super().__init__(text, parent)
        self.border_color = border_color
        self.text_color = text_color or border_color
        self.bg_color = bg_color or TerminalColors.BG_HEADER
        self.setCursor(Qt.PointingHandCursor)
        self.setFont(QFont("JetBrains Mono", 10, QFont.Bold))
        self.setFixedHeight(50)
        self.setMinimumHeight(50)
        self.update_style()
    
    def update_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.bg_color};
                color: {self.text_color};
                border: 2px solid {self.border_color};
                border-radius: 0px;
                padding: 12px 24px;
                font-weight: bold;
                min-width: 80px;
                min-height: 40px;
            }}
            QPushButton:hover {{
                background-color: {self.border_color};
                color: {TerminalColors.BG_DARK};
            }}
            QPushButton:pressed {{
                background-color: {self.border_color};
            }}
        """)


class NewsItemWidget(QFrame):
    """Custom news item widget"""
    clicked = pyqtSignal(int)
    
    def __init__(self, index, score, title, source, parent=None):
        super().__init__(parent)
        self.index = index
        self.is_selected = False
        self.setup_ui(score, title, source)
    
    def setup_ui(self, score, title, source):
        self.setFixedHeight(70)
        self.setCursor(Qt.PointingHandCursor)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)
        
        # Score section
        score_frame = QFrame()
        score_frame.setFixedWidth(50)
        score_layout = QVBoxLayout(score_frame)
        score_layout.setContentsMargins(0, 0, 0, 0)
        score_layout.setSpacing(0)
        score_layout.setAlignment(Qt.AlignCenter)
        
        # Determine score color
        if score >= 90:
            score_color = TerminalColors.TEXT_GREEN
        elif score >= 80:
            score_color = TerminalColors.TEXT_CYAN
        elif score >= 70:
            score_color = TerminalColors.TEXT_YELLOW
        else:
            score_color = TerminalColors.TEXT_GRAY
        
        score_label = QLabel(str(score))
        score_label.setFont(QFont("JetBrains Mono", 14, QFont.Bold))
        score_label.setStyleSheet(f"color: {score_color};")
        score_label.setAlignment(Qt.AlignCenter)
        
        score_sub = QLabel("/100")
        score_sub.setFont(QFont("JetBrains Mono", 8))
        score_sub.setStyleSheet(f"color: {TerminalColors.TEXT_DARK_GRAY};")
        score_sub.setAlignment(Qt.AlignCenter)
        
        score_layout.addWidget(score_label)
        score_layout.addWidget(score_sub)
        
        # Content section
        content_frame = QFrame()
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(5)
        
        title_label = QLabel(title[:80] + "..." if len(title) > 80 else title)
        title_label.setFont(QFont("JetBrains Mono", 10))
        title_label.setStyleSheet(f"color: {TerminalColors.TEXT_WHITE};")
        title_label.setWordWrap(True)
        
        meta_label = QLabel(f"<span style='color: {TerminalColors.TEXT_CYAN};'>{source}</span> • #{str(self.index + 1).zfill(3)}")
        meta_label.setFont(QFont("JetBrains Mono", 8))
        meta_label.setStyleSheet(f"color: {TerminalColors.TEXT_GRAY};")
        
        content_layout.addWidget(title_label)
        content_layout.addWidget(meta_label)
        
        layout.addWidget(score_frame)
        layout.addWidget(content_frame, 1)
        
        self.update_style()
    
    def update_style(self):
        if self.is_selected:
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: rgba(0, 212, 255, 0.1);
                    border-left: 3px solid {TerminalColors.TEXT_CYAN};
                    border-top: none;
                    border-right: none;
                    border-bottom: none;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: transparent;
                    border-left: 3px solid transparent;
                }}
                QFrame:hover {{
                    background-color: rgba(0, 255, 65, 0.05);
                    border-left: 3px solid {TerminalColors.TEXT_GREEN};
                }}
            """)
    
    def set_selected(self, selected):
        self.is_selected = selected
        self.update_style()
    
    def mousePressEvent(self, event):
        self.clicked.emit(self.index)
        super().mousePressEvent(event)


class LinkedInTerminalApp(QMainWindow):
    """Main application window with terminal theme"""
    
    def __init__(self):
        super().__init__()
        self.current_news_items = []
        self.selected_news = None
        self.current_post = None
        self.post_count = 0
        self.news_widgets = []
        self.nav_buttons = []
        self.settings = {}  # Store settings
        self.chat_messages = []  # store (role, text) tuples for chat history
        
        self.init_fonts()
        self.load_settings()
        self.init_ui()
        self.start_clock()
    
    def init_fonts(self):
        """Initialize fonts"""
        # Try to load JetBrains Mono, fallback to Consolas/Courier
        self.mono_font = QFont("JetBrains Mono", 10)
        # Use Consolas as fallback (works on Windows)
        self.mono_font_fallback = QFont("Consolas", 10)
        if not self.mono_font.exactMatch():
            self.mono_font = self.mono_font_fallback
    
    def load_settings(self):
        """Load settings from .env file"""
        try:
            from dotenv import load_dotenv, dotenv_values
            import os
            
            load_dotenv()
            env_values = dotenv_values('.env')
            
            self.settings = {
                'api_key': os.getenv('GROQ_API_KEY', ''),
                'webhook_url': os.getenv('MAKE_WEBHOOK_URL', ''),
                'scanline': True,
                'glow': True,
                'contrast': False
            }
        except Exception as e:
            print(f"Error loading settings: {e}")
            self.settings = {
                'api_key': '',
                'webhook_url': '',
                'scanline': True,
                'glow': True,
                'contrast': False
            }
    
    def save_settings_clicked(self):
        """Save settings when button is clicked"""
        try:
            import os
            from pathlib import Path
            
            # Get values from inputs
            api_key = self.api_key_input.text()
            webhook_url = self.webhook_input.text()
            
            # Read existing .env or create new
            env_file = '.env'
            env_content = {}
            
            if os.path.exists(env_file):
                with open(env_file, 'r') as f:
                    for line in f:
                        if '=' in line and not line.startswith('#'):
                            key, value = line.strip().split('=', 1)
                            env_content[key] = value
            
            # Update with new values
            if api_key:
                env_content['GROQ_API_KEY'] = api_key
            if webhook_url:
                env_content['MAKE_WEBHOOK_URL'] = webhook_url
            
            # Save to .env
            with open(env_file, 'w') as f:
                for key, value in env_content.items():
                    f.write(f"{key}={value}\n")
            
            # Update settings dict
            self.settings['scanline'] = self.scanline_cb.isChecked()
            self.settings['glow'] = self.glow_cb.isChecked()
            self.settings['contrast'] = self.contrast_cb.isChecked()
            
            QMessageBox.information(self, "Success", "Settings saved successfully!")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save settings: {str(e)}")
    
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("LinkedIn News Bot - Terminal")
        self.setGeometry(50, 50, 1400, 850)
        self.setMinimumSize(1200, 700)
        
        # Set dark background
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {TerminalColors.BG_DARK};
            }}
            QScrollBar:vertical {{
                background-color: {TerminalColors.BG_DARK};
                width: 8px;
                border: none;
            }}
            QScrollBar::handle:vertical {{
                background-color: {TerminalColors.BORDER};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: #555555;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar:horizontal {{
                background-color: {TerminalColors.BG_DARK};
                height: 8px;
                border: none;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {TerminalColors.BORDER};
                border-radius: 4px;
                min-width: 20px;
            }}
        """)
        
        # Main container
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(0)
        
        # Terminal frame
        terminal_frame = QFrame()
        terminal_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {TerminalColors.BG_DARK};
                border: 1px solid {TerminalColors.BORDER};
                border-radius: 8px;
            }}
        """)
        terminal_layout = QVBoxLayout(terminal_frame)
        terminal_layout.setContentsMargins(0, 0, 0, 0)
        terminal_layout.setSpacing(0)
        
        # Title bar
        title_bar = self.create_title_bar()
        terminal_layout.addWidget(title_bar)
        
        # Content area (sidebar + main)
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Sidebar
        sidebar = self.create_sidebar()
        content_layout.addWidget(sidebar)
        
        # Main content
        main_content = self.create_main_content()
        content_layout.addWidget(main_content, 1)
        
        terminal_layout.addWidget(content_widget, 1)
        
        # Command line footer
        cmd_footer = self.create_command_footer()
        terminal_layout.addWidget(cmd_footer)
        
        main_layout.addWidget(terminal_frame)
        self.setCentralWidget(main_widget)
    
    def create_title_bar(self):
        """Create the terminal title bar"""
        title_bar = QFrame()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet(f"""
            QFrame {{
                background-color: {TerminalColors.BG_HEADER};
                border-bottom: 1px solid {TerminalColors.BORDER};
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
        """)
        
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(8)
        
        # Window buttons
        btn_close = WindowButton(TerminalColors.BTN_CLOSE)
        btn_minimize = WindowButton(TerminalColors.BTN_MINIMIZE)
        btn_maximize = WindowButton(TerminalColors.BTN_MAXIMIZE)
        
        layout.addWidget(btn_close)
        layout.addWidget(btn_minimize)
        layout.addWidget(btn_maximize)
        
        layout.addSpacing(20)
        
        # Path
        path_label = QLabel("C:\\Users\\Admin\\linkedin-news-bot>")
        path_label.setFont(self.mono_font)
        path_label.setStyleSheet(f"color: {TerminalColors.TEXT_GRAY};")
        layout.addWidget(path_label)
        
        exe_label = QLabel("newsbot.exe")
        exe_label.setFont(QFont(self.mono_font.family(), 10, QFont.Bold))
        exe_label.setStyleSheet(f"color: {TerminalColors.TEXT_GREEN};")
        layout.addWidget(exe_label)
        
        layout.addStretch()
        
        # DateTime
        self.datetime_label = QLabel()
        self.datetime_label.setFont(QFont(self.mono_font.family(), 9))
        self.datetime_label.setStyleSheet(f"color: {TerminalColors.TEXT_GRAY};")
        layout.addWidget(self.datetime_label)
        
        layout.addSpacing(15)
        
        # Status
        status_label = QLabel("● ONLINE")
        status_label.setFont(QFont(self.mono_font.family(), 9))
        status_label.setStyleSheet(f"color: {TerminalColors.TEXT_GREEN};")
        layout.addWidget(status_label)
        
        return title_bar
    
    def create_sidebar(self):
        """Create the sidebar"""
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet(f"""
            QFrame {{
                background-color: {TerminalColors.BG_SIDEBAR};
                border-right: 1px solid {TerminalColors.BORDER};
            }}
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Logo section
        logo_frame = QFrame()
        logo_frame.setStyleSheet(f"border-bottom: 1px solid {TerminalColors.BORDER};")
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setContentsMargins(15, 15, 15, 15)
        logo_layout.setSpacing(2)
        
        # ASCII box logo
        logo_lines = [
            "╔══════════════╗",
            "║   LINK BOT   ║",
            "╚══════════════╝"
        ]
        
        for line in logo_lines:
            lbl = GlowLabel(line, TerminalColors.TEXT_GREEN)
            lbl.setFont(QFont(self.mono_font.family(), 11, QFont.Bold))
            lbl.setAlignment(Qt.AlignCenter)
            logo_layout.addWidget(lbl)
        
        version_label = QLabel("LINK Automation v1.0")
        version_label.setFont(QFont(self.mono_font.family(), 8))
        version_label.setStyleSheet(f"color: {TerminalColors.TEXT_GRAY};")
        version_label.setAlignment(Qt.AlignCenter)
        logo_layout.addSpacing(5)
        logo_layout.addWidget(version_label)
        
        layout.addWidget(logo_frame)
        
        # Navigation label
        nav_label = QLabel("NAVIGATION")
        nav_label.setFont(QFont(self.mono_font.family(), 8))
        nav_label.setStyleSheet(f"color: {TerminalColors.TEXT_GRAY}; padding: 15px 20px 5px 20px;")
        layout.addWidget(nav_label)
        
        # Navigation buttons
        nav_items = [
            ("1", "News Feed"),
            ("2", "Generator"),
            ("3", "Settings"),
            ("4", "About"),
            ("5", "Chat")
        ]
        
        for i, (num, text) in enumerate(nav_items):
            btn = NavButton(num, text)
            btn.clicked.connect(lambda checked, idx=i: self.show_page(idx))
            self.nav_buttons.append(btn)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # System status
        status_frame = QFrame()
        status_frame.setStyleSheet(f"border-top: 1px solid {TerminalColors.BORDER};")
        status_layout = QVBoxLayout(status_frame)
        status_layout.setContentsMargins(15, 15, 15, 15)
        status_layout.setSpacing(8)
        
        status_title = QLabel("SYSTEM STATUS")
        status_title.setFont(QFont(self.mono_font.family(), 8))
        status_title.setStyleSheet(f"color: {TerminalColors.TEXT_GRAY};")
        status_layout.addWidget(status_title)
        
        # Status items
        status_items = [
            ("Memory:", "OK", TerminalColors.TEXT_GREEN),
            ("API:", "Connected", TerminalColors.TEXT_CYAN),
            ("Posts:", "0", TerminalColors.TEXT_YELLOW)
        ]
        
        for label, value, color in status_items:
            row = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setFont(QFont(self.mono_font.family(), 9))
            lbl.setStyleSheet(f"color: {color};")
            
            val = QLabel(value)
            val.setFont(QFont(self.mono_font.family(), 9))
            val.setStyleSheet(f"color: {color};")
            
            if label == "Posts:":
                self.post_count_label = val
            
            row.addWidget(lbl)
            row.addStretch()
            row.addWidget(val)
            status_layout.addLayout(row)
        
        layout.addWidget(status_frame)
        
        return sidebar
    
    def create_main_content(self):
        """Create the main content area"""
        content = QFrame()
        content.setStyleSheet(f"background-color: {TerminalColors.BG_DARK};")
        
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Stacked widget for pages
        self.stacked = QStackedWidget()
        
        # Create pages
        self.stacked.addWidget(self.create_news_page())
        self.stacked.addWidget(self.create_generator_page())
        self.stacked.addWidget(self.create_settings_page())
        self.stacked.addWidget(self.create_about_page())
        self.stacked.addWidget(self.create_chat_page())
        
        layout.addWidget(self.stacked)
        
        # Set initial page
        self.show_page(0)
        
        return content
    
    def create_news_page(self):
        """Create the news page"""
        page = QFrame()
        page.setStyleSheet(f"background-color: {TerminalColors.BG_DARK};")
        
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # Header
        header = GlowLabel("> LATEST_NEWS.exe", TerminalColors.TEXT_CYAN)
        header.setFont(QFont(self.mono_font.family(), 20, QFont.Bold))
        layout.addWidget(header)
        
        subtitle = QLabel("Curated LLM & AI News Articles | Real-time Feed")
        subtitle.setFont(QFont(self.mono_font.family(), 10))
        subtitle.setStyleSheet(f"color: {TerminalColors.TEXT_GRAY};")
        layout.addWidget(subtitle)
        
        layout.addSpacing(10)
        
        # Action bar
        action_layout = QHBoxLayout()
        action_layout.setSpacing(15)
        
        fetch_btn = TerminalButton("FETCH NEWS", TerminalColors.TEXT_GREEN)
        fetch_btn.setMinimumWidth(180)
        fetch_btn.clicked.connect(self.fetch_news)
        action_layout.addWidget(fetch_btn)
        
        refresh_btn = TerminalButton("REFRESH", TerminalColors.TEXT_GRAY)
        refresh_btn.setMinimumWidth(140)
        refresh_btn.clicked.connect(self.fetch_news)
        action_layout.addWidget(refresh_btn)
        
        self.news_status = QLabel("● Ready")
        self.news_status.setFont(QFont(self.mono_font.family(), 10))
        self.news_status.setStyleSheet(f"color: {TerminalColors.TEXT_GRAY};")
        action_layout.addWidget(self.news_status)
        
        action_layout.addStretch()
        layout.addLayout(action_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {TerminalColors.BG_HEADER};
                border: none;
                border-radius: 3px;
            }}
            QProgressBar::chunk {{
                background-color: {TerminalColors.TEXT_GREEN};
                border-radius: 3px;
            }}
        """)
        layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("")
        self.progress_label.setFont(QFont(self.mono_font.family(), 9))
        self.progress_label.setStyleSheet(f"color: {TerminalColors.TEXT_GREEN};")
        self.progress_label.setVisible(False)
        layout.addWidget(self.progress_label)
        
        # News list container
        list_container = QFrame()
        list_container.setStyleSheet(f"""
            QFrame {{
                background-color: {TerminalColors.BG_INPUT};
                border: 1px solid {TerminalColors.BORDER};
                border-radius: 4px;
            }}
        """)
        list_layout = QVBoxLayout(list_container)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(0)
        
        # List header
        list_header = QFrame()
        list_header.setFixedHeight(35)
        list_header.setStyleSheet(f"""
            QFrame {{
                background-color: {TerminalColors.BG_HEADER};
                border-bottom: 1px solid {TerminalColors.BORDER};
            }}
        """)
        header_layout = QHBoxLayout(list_header)
        header_layout.setContentsMargins(15, 0, 15, 0)
        
        header_title = QLabel("NEWS ARTICLES")
        header_title.setFont(QFont(self.mono_font.family(), 9))
        header_title.setStyleSheet(f"color: {TerminalColors.TEXT_GRAY};")
        header_layout.addWidget(header_title)
        
        header_layout.addStretch()
        
        self.news_count_label = QLabel("0 items")
        self.news_count_label.setFont(QFont(self.mono_font.family(), 9))
        self.news_count_label.setStyleSheet(f"color: {TerminalColors.TEXT_GREEN};")
        header_layout.addWidget(self.news_count_label)
        
        list_layout.addWidget(list_header)
        
        # Scroll area for news items
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        self.news_list_widget = QWidget()
        self.news_list_layout = QVBoxLayout(self.news_list_widget)
        self.news_list_layout.setContentsMargins(0, 0, 0, 0)
        self.news_list_layout.setSpacing(0)
        self.news_list_layout.addStretch()
        
        # Empty state
        self.empty_state = QFrame()
        empty_layout = QVBoxLayout(self.empty_state)
        empty_layout.setAlignment(Qt.AlignCenter)
        
        empty_icon = QLabel("[WAITING FOR INPUT]")
        empty_icon.setFont(QFont(self.mono_font.family(), 14, QFont.Bold))
        empty_icon.setStyleSheet(f"color: {TerminalColors.TEXT_GRAY};")
        empty_icon.setAlignment(Qt.AlignCenter)
        empty_layout.addWidget(empty_icon)
        
        empty_text = QLabel("No news loaded. Click FETCH NEWS to begin.")
        empty_text.setFont(QFont(self.mono_font.family(), 11))
        empty_text.setStyleSheet(f"color: {TerminalColors.TEXT_GRAY};")
        empty_text.setAlignment(Qt.AlignCenter)
        empty_layout.addWidget(empty_text)
        
        empty_hint = QLabel("Press [F] for quick fetch")
        empty_hint.setFont(QFont(self.mono_font.family(), 9))
        empty_hint.setStyleSheet(f"color: {TerminalColors.TEXT_DARK_GRAY};")
        empty_hint.setAlignment(Qt.AlignCenter)
        empty_layout.addWidget(empty_hint)
        
        self.news_list_layout.insertWidget(0, self.empty_state)
        
        scroll.setWidget(self.news_list_widget)
        list_layout.addWidget(scroll, 1)
        
        layout.addWidget(list_container, 1)
        
        return page
    
    def create_generator_page(self):
        """Create the generator page"""
        page = QFrame()
        page.setStyleSheet(f"background-color: {TerminalColors.BG_DARK};")
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # Header
        header = GlowLabel("> POST_GENERATOR.exe", TerminalColors.TEXT_PURPLE)
        header.setFont(QFont(self.mono_font.family(), 20, QFont.Bold))
        layout.addWidget(header)
        
        subtitle = QLabel("AI-Powered LinkedIn Post Creation")
        subtitle.setFont(QFont(self.mono_font.family(), 10))
        subtitle.setStyleSheet(f"color: {TerminalColors.TEXT_GRAY};")
        layout.addWidget(subtitle)
        
        layout.addSpacing(10)
        
        # Selected article card
        article_card = QFrame()
        article_card.setStyleSheet(f"""
            QFrame {{
                background-color: {TerminalColors.BG_HEADER};
                border: 1px solid {TerminalColors.BORDER};
                border-radius: 4px;
                padding: 15px;
            }}
        """)
        article_layout = QVBoxLayout(article_card)
        article_layout.setSpacing(10)
        
        article_header = QLabel("◆ SELECTED ARTICLE")
        article_header.setFont(QFont(self.mono_font.family(), 10, QFont.Bold))
        article_header.setStyleSheet(f"color: {TerminalColors.TEXT_YELLOW};")
        article_layout.addWidget(article_header)
        
        self.selected_title = QLabel("No article selected")
        self.selected_title.setFont(QFont(self.mono_font.family(), 11, QFont.Bold))
        self.selected_title.setStyleSheet(f"color: {TerminalColors.TEXT_WHITE};")
        self.selected_title.setWordWrap(True)
        article_layout.addWidget(self.selected_title)
        
        self.selected_details = QLabel("Select a news article from the News Feed to generate a post.")
        self.selected_details.setFont(QFont(self.mono_font.family(), 10))
        self.selected_details.setStyleSheet(f"color: {TerminalColors.TEXT_GRAY};")
        self.selected_details.setWordWrap(True)
        article_layout.addWidget(self.selected_details)
        
        layout.addWidget(article_card)
        
        # Generate button
        action_layout = QHBoxLayout()
        action_layout.setSpacing(15)
        
        gen_btn = TerminalButton("GENERATE POST", TerminalColors.TEXT_PURPLE)
        gen_btn.setMinimumWidth(220)
        gen_btn.clicked.connect(self.generate_post)
        action_layout.addWidget(gen_btn)
        
        self.gen_status = QLabel("")
        self.gen_status.setFont(QFont(self.mono_font.family(), 10))
        self.gen_status.setStyleSheet(f"color: {TerminalColors.TEXT_GRAY};")
        action_layout.addWidget(self.gen_status)
        
        action_layout.addStretch()
        layout.addLayout(action_layout)
        
        # Output section
        output_header = QHBoxLayout()
        output_label = QLabel("GENERATED OUTPUT")
        output_label.setFont(QFont(self.mono_font.family(), 10, QFont.Bold))
        output_label.setStyleSheet(f"color: {TerminalColors.TEXT_CYAN};")
        output_header.addWidget(output_label)
        
        output_header.addStretch()
        
        self.char_count = QLabel("0 characters")
        self.char_count.setFont(QFont(self.mono_font.family(), 9))
        self.char_count.setStyleSheet(f"color: {TerminalColors.TEXT_GRAY};")
        output_header.addWidget(self.char_count)
        
        layout.addLayout(output_header)
        
        # Post output
        self.post_output = QTextEdit()
        self.post_output.setReadOnly(False)
        self.post_output.setMinimumHeight(250)
        self.post_output.setFont(QFont(self.mono_font.family(), 10))
        self.post_output.setPlaceholderText("// Output will appear here...")
        self.post_output.setStyleSheet(f"""
            QTextEdit {{
                background-color: {TerminalColors.BG_INPUT};
                color: {TerminalColors.TEXT_WHITE};
                border: 1px solid {TerminalColors.BORDER};
                border-radius: 4px;
                padding: 20px;
            }}
        """)
        layout.addWidget(self.post_output)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        save_btn = TerminalButton("SAVE", TerminalColors.TEXT_YELLOW)
        save_btn.setMinimumWidth(120)
        save_btn.clicked.connect(self.save_post)
        btn_layout.addWidget(save_btn)
        
        post_btn = TerminalButton("POST TO LINKEDIN", TerminalColors.TEXT_WHITE, 
                                  TerminalColors.TEXT_WHITE, TerminalColors.ACCENT_BLUE)
        post_btn.setMinimumWidth(220)
        post_btn.clicked.connect(self.post_to_linkedin)
        btn_layout.addWidget(post_btn)
        
        copy_btn = TerminalButton("COPY", TerminalColors.TEXT_GRAY)
        copy_btn.setMinimumWidth(120)
        copy_btn.clicked.connect(self.copy_post)
        btn_layout.addWidget(copy_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        layout.addStretch()
        
        scroll.setWidget(scroll_content)
        
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll)
        
        return page
    
    def create_settings_page(self):
        """Create the settings page"""
        page = QFrame()
        page.setStyleSheet(f"background-color: {TerminalColors.BG_DARK};")
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header = GlowLabel("> CONFIG.sys", TerminalColors.TEXT_ORANGE)
        header.setFont(QFont(self.mono_font.family(), 20, QFont.Bold))
        layout.addWidget(header)
        
        subtitle = QLabel("Application Settings & Configuration")
        subtitle.setFont(QFont(self.mono_font.family(), 10))
        subtitle.setStyleSheet(f"color: {TerminalColors.TEXT_GRAY};")
        layout.addWidget(subtitle)
        
        layout.addSpacing(10)
        
        # API Settings card
        api_card = QFrame()
        api_card.setMaximumWidth(600)
        api_card.setStyleSheet(f"""
            QFrame {{
                background-color: {TerminalColors.BG_HEADER};
                border: 1px solid {TerminalColors.BORDER};
                border-radius: 4px;
            }}
        """)
        api_layout = QVBoxLayout(api_card)
        api_layout.setContentsMargins(20, 20, 20, 20)
        api_layout.setSpacing(15)
        
        api_header = QLabel("[API CONFIGURATION]")
        api_header.setFont(QFont(self.mono_font.family(), 11, QFont.Bold))
        api_header.setStyleSheet(f"color: {TerminalColors.TEXT_CYAN};")
        api_layout.addWidget(api_header)
        
        # OpenAI API Key
        api_key_label = QLabel("Groq API Key")
        api_key_label.setFont(QFont(self.mono_font.family(), 9))
        api_key_label.setStyleSheet(f"color: {TerminalColors.TEXT_GRAY};")
        api_layout.addWidget(api_key_label)
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setText(self.settings.get('api_key', ''))
        self.api_key_input.setFont(self.mono_font)
        self.api_key_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {TerminalColors.BG_INPUT};
                color: {TerminalColors.TEXT_WHITE};
                border: 1px solid {TerminalColors.BORDER};
                border-radius: 4px;
                padding: 15px;
            }}
            QLineEdit:focus {{
                border-color: {TerminalColors.TEXT_GREEN};
            }}
        """)
        api_layout.addWidget(self.api_key_input)
        
        # Webhook URL
        webhook_label = QLabel("Webhook URL")
        webhook_label.setFont(QFont(self.mono_font.family(), 9))
        webhook_label.setStyleSheet(f"color: {TerminalColors.TEXT_GRAY};")
        api_layout.addWidget(webhook_label)
        
        self.webhook_input = QLineEdit()
        self.webhook_input.setPlaceholderText("https://...")
        self.webhook_input.setEchoMode(QLineEdit.Password)
        self.webhook_input.setText(self.settings.get('webhook_url', ''))
        self.webhook_input.setFont(self.mono_font)
        self.webhook_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {TerminalColors.BG_INPUT};
                color: {TerminalColors.TEXT_WHITE};
                border: 1px solid {TerminalColors.BORDER};
                border-radius: 4px;
                padding: 15px;
            }}
            QLineEdit:focus {{
                border-color: {TerminalColors.TEXT_GREEN};
            }}
        """)
        api_layout.addWidget(self.webhook_input)
        
        layout.addWidget(api_card)
        
        # Display Settings card
        display_card = QFrame()
        display_card.setMaximumWidth(600)
        display_card.setStyleSheet(f"""
            QFrame {{
                background-color: {TerminalColors.BG_HEADER};
                border: 1px solid {TerminalColors.BORDER};
                border-radius: 4px;
            }}
        """)
        display_layout = QVBoxLayout(display_card)
        display_layout.setContentsMargins(20, 20, 20, 20)
        display_layout.setSpacing(15)
        
        display_header = QLabel("[DISPLAY OPTIONS]")
        display_header.setFont(QFont(self.mono_font.family(), 11, QFont.Bold))
        display_header.setStyleSheet(f"color: {TerminalColors.TEXT_PURPLE};")
        display_layout.addWidget(display_header)
        
        # Checkboxes
        self.scanline_cb = QCheckBox("Enable scanline effect")
        self.scanline_cb.setChecked(self.settings.get('scanline', True))
        self.scanline_cb.setFont(QFont(self.mono_font.family(), 10))
        self.scanline_cb.setStyleSheet(f"""
            QCheckBox {{
                color: {TerminalColors.TEXT_WHITE};
                spacing: 10px;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {TerminalColors.BORDER};
                border-radius: 3px;
                background-color: {TerminalColors.BG_INPUT};
            }}
            QCheckBox::indicator:checked {{
                background-color: {TerminalColors.TEXT_GREEN};
                border-color: {TerminalColors.TEXT_GREEN};
            }}
        """)
        display_layout.addWidget(self.scanline_cb)
        
        self.glow_cb = QCheckBox("Show glow effects")
        self.glow_cb.setChecked(self.settings.get('glow', True))
        self.glow_cb.setFont(QFont(self.mono_font.family(), 10))
        self.glow_cb.setStyleSheet(f"""
            QCheckBox {{
                color: {TerminalColors.TEXT_WHITE};
                spacing: 10px;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {TerminalColors.BORDER};
                border-radius: 3px;
                background-color: {TerminalColors.BG_INPUT};
            }}
            QCheckBox::indicator:checked {{
                background-color: {TerminalColors.TEXT_GREEN};
                border-color: {TerminalColors.TEXT_GREEN};
            }}
        """)
        display_layout.addWidget(self.glow_cb)
        
        self.contrast_cb = QCheckBox("High contrast mode")
        self.contrast_cb.setChecked(self.settings.get('contrast', False))
        self.contrast_cb.setFont(QFont(self.mono_font.family(), 10))
        self.contrast_cb.setStyleSheet(f"""
            QCheckBox {{
                color: {TerminalColors.TEXT_WHITE};
                spacing: 10px;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {TerminalColors.BORDER};
                border-radius: 3px;
                background-color: {TerminalColors.BG_INPUT};
            }}
            QCheckBox::indicator:checked {{
                background-color: {TerminalColors.TEXT_GREEN};
                border-color: {TerminalColors.TEXT_GREEN};
            }}
        """)
        display_layout.addWidget(self.contrast_cb)
        
        layout.addWidget(display_card)
        
        # Save button
        save_btn = TerminalButton("SAVE SETTINGS", TerminalColors.TEXT_GREEN)
        save_btn.setMinimumWidth(220)
        save_btn.setMaximumWidth(220)
        save_btn.clicked.connect(self.save_settings_clicked)
        layout.addWidget(save_btn, alignment=Qt.AlignLeft)
        
        layout.addStretch()
        
        scroll.setWidget(scroll_content)
        
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll)
        
        return page
    
    def create_chat_page(self):
        """Create the AI chat page for discussing selected article"""
        page = QFrame()
        page.setStyleSheet(f"background-color: {TerminalColors.BG_DARK};")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(10)

        header = GlowLabel("> AI_CHAT.exe", TerminalColors.TEXT_PURPLE)
        header.setFont(QFont(self.mono_font.family(), 18, QFont.Bold))
        layout.addWidget(header)

        subtitle = QLabel("Chat with Groq AI about the selected news article")
        subtitle.setFont(QFont(self.mono_font.family(), 10))
        subtitle.setStyleSheet(f"color: {TerminalColors.TEXT_GRAY};")
        layout.addWidget(subtitle)

        # Chat history (styled as chat bubbles)
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setMinimumHeight(320)
        self.chat_history.setFont(QFont(self.mono_font.family(), 10))
        self.chat_history.setStyleSheet(f"""
            QTextEdit {{
                background-color: {TerminalColors.BG_INPUT};
                color: {TerminalColors.TEXT_WHITE};
                border: 1px solid {TerminalColors.BORDER};
                border-radius: 8px;
                padding: 12px;
            }}
        """)
        # Initial hint
        self.chat_history.setHtml(f"<div style='color:{TerminalColors.TEXT_GRAY};'>No messages yet. Select an article and start the conversation.</div>")
        layout.addWidget(self.chat_history)

        # Input area
        input_frame = QFrame()
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(0,0,0,0)
        input_layout.setSpacing(8)

        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Ask the AI about the selected article... (Press Enter to send)")
        self.chat_input.setFont(self.mono_font)
        self.chat_input.setStyleSheet(f"background-color:{TerminalColors.BG_HEADER}; color:{TerminalColors.TEXT_WHITE}; padding:10px; border-radius:6px;")
        # Send on Enter
        self.chat_input.returnPressed.connect(self.send_chat_message)
        input_layout.addWidget(self.chat_input, 1)

        self.chat_send_btn = TerminalButton("SEND", TerminalColors.TEXT_GREEN)
        self.chat_send_btn.setMinimumWidth(120)
        self.chat_send_btn.clicked.connect(self.send_chat_message)
        # neutral, minimal button style (no bright colors)
        self.chat_send_btn.setStyleSheet(f"QPushButton {{ background-color: transparent; color: {TerminalColors.TEXT_WHITE}; border: 1px solid {TerminalColors.BORDER}; padding: 10px 12px; border-radius: 6px; }} QPushButton:hover {{ background-color: {TerminalColors.BG_HEADER}; }}")
        input_layout.addWidget(self.chat_send_btn)

        clear_btn = TerminalButton("CLEAR", TerminalColors.TEXT_YELLOW)
        clear_btn.setMinimumWidth(100)
        clear_btn.clicked.connect(self.clear_chat)
        clear_btn.setStyleSheet(f"QPushButton {{ background-color: transparent; color: {TerminalColors.TEXT_WHITE}; border: 1px solid {TerminalColors.BORDER}; padding: 10px 12px; border-radius: 6px; }} QPushButton:hover {{ background-color: {TerminalColors.BG_HEADER}; }}")
        input_layout.addWidget(clear_btn)

        layout.addWidget(input_frame)

        return page

    def render_chat_messages(self):
        """Render chat messages stored in self.chat_messages as chat bubbles"""
        rendered = ""
        for role, text in self.chat_messages:
            safe = html.escape(str(text))
            # preserve newlines
            safe = safe.replace('\n', '<br>')
            if role == 'user':
                bubble = (
                    f"<div style='text-align:right; margin:8px 0;'>"
                    f"<div style='display:inline-block; background:{TerminalColors.BG_HEADER}; color:{TerminalColors.TEXT_WHITE}; padding:10px 14px; border-radius:12px; max-width:70%; white-space:pre-wrap; word-break:break-word;'>{safe}</div>"
                    f"</div>"
                )
            elif role == 'assistant':
                bubble = (
                    f"<div style='text-align:left; margin:8px 0;'>"
                    f"<div style='display:inline-block; background:{TerminalColors.BG_INPUT}; color:{TerminalColors.TEXT_WHITE}; padding:10px 14px; border-radius:12px; max-width:70%; white-space:pre-wrap; word-break:break-word;'>{safe}</div>"
                    f"</div>"
                )
            else:
                bubble = f"<div style='color:{TerminalColors.TEXT_GRAY}; margin:6px 0;'>{safe}</div>"
            rendered += bubble
        self.chat_history.setHtml(rendered)
        self.chat_history.verticalScrollBar().setValue(self.chat_history.verticalScrollBar().maximum())

    def clear_chat(self):
        """Clear chat history"""
        self.chat_messages = []
        self.chat_history.setHtml(f"<div style='color:{TerminalColors.TEXT_GRAY};'>No messages yet. Select an article and start the conversation.</div>")

    def send_chat_message(self):
        """Send a message to the Groq AI chat model using a background worker"""
        user_text = self.chat_input.text().strip()
        if not user_text:
            return

        # Append user message and a placeholder assistant message
        self.chat_messages.append(('user', user_text))
        self.chat_messages.append(('assistant', 'AI is typing...'))
        self.render_chat_messages()
        self.chat_input.clear()

        # Build context from selected article if available
        context = ""
        if getattr(self, "selected_news", None):
            news = self.selected_news
            context = f"Article Title: {news.get('title')}\nSummary: {news.get('summary')}\nLink: {news.get('link')}\n\n"

        if not groq_client:
            # Replace placeholder with error
            if self.chat_messages and self.chat_messages[-1][0] == 'assistant':
                self.chat_messages[-1] = ('assistant', 'Groq client not available (import error).')
            else:
                self.chat_messages.append(('assistant', 'Groq client not available (import error).'))
            self.render_chat_messages()
            return

        # Disable input while waiting
        self.chat_input.setDisabled(True)
        try:
            self.chat_send_btn.setDisabled(True)
        except Exception:
            pass

        # Start background worker
        self.chat_worker = ChatWorker(context, user_text, groq_client)
        self.chat_worker.finished.connect(self.on_chat_finished)
        self.chat_worker.error.connect(self.on_chat_error)
        self.chat_worker.start()

    def on_chat_finished(self, ai_reply):
        # Replace the last assistant placeholder with the real reply
        if self.chat_messages and self.chat_messages[-1][0] == 'assistant':
            self.chat_messages[-1] = ('assistant', ai_reply)
        else:
            self.chat_messages.append(('assistant', ai_reply))
        self.render_chat_messages()
        self.chat_input.setDisabled(False)
        try:
            self.chat_send_btn.setDisabled(False)
        except Exception:
            pass
        try:
            self.chat_worker.quit()
        except Exception:
            pass

    def on_chat_error(self, err_msg):
        err_text = f"Error contacting Groq API: {err_msg}"
        if self.chat_messages and self.chat_messages[-1][0] == 'assistant':
            self.chat_messages[-1] = ('assistant', err_text)
        else:
            self.chat_messages.append(('assistant', err_text))
        self.render_chat_messages()
        self.chat_input.setDisabled(False)
        try:
            self.chat_send_btn.setDisabled(False)
        except Exception:
            pass
        try:
            self.chat_worker.quit()
        except Exception:
            pass

    def create_about_page(self):
        """Create the about page"""
        page = QFrame()
        page.setStyleSheet(f"background-color: {TerminalColors.BG_DARK};")
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # Header
        header = GlowLabel("> ABOUT.txt", TerminalColors.TEXT_GREEN)
        header.setFont(QFont(self.mono_font.family(), 20, QFont.Bold))
        layout.addWidget(header)
        
        layout.addSpacing(10)
        
        # About content
        about_card = QFrame()
        about_card.setStyleSheet(f"""
            QFrame {{
                background-color: {TerminalColors.BG_HEADER};
                border: 1px solid {TerminalColors.BORDER};
                border-radius: 4px;
            }}
        """)
        about_layout = QVBoxLayout(about_card)
        about_layout.setContentsMargins(25, 25, 25, 25)
        
        about_text = """╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ██╗     ██╗███╗   ██╗██╗  ██╗                          ║
║   ██║     ██║████╗  ██║██║ ██╔╝                          ║
║   ██║     ██║██╔██╗ ██║█████╔╝                           ║
║   ██║     ██║██║╚██╗██║██╔═██╗                           ║
║   ███████╗██║██║ ╚████║██║  ██╗                          ║
║   ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝                          ║
║                                                           ║
║              LINK BOT - AI Automation Tool                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

  Version:     1.0.0
  Build:       2024.01.15
  Author:      EK KABOURI ISMAIL
  License:     MIT

  ─────────────────────────────────────────────────────────

  DESCRIPTION:

  LINK News Bot is an AI-powered automation tool that
  fetches the latest AI/LLM news, generates engaging
  social media posts, and helps you maintain a consistent
  online presence.

  FEATURES:

  • Real-time news aggregation from multiple sources
  • AI-powered post generation using Groq API
  • One-click posting via webhooks
  • Local post saving and history tracking
  • Customizable templates and styling

  ─────────────────────────────────────────────────────────

  KEYBOARD SHORTCUTS:

  [F]     - Fetch news
  [G]     - Generate post
  [1-4]   - Navigate pages
  [Ctrl+C] - Copy post
  [Ctrl+S] - Save post

  ─────────────────────────────────────────────────────────

  © 2024 LINK News Bot. All rights reserved."""
        
        about_label = QLabel(about_text)
        about_label.setFont(QFont(self.mono_font.family(), 9))
        about_label.setStyleSheet(f"color: {TerminalColors.TEXT_GREEN};")
        about_layout.addWidget(about_label)
        
        layout.addWidget(about_card)
        layout.addStretch()
        
        scroll.setWidget(scroll_content)
        
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll)
        
        return page
    
    def create_command_footer(self):
        """Create the command line footer"""
        footer = QFrame()
        footer.setFixedHeight(40)
        footer.setStyleSheet(f"""
            QFrame {{
                background-color: {TerminalColors.BG_SIDEBAR};
                border-top: 1px solid {TerminalColors.BORDER};
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
            }}
        """)
        
        layout = QHBoxLayout(footer)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(10)
        
        prompt = QLabel(">")
        prompt.setFont(QFont(self.mono_font.family(), 11, QFont.Bold))
        prompt.setStyleSheet(f"color: {TerminalColors.TEXT_GREEN};")
        layout.addWidget(prompt)
        
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Type a command... (help, fetch, generate, clear)")
        self.command_input.setFont(self.mono_font)
        self.command_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: transparent;
                color: {TerminalColors.TEXT_WHITE};
                border: none;
            }}
            QLineEdit::placeholder {{
                color: {TerminalColors.TEXT_DARK_GRAY};
            }}
        """)
        self.command_input.returnPressed.connect(self.handle_command)
        layout.addWidget(self.command_input, 1)
        
        cursor = QLabel("█")
        cursor.setFont(self.mono_font)
        cursor.setStyleSheet(f"color: {TerminalColors.TEXT_GREEN};")
        layout.addWidget(cursor)
        
        # Blinking cursor animation
        self.cursor_visible = True
        self.cursor_label = cursor
        self.cursor_timer = QTimer()
        self.cursor_timer.timeout.connect(self.blink_cursor)
        self.cursor_timer.start(500)
        
        return footer
    
    def blink_cursor(self):
        """Blink the cursor"""
        self.cursor_visible = not self.cursor_visible
        self.cursor_label.setVisible(self.cursor_visible)
    
    def start_clock(self):
        """Start the clock timer"""
        self.update_clock()
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
    
    def update_clock(self):
        """Update the clock display"""
        now = datetime.now()
        formatted = now.strftime("%a, %b %d %H:%M:%S")
        self.datetime_label.setText(formatted)
    
    def show_page(self, index):
        """Show a specific page"""
        self.stacked.setCurrentIndex(index)
        
        # Update nav button states
        for i, btn in enumerate(self.nav_buttons):
            btn.set_active(i == index)
    
    def handle_command(self):
        """Handle command input"""
        command = self.command_input.text().lower().strip()
        self.command_input.clear()
        
        if command == "help":
            QMessageBox.information(self, "Help", 
                "Commands: fetch, generate, clear, news, generator, settings, about")
        elif command == "fetch":
            self.show_page(0)
            self.fetch_news()
        elif command == "generate":
            self.show_page(1)
            self.generate_post()
        elif command == "clear":
            self.clear_news()
        elif command == "news":
            self.show_page(0)
        elif command == "generator":
            self.show_page(1)
        elif command == "settings":
            self.show_page(2)
        elif command == "about":
            self.show_page(3)
        elif command:
            QMessageBox.warning(self, "Unknown Command", 
                'Unknown command. Type "help" for available commands.')
    
    def keyPressEvent(self, event):
        """Handle keyboard shortcuts"""
        if self.command_input.hasFocus():
            return super().keyPressEvent(event)
        
        if event.key() == Qt.Key_F:
            self.show_page(0)
            self.fetch_news()
        elif event.key() == Qt.Key_G:
            self.show_page(1)
            self.generate_post()
        elif event.key() == Qt.Key_1:
            self.show_page(0)
        elif event.key() == Qt.Key_2:
            self.show_page(1)
        elif event.key() == Qt.Key_3:
            self.show_page(2)
        elif event.key() == Qt.Key_4:
            self.show_page(3)
        else:
            super().keyPressEvent(event)
    
    def fetch_news(self):
        """Fetch news from real news sources"""
        self.news_status.setText("● Fetching...")
        self.news_status.setStyleSheet(f"color: {TerminalColors.TEXT_YELLOW};")
        self.progress_bar.setVisible(True)
        self.progress_label.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Use QThread to fetch news asynchronously
        self.fetch_thread = QThread()
        self.fetch_worker = NewsWorker()
        self.fetch_worker.moveToThread(self.fetch_thread)
        
        self.fetch_worker.progress.connect(self.update_fetch_progress_real)
        self.fetch_worker.finished.connect(self.on_news_fetched_real)
        self.fetch_worker.error.connect(self.on_fetch_error)
        self.fetch_thread.started.connect(self.fetch_worker.run)
        
        self.fetch_thread.start()
    
    def update_fetch_progress_real(self, message):
        """Update fetch progress from worker"""
        self.progress_label.setText(message)
        self.progress_bar.setValue(min(self.progress_bar.value() + 25, 90))
    
    def on_news_fetched_real(self, news_list):
        """Handle real fetched news"""
        if self.fetch_thread:
            self.fetch_thread.quit()
            self.fetch_thread.wait()
        
        self.current_news_items = news_list
        self.progress_bar.setValue(100)
        self.progress_label.setText("Complete!")
        
        # Clear existing items
        self.clear_news_list()
        
        # Hide empty state
        self.empty_state.setVisible(False)
        
        # Add news items
        for i, news in enumerate(news_list):
            score = news.get('rank_score', 0)
            widget = NewsItemWidget(i, score, news['title'], news['source'])
            widget.clicked.connect(self.on_news_selected)
            self.news_widgets.append(widget)
            self.news_list_layout.insertWidget(i, widget)
        
        self.news_count_label.setText(f"{len(news_list)} items")
        self.news_status.setText(f"● Ready - {len(news_list)} articles loaded")
        self.news_status.setStyleSheet(f"color: {TerminalColors.TEXT_GREEN};")
        
        # Hide progress after delay
        QTimer.singleShot(500, lambda: (self.progress_bar.setVisible(False), self.progress_label.setVisible(False)))
    
    def on_fetch_error(self, error_msg):
        """Handle fetch error"""
        if self.fetch_thread:
            self.fetch_thread.quit()
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        self.news_status.setText(f"● Error: {error_msg}")
        self.news_status.setStyleSheet(f"color: {TerminalColors.TEXT_YELLOW};")
        QMessageBox.warning(self, "Fetch Error", f"Failed to fetch news: {error_msg}")
    
    def clear_news_list(self):
        """Clear the news list"""
        for widget in self.news_widgets:
            widget.deleteLater()
        self.news_widgets.clear()
    
    def clear_news(self):
        """Clear all news"""
        self.clear_news_list()
        self.current_news_items = []
        self.empty_state.setVisible(True)
        self.news_count_label.setText("0 items")
        self.news_status.setText("● Cleared")
    
    def on_news_selected(self, index):
        """Handle news selection"""
        # Update selection state
        for i, widget in enumerate(self.news_widgets):
            widget.set_selected(i == index)
        
        self.selected_news = self.current_news_items[index]
        
        # Update generator page
        news = self.selected_news
        self.selected_title.setText(news['title'])
        self.selected_details.setText(
            f"Score: {news['score']}/100 | Source: {news['source']}\n\n{news['summary']}"
        )
        self.post_output.clear()
        self.current_post = None
        self.char_count.setText("0 characters")
    
    def generate_post(self):
        """Generate a post using AI"""
        if not self.selected_news:
            QMessageBox.warning(self, "Warning", "Please select a news article first!")
            return
        
        self.gen_status.setText("Generating with Groq AI...")
        self.gen_status.setStyleSheet(f"color: {TerminalColors.TEXT_YELLOW};")
        self.post_output.setText("Analyzing article with AI...")
        
        # Use QThread for AI generation
        self.gen_thread = QThread()
        self.gen_worker = PostGeneratorWorker(self.selected_news)
        self.gen_worker.moveToThread(self.gen_thread)
        
        self.gen_worker.finished.connect(self.on_post_generated_real)
        self.gen_worker.error.connect(self.on_generate_error)
        self.gen_thread.started.connect(self.gen_worker.run)
        
        self.gen_thread.start()
    
    def on_post_generated_real(self, post_text):
        """Handle AI-generated post"""
        if self.gen_thread:
            self.gen_thread.quit()
            self.gen_thread.wait()
        
        self.current_post = post_text
        self.post_output.setText(post_text)
        self.char_count.setText(f"{len(post_text)} characters")
        self.gen_status.setText("Post generated successfully")
        self.gen_status.setStyleSheet(f"color: {TerminalColors.TEXT_GREEN};")
    
    def on_generate_error(self, error_msg):
        """Handle generation error"""
        if self.gen_thread:
            self.gen_thread.quit()
        self.post_output.setText("")
        self.gen_status.setText(f"Error: {error_msg}")
        self.gen_status.setStyleSheet(f"color: {TerminalColors.TEXT_YELLOW};")
        QMessageBox.warning(self, "Generation Error", f"Failed to generate post: {error_msg}")
    
    def save_post(self):
        """Save the post locally"""
        post_text = self.post_output.toPlainText()
        if not post_text.strip():
            QMessageBox.warning(self, "Warning", "Please generate a post first!")
            return
        
        try:
            import os
            from datetime import datetime
            
            # Create posts directory if it doesn't exist
            posts_dir = "saved_posts"
            if not os.path.exists(posts_dir):
                os.makedirs(posts_dir)
            
            # Save with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{posts_dir}/post_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(post_text)
            
            self.post_count += 1
            self.post_count_label.setText(str(self.post_count))
            QMessageBox.information(self, "Success", f"Post saved to {filename}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save post: {str(e)}")
    
    def post_to_linkedin(self):
        """Post to LinkedIn via webhook"""
        if not self.post_output.toPlainText().strip():
            QMessageBox.warning(self, "Warning", "Please generate a post first!")
            return
        
        try:
            import requests
            from dotenv import load_dotenv
            import os
            
            load_dotenv()
            webhook_url = os.getenv('MAKE_WEBHOOK_URL')
            
            if not webhook_url:
                QMessageBox.warning(self, "Error", "MAKE_WEBHOOK_URL not configured in .env")
                return
            
            # Get the edited post text
            post_text = self.post_output.toPlainText()
            
            payload = {
                "content": post_text
            }
            
            response = requests.post(webhook_url, json=payload, timeout=10)
            
            if response.status_code in [200, 201]:
                QMessageBox.information(self, "Success", "Post sent to LinkedIn webhook!")
                self.post_count += 1
                self.post_count_label.setText(str(self.post_count))
            else:
                QMessageBox.warning(self, "Error", f"Webhook returned status {response.status_code}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to post: {str(e)}")
    
    def copy_post(self):
        """Copy post to clipboard"""
        post_text = self.post_output.toPlainText()
        if not post_text.strip():
            QMessageBox.warning(self, "Warning", "Please generate a post first!")
            return
        
        clipboard = QApplication.clipboard()
        clipboard.setText(post_text)
        QMessageBox.information(self, "Success", "Post copied to clipboard!")


def main():
    app = QApplication(sys.argv)
    
    # Set application-wide font
    app.setFont(QFont("Consolas", 10))
    
    # Dark palette for message boxes
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(TerminalColors.BG_HEADER))
    palette.setColor(QPalette.WindowText, QColor(TerminalColors.TEXT_WHITE))
    palette.setColor(QPalette.Base, QColor(TerminalColors.BG_INPUT))
    palette.setColor(QPalette.AlternateBase, QColor(TerminalColors.BG_HEADER))
    palette.setColor(QPalette.Text, QColor(TerminalColors.TEXT_WHITE))
    palette.setColor(QPalette.Button, QColor(TerminalColors.BG_HEADER))
    palette.setColor(QPalette.ButtonText, QColor(TerminalColors.TEXT_WHITE))
    palette.setColor(QPalette.Highlight, QColor(TerminalColors.TEXT_GREEN))
    palette.setColor(QPalette.HighlightedText, QColor(TerminalColors.BG_DARK))
    app.setPalette(palette)
    
    window = LinkedInTerminalApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()