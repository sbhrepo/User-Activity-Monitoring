"""Main GUI application for Server Activity Monitor"""
import sys
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QListWidget, QListWidgetItem,
    QComboBox, QDialog, QSplitter, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QTimer
from PyQt5.QtGui import QFont, QColor

from config import (
    APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, get_user_name, save_user_name,
    STATUS_NEED_SERVER, STATUS_USING_SERVER, STATUS_DONE_SERVER, VALID_STATUSES,
    THEME_PRIMARY, THEME_SUCCESS, THEME_WARNING, THEME_DANGER,
    THEME_BACKGROUND, THEME_SURFACE, THEME_BORDER, THEME_TEXT, THEME_TEXT_SECONDARY
)
from network_discovery import NetworkDiscovery
from messaging import MessageServer, MessageClient
from database import MessageDatabase


class UserInputDialog(QDialog):
    """Dialog for initial user name input"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.username = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog UI"""
        self.setWindowTitle("Welcome - Enter Your Name")
        self.setModal(True)
        self.setGeometry(100, 100, 450, 200)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {THEME_BACKGROUND};
            }}
            QLabel {{
                color: {THEME_TEXT};
                font-size: 10pt;
            }}
            QLineEdit {{
                background-color: {THEME_SURFACE};
                color: {THEME_TEXT};
                border: 2px solid {THEME_BORDER};
                border-radius: 6px;
                padding: 8px 10px;
                font-size: 11pt;
                min-height: 36px;
            }}
            QLineEdit:focus {{
                border: 2px solid {THEME_PRIMARY};
            }}
            QPushButton {{
                background-color: {THEME_PRIMARY};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 24px;
                font-size: 10pt;
                font-weight: bold;
                min-height: 36px;
            }}
            QPushButton:hover {{
                background-color: #1d4ed8;
            }}
            QPushButton:pressed {{
                background-color: #1e40af;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Title
        title = QLabel("Welcome to Server Activity Monitor")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Instructions
        label = QLabel("Enter your name to identify yourself on the network:")
        layout.addWidget(label)
        
        # Input field
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Your name")
        self.name_input.returnPressed.connect(self.accept)
        layout.addWidget(self.name_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_btn = QPushButton("Continue")
        ok_btn.clicked.connect(self.accept)
        ok_btn.setMinimumWidth(100)
        button_layout.addWidget(ok_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def accept(self):
        """Accept dialog and save username"""
        username = self.name_input.text().strip()
        if not username:
            QMessageBox.warning(self, "Error", "Please enter your name")
            return
        
        if save_user_name(username):
            self.username = username
            super().accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to save user name")


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.username = get_user_name()
        
        if not self.username:
            dialog = UserInputDialog()
            if dialog.exec_() == QDialog.Accepted:
                self.username = dialog.username
            else:
                sys.exit()
        
        self.current_status = STATUS_NEED_SERVER
        self.discovery = NetworkDiscovery(self.username, self.on_discovery_update)
        self.message_server = MessageServer(self.username, self.on_message_received)
        self.message_db = MessageDatabase()
        
        self.init_ui()
        self.start_services()
        
        # Timer to refresh user list
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_user_list)
        self.refresh_timer.start(2000)  # Refresh every 2 seconds
    
    def init_ui(self):
        """Initialize main UI"""
        self.setWindowTitle(f"{APP_NAME} - {self.username}")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.apply_stylesheet()
        
        # Central widget
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header section
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)
        
        title_label = QLabel("Your Status")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(VALID_STATUSES)
        self.status_combo.setCurrentText(self.current_status)
        self.status_combo.currentTextChanged.connect(self.on_status_changed)
        header_layout.addWidget(self.status_combo)
        header_layout.addStretch()
        
        main_layout.addLayout(header_layout)
        
        # Content section: Users and Chat
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)
        
        # Left panel: Users list
        left_layout = QVBoxLayout()
        left_layout.setSpacing(10)
        
        users_title = QLabel("Users Online")
        users_title_font = QFont()
        users_title_font.setPointSize(11)
        users_title_font.setBold(True)
        users_title.setFont(users_title_font)
        left_layout.addWidget(users_title)
        
        self.users_list = QListWidget()
        self.users_list.itemSelectionChanged.connect(self.on_user_selected)
        left_layout.addWidget(self.users_list)
        
        content_layout.addLayout(left_layout, 1)
        
        # Right panel: Chat
        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)
        
        chat_title = QLabel("Messages")
        chat_title_font = QFont()
        chat_title_font.setPointSize(11)
        chat_title_font.setBold(True)
        chat_title.setFont(chat_title_font)
        right_layout.addWidget(chat_title)
        
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        chat_font = QFont("Segoe UI", 9)
        self.chat_display.setFont(chat_font)
        self.chat_display.setMinimumHeight(250)
        right_layout.addWidget(self.chat_display, 1)
        
        # Message input section
        msg_layout = QHBoxLayout()
        msg_layout.setSpacing(8)
        
        self.msg_input = QLineEdit()
        self.msg_input.setPlaceholderText("Type your message...")
        self.msg_input.returnPressed.connect(self.send_message)
        self.msg_input.setMinimumHeight(36)
        msg_layout.addWidget(self.msg_input)
        
        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.send_message)
        send_btn.setMinimumWidth(80)
        send_btn.setMinimumHeight(36)
        msg_layout.addWidget(send_btn)
        
        right_layout.addLayout(msg_layout)
        
        content_layout.addLayout(right_layout, 1)
        
        main_layout.addLayout(content_layout, 1)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
    def apply_stylesheet(self):
        """Apply modern stylesheet to the application"""
        stylesheet = f"""
        QMainWindow {{
            background-color: {THEME_BACKGROUND};
        }}
        
        QWidget {{
            background-color: {THEME_BACKGROUND};
            color: {THEME_TEXT};
        }}
        
        QLabel {{
            color: {THEME_TEXT};
        }}
        
        QComboBox {{
            background-color: {THEME_SURFACE};
            color: {THEME_TEXT};
            border: 2px solid {THEME_BORDER};
            border-radius: 6px;
            padding: 6px 8px;
            font-size: 10pt;
            selection-background-color: {THEME_PRIMARY};
        }}
        
        QComboBox:hover {{
            border: 2px solid {THEME_PRIMARY};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}
        
        QLineEdit {{
            background-color: {THEME_SURFACE};
            color: {THEME_TEXT};
            border: 2px solid {THEME_BORDER};
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 10pt;
        }}
        
        QLineEdit:focus {{
            border: 2px solid {THEME_PRIMARY};
            background-color: {THEME_SURFACE};
        }}
        
        QLineEdit::placeholder {{
            color: {THEME_TEXT_SECONDARY};
        }}
        
        QTextEdit {{
            background-color: {THEME_SURFACE};
            color: {THEME_TEXT};
            border: 2px solid {THEME_BORDER};
            border-radius: 6px;
            padding: 8px;
            font-family: 'Segoe UI', Courier;
            font-size: 9pt;
        }}
        
        QTextEdit:focus {{
            border: 2px solid {THEME_PRIMARY};
        }}
        
        QListWidget {{
            background-color: {THEME_SURFACE};
            color: {THEME_TEXT};
            border: 2px solid {THEME_BORDER};
            border-radius: 6px;
            outline: none;
        }}
        
        QListWidget::item {{
            padding: 8px;
            margin: 4px;
            border-radius: 4px;
            background-color: {THEME_BACKGROUND};
        }}
        
        QListWidget::item:hover {{
            background-color: #e0e7ff;
        }}
        
        QListWidget::item:selected {{
            background-color: {THEME_PRIMARY};
            color: white;
        }}
        
        QPushButton {{
            background-color: {THEME_PRIMARY};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 6px 16px;
            font-size: 10pt;
            font-weight: bold;
        }}
        
        QPushButton:hover {{
            background-color: #1d4ed8;
        }}
        
        QPushButton:pressed {{
            background-color: #1e40af;
        }}
        """
        
        self.setStyleSheet(stylesheet)
    
    def start_services(self):
        """Start network discovery and message server"""
        self.discovery.start()
        self.message_server.start()
        self.load_messages()
    
    def on_discovery_update(self):
        """Called when users list changes"""
        self.refresh_user_list()
    
    def refresh_user_list(self):
        """Refresh the users list"""
        users = self.discovery.get_online_users()
        
        # Clear and repopulate list
        self.users_list.clear()
        
        if not users:
            no_users_item = QListWidgetItem("No other users online")
            no_users_item.setForeground(QColor(THEME_TEXT_SECONDARY))
            self.users_list.addItem(no_users_item)
            return
        
        for username, user in sorted(users.items()):
            # Create formatted user item
            item_text = f"{username}"
            item = QListWidgetItem(item_text)
            
            # Set colors based on status with modern palette
            if user.status == STATUS_USING_SERVER:
                item.setBackground(QColor("#fee2e2"))  # Light red
                item.setForeground(QColor("#991b1b"))  # Dark red
            elif user.status == STATUS_NEED_SERVER:
                item.setBackground(QColor("#fef3c7"))  # Light amber
                item.setForeground(QColor("#92400e"))  # Dark amber
            elif user.status == STATUS_DONE_SERVER:
                item.setBackground(QColor("#dcfce7"))  # Light green
                item.setForeground(QColor("#166534"))  # Dark green
            
            # Add status as subtitle
            item.setText(f"{username}\n{user.status}")
            
            # Set item font
            font = QFont("Segoe UI", 9)
            item.setFont(font)
            
            self.users_list.addItem(item)
    
    def on_user_selected(self):
        """Handle user selection"""
        pass  # Could show user-specific info here
    
    def on_status_changed(self):
        """Handle status change"""
        self.current_status = self.status_combo.currentText()
        # Status is used in broadcasts
    
    def send_message(self):
        """Send message to all users"""
        message = self.msg_input.text().strip()
        if not message:
            return
        
        # Save to local database
        self.message_db.add_message(self.username, message)
        
        # Send to all online users
        users = self.discovery.get_online_users()
        for username, user in users.items():
            MessageClient.send_message(user.ip_address, self.username, message)
        
        # Clear input and refresh display
        self.msg_input.clear()
        self.load_messages()
    
    def on_message_received(self, message):
        """Handle received message"""
        if message.get('type') == 'message':
            sender = message.get('sender')
            content = message.get('content')
            
            if sender and content:
                self.message_db.add_message(sender, content)
                self.load_messages()
    
    def load_messages(self):
        """Load and display messages"""
        messages = self.message_db.get_messages(limit=50)
        
        self.chat_display.clear()
        
        # Build HTML for better message formatting
        html_content = '<div style="font-family: Segoe UI; font-size: 10pt;">'
        
        for sender, content, timestamp in messages:
            try:
                dt = datetime.fromisoformat(timestamp)
                time_str = dt.strftime("%H:%M")
            except:
                time_str = "??:??"
            
            # Make sender name colored
            sender_color = self._get_sender_color(sender)
            
            # Format: [HH:MM] Sender: Message
            html_content += f'<div style="margin-bottom: 8px; padding: 4px 0;">'
            html_content += f'<span style="color: #999; font-size: 9pt;">[{time_str}]</span> '
            html_content += f'<span style="color: {sender_color}; font-weight: bold;">{sender}:</span> '
            html_content += f'<span style="color: {THEME_TEXT};">{content}</span>'
            html_content += '</div>'
        
        html_content += '</div>'
        self.chat_display.setHtml(html_content)
        
        # Scroll to bottom
        scrollbar = self.chat_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def _get_sender_color(self, sender):
        """Generate a consistent color for a sender"""
        # Use hash to create consistent colors
        hash_val = hash(sender) % 6
        colors = [
            '#2563eb',  # Blue
            '#7c3aed',  # Purple
            '#db2777',  # Pink
            '#ea580c',  # Orange
            '#15803d',  # Green
            '#0891b2',  # Cyan
        ]
        return colors[hash_val]
    
    def closeEvent(self, event):
        """Clean up on close"""
        self.refresh_timer.stop()
        self.discovery.stop()
        self.message_server.stop()
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
