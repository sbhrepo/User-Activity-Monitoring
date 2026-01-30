# Server Activity Monitor - Windows 11

A lightweight network application for monitoring server usage and team communication.

## Features

✅ **Automatic Network Discovery** - Find other users running the app on your local network (no network scanning required)
✅ **Status Management** - Display your server status:
   - "I need the server"
   - "I'm using the server"  
   - "I'm done using the server"
✅ **Real-time Chat** - Send and receive messages with other users
✅ **GUI Interface** - Clean, easy-to-use graphical interface
✅ **Data Persistence** - Messages are stored locally
✅ **No Central Server Required** - Uses UDP broadcast for peer-to-peer discovery

## Requirements

- Windows 11
- Python 3.8 or higher
- PyQt5

## Installation

### Option 1: Automatic Setup
1. Download or extract the application folder
2. Run `setup.bat` to install dependencies
3. Run `run.bat` to start the application

### Option 2: Manual Setup
1. Install Python 3.8+ from https://www.python.org/
2. Open Command Prompt in the application folder
3. Run: `pip install -r requirements.txt`
4. Run: `python run.py`

## Usage

### First Run
- Enter your name to identify yourself on the network
- This will be saved for future runs

### Main Interface
1. **Status Selection** - Select your current server status from the dropdown
2. **Users List** - View all users currently running the application on your network
3. **Chat Box** - Send messages to other users and view their messages

### How Network Discovery Works
The application uses **UDP broadcast** on your local network subnet:
- No network scanning needed
- Lightweight and efficient
- Works within your local network (LAN)
- Users are automatically discovered when they start the app
- Users disappear from the list after 15 seconds of inactivity

## How to Deploy

### Single Machine
1. Run setup.bat on the target machine
2. Run run.bat to start the application

### Multiple Machines
1. Copy the entire application folder to each machine
2. Run setup.bat on each machine
3. Run run.bat on each machine
4. All users on the same local network will automatically discover each other

### Create Shortcut
- Right-click `run.bat` → Send to → Desktop (create shortcut)
- Users can double-click the shortcut to launch

## File Structure

```
Server-Activity-Monitor/
├── src/
│   ├── main.py              # Main GUI application
│   ├── config.py            # Configuration and settings
│   ├── network_discovery.py # UDP broadcast discovery
│   ├── messaging.py         # Message sending/receiving
│   └── database.py          # Local message storage
├── requirements.txt         # Python dependencies
├── setup.bat               # Automated setup script
├── run.bat                 # Application launcher
├── run.py                  # Main entry point
└── README.md               # This file
```

## Data Location

All application data is stored in:
- `%APPDATA%\ServerActivityMonitor\`
- User configuration: `user_config.json`
- Messages database: `messages.db`

## Troubleshooting

### "Python is not installed"
- Install Python 3.8+ from https://www.python.org/
- Make sure to check "Add Python to PATH" during installation

### Can't see other users
- Ensure all users are on the same local network (LAN)
- Check Windows Firewall settings - UDP port 27001 and 27002 should be allowed
- All users must have the application running

### Messages not appearing
- Ensure users are on the same network
- Check that local firewall allows UDP on ports 27001 and 27002
- Messages are stored locally even if network fails

## Network Ports

- **UDP Port 27001** - Discovery broadcasts
- **UDP Port 27002** - Message transmission

These ports must be open in your local network. Most corporate networks allow these by default.

## Security Notes

- This application is designed for local network use only
- No encryption is used (suitable for trusted networks)
- Messages are stored in plain text locally
- For sensitive data, use encrypted communication channels

## Version

Server Activity Monitor v1.0.0

## Support

For issues or questions, check the README.md or examine the application logs in the data directory.
