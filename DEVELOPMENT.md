# Development Guide - Server Activity Monitor

## Development Environment Setup

### Prerequisites
- Windows 11
- Python 3.8+
- Git (optional)

### Initial Setup
```bash
# Clone or extract the repository
cd User-Activity-Monitoring

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Project Structure

```
User-Activity-Monitoring/
├── src/                      # Source code
│   ├── main.py              # GUI application (main entry point)
│   ├── config.py            # Configuration management
│   ├── network_discovery.py # Network discovery implementation
│   ├── messaging.py         # Message sending/receiving
│   └── database.py          # SQLite database wrapper
├── run.py                   # Python entry point
├── run.bat                  # Windows launcher
├── setup.bat                # Setup script
├── build.bat                # Build script for exe
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore file
├── README.md               # User documentation
├── QUICKSTART.md           # Quick start guide
├── TECHNICAL.md            # Technical documentation
├── BUILD.md                # Build instructions
└── DEVELOPMENT.md          # This file
```

## Running in Development Mode

### Method 1: Direct Python (Recommended for Development)
```bash
cd src
python main.py
```

### Method 2: Using Entry Point
```bash
python run.py
```

### Method 3: Using Batch File
```bash
run.bat
```

## Code Organization

### Adding New Features

#### Example 1: Adding a New Status Option
1. Edit `src/config.py`:
```python
STATUS_NEW_STATUS = 'New status text'
VALID_STATUSES = [STATUS_NEED_SERVER, STATUS_USING_SERVER, STATUS_DONE_SERVER, STATUS_NEW_STATUS]
```

2. Edit `src/main.py` - the status dropdown updates automatically via `VALID_STATUSES`

#### Example 2: Adding a New UI Panel
1. Create new method in `MainWindow` class in `src/main.py`:
```python
def create_new_panel(self):
    """Create a new UI panel"""
    panel_layout = QVBoxLayout()
    # Add widgets
    return panel_layout
```

2. Add to `init_ui()` method:
```python
main_layout.addLayout(self.create_new_panel())
```

#### Example 3: Adding a New Message Type
1. Define in `src/messaging.py`:
```python
# Modify MessageClient.send_message to accept type parameter
def send_message(ip_address, sender, message, msg_type='message'):
    msg_obj = {
        'type': msg_type,  # 'message', 'status_update', etc.
        'sender': sender,
        'content': message,
        'timestamp': datetime.now().isoformat()
    }
```

2. Handle in `src/main.py`:
```python
def on_message_received(self, message):
    msg_type = message.get('type')
    if msg_type == 'message':
        # Handle chat message
        pass
    elif msg_type == 'status_update':
        # Handle status update
        pass
```

## Debugging

### Enable Debug Output
Edit `src/main.py` and add logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"Users discovered: {users}")
```

### Test Network Discovery
Create `test_discovery.py`:
```python
import sys
sys.path.insert(0, 'src')
from network_discovery import NetworkDiscovery

d = NetworkDiscovery("TestUser")
d.start()
print("Waiting for users...")
import time
time.sleep(10)
users = d.get_online_users()
print(f"Found users: {users}")
d.stop()
```

Run: `python test_discovery.py`

### Test Database
Create `test_db.py`:
```python
import sys
sys.path.insert(0, 'src')
from database import MessageDatabase

db = MessageDatabase()
db.add_message("TestUser", "Hello")
messages = db.get_messages()
for sender, msg, timestamp in messages:
    print(f"{sender}: {msg}")
```

Run: `python test_db.py`

## Key Classes and Methods

### NetworkDiscovery
```python
# Methods
discovery.start()                    # Start discovery
discovery.stop()                     # Stop discovery
discovery.get_online_users()        # Get dict of online users
discovery.update_status(status)      # Update user status

# Callbacks
on_discovery_update()                # Called when users change
```

### User
```python
user.username                        # User's name
user.ip_address                      # IP address
user.status                          # Current status
user.last_seen                       # Last activity time
user.is_online(timeout_seconds=15)   # Check if online
```

