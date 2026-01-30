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
    STATUS_NEED_SERVER, STATUS_USING_SERVER, STATUS_DONE_SERVER, VALID_STATUSES
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
        self.setWindowTitle("User Name Setup")
        self.setModal(True)
        self.setGeometry(100, 100, 400, 150)
        
        layout = QVBoxLayout()
        
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
        ok_btn = QPushButton("Continue")
        ok_btn.clicked.connect(self.accept)
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
        
        # Central widget
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Top section: Status control
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Your Status:"))
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(VALID_STATUSES)
        self.status_combo.setCurrentText(self.current_status)
        self.status_combo.currentTextChanged.connect(self.on_status_changed)
        status_layout.addWidget(self.status_combo)
        status_layout.addStretch()
        
        main_layout.addLayout(status_layout)
        
        # Middle section: Users and Chat
        content_layout = QHBoxLayout()
        
        # Left panel: Users list
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Users on Network:"))
        
        self.users_list = QListWidget()
        self.users_list.itemSelectionChanged.connect(self.on_user_selected)
        left_layout.addWidget(self.users_list)
        
        content_layout.addLayout(left_layout, 1)
        
        # Right panel: Chat
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Chat:"))
        
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Courier", 9))
        right_layout.addWidget(self.chat_display)
        
        # Message input
        msg_layout = QHBoxLayout()
        self.msg_input = QLineEdit()
        self.msg_input.setPlaceholderText("Type message and press Enter...")
        self.msg_input.returnPressed.connect(self.send_message)
        msg_layout.addWidget(self.msg_input)
        
        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.send_message)
        send_btn.setMaximumWidth(80)
        msg_layout.addWidget(send_btn)
        
        right_layout.addLayout(msg_layout)
        
        content_layout.addLayout(right_layout, 1)
        
        main_layout.addLayout(content_layout, 1)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
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
            self.users_list.addItem(QListWidgetItem("No other users online"))
            return
        
        for username, user in sorted(users.items()):
            item_text = f"{username}\n({user.status})"
            item = QListWidgetItem(item_text)
            
            # Color code by status
            if user.status == STATUS_USING_SERVER:
                item.setBackground(QColor("#ffcccc"))
            elif user.status == STATUS_NEED_SERVER:
                item.setBackground(QColor("#ffffcc"))
            elif user.status == STATUS_DONE_SERVER:
                item.setBackground(QColor("#ccffcc"))
            
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
        
        for sender, content, timestamp in messages:
            try:
                dt = datetime.fromisoformat(timestamp)
                time_str = dt.strftime("%H:%M:%S")
            except:
                time_str = "??:??:??"
            
            msg_line = f"[{time_str}] {sender}: {content}\n"
            self.chat_display.append(msg_line)
    
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