### MessageServer
```python
# Methods
server.start()                       # Start server
server.stop()                        # Stop server

# Constructor
MessageServer(username, on_message_callback)
```

### MessageDatabase
```python
# Methods
db.add_message(sender, message)      # Add message
db.get_messages(limit=100)           # Retrieve messages
db.init_db()                         # Initialize database
```

## Testing Checklist

Before committing changes:
- [ ] Application starts without errors
- [ ] User name entry dialog appears on first run
- [ ] GUI renders correctly
- [ ] Can change status
- [ ] Can send messages
- [ ] Messages appear in chat
- [ ] No crashes on close
- [ ] User data persists between runs

## Performance Optimization Tips

### If CPU Usage is High
1. Check UI refresh rate in `main.py`:
```python
self.refresh_timer.start(2000)  # Increase interval if needed
```

2. Check broadcast frequency in `network_discovery.py`:
```python
# Increase DISCOVERY_INTERVAL in config.py
DISCOVERY_INTERVAL = 10  # seconds
```

### If Memory Usage Grows
1. Limit message history:
```python
# In database.py, limit query
db.get_messages(limit=50)  # Instead of 100
```

2. Clean old messages from SQLite:
```python
# Add to database.py
def delete_old_messages(self, days=30):
    cutoff = datetime.now() - timedelta(days=days)
    conn = sqlite3.connect(str(self.db_path))
    cursor = conn.cursor()
    cursor.execute('DELETE FROM messages WHERE timestamp < ?', (cutoff.isoformat(),))
    conn.commit()
    conn.close()
```

## Building Executable

### Create .exe for Distribution
```bash
pip install pyinstaller
build.bat
```

Output: `dist\ServerActivityMonitor.exe`

### Size Optimization
Edit `build.bat` to strip debug symbols:
```batch
pyinstaller --onefile --windowed --strip ^
    --hidden-import=PyQt5 ^
    src/main.py
```

## Extending for Other Platforms

### macOS Support
```bash
# Install dependencies
pip install -r requirements.txt

# Run
python run.py

# Build app bundle
pyinstaller --onefile --windowed src/main.py
```

### Linux Support
```bash
# Install Qt5 libraries
sudo apt-get install python3-pyqt5

# Run
python3 run.py

# Build
pyinstaller --onefile --windowed src/main.py
```

## Version Control

### Recommended .gitignore Additions
Already included in `.gitignore`:
- `__pycache__/`
- `*.pyc`
- `build/`
- `dist/`
- `.venv/`

### Commit Workflow
```bash
git add .
git commit -m "Feature: Add new status option"
git push
```

## Contributing Guidelines

### Code Style
- Use Python 3.8+ syntax
- PEP 8 formatting
- Meaningful variable names
- Add docstrings to functions

### Example Function
```python
def get_user_status(username):
    """
    Retrieve the current status of a user.
    
    Args:
        username (str): Name of the user
    
    Returns:
        str: Current status or None if not found
    """
    users = discovery.get_online_users()
    return users.get(username).status if username in users else None
```

## Known Limitations and Future Work

### Current Limitations
- UDP-only (no TCP fallback)
- No message encryption
- No persistent user data (except chat)
- Limited to local network

### Planned Enhancements
- [ ] Persistent user status
- [ ] Message search functionality
- [ ] File sharing
- [ ] User profiles
- [ ] Admin dashboard
- [ ] Cloud sync option

## Troubleshooting Development

### "Module not found" errors
```bash
# Ensure src is in path
set PYTHONPATH=%PYTHONPATH%;.\src
python -c "from config import *"
```

### PyQt5 not loading
```bash
# Reinstall PyQt5
pip install --force-reinstall PyQt5
```

### Port already in use
```bash
# Check what's using port 27001
netstat -ano | find "27001"
# Kill process if needed
taskkill /PID <PID> /F
```

## Contact & Support

For development questions, refer to:
- TECHNICAL.md - Architecture details
- README.md - Feature documentation
- Code comments - Implementation details

---

**Happy coding!**
