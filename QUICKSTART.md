# Quick Start Guide - Server Activity Monitor

## 5-Minute Setup

### Step 1: Install (1 minute)
1. Download the application folder
2. Right-click `setup.bat` → **Run as Administrator**
3. Wait for installation to complete
4. A command window will show "Installation complete!"

### Step 2: First Run (1 minute)
- Double-click `run.bat`
- Enter your name (e.g., "John")
- Click "Continue"
- The application window opens

### Step 3: Invite Others (3 minutes)
- Copy the application folder to other computers on your **local network**
- Run `setup.bat` on each computer
- Run `run.bat` on each computer
- Each user enters their own name
- **Within 10 seconds, all users appear in each other's User List!**

## How It Works

```
Your Computer            Network              Other Computer
     │                     │                        │
     ├─ Run app ─────► Broadcast "Hi, I'm John" ──────►│
     │                     │                        │
     │◄─ Receive "Hi, I'm Alice" ────────────────────┤
     │                     │                        │
  Display Alice            │      Display John
  in user list             │      in user list
```

## Common Tasks

### Change Your Status
1. Click the dropdown next to "Your Status:"
2. Select one of:
   - "I need the server"
   - "I'm using the server"
   - "I'm done using the server"
3. **Automatically updates across all users!**

### Send a Message
1. Type in the message box at the bottom
2. Press **Enter** or click **Send**
3. Message appears in chat for all users
4. Messages are saved so they persist

### See Who's Using the Server
- Look at the **Users on Network** list
- Color coding shows status:
  - 🟡 Yellow = "I need the server"
  - 🔴 Red = "I'm using the server"
  - 🟢 Green = "I'm done using the server"

## Troubleshooting

### "Can't see other users"
**Checklist:**
- [ ] Other computers are on the **same Wi-Fi/Network**
- [ ] All apps have been running for **at least 10 seconds**
- [ ] Windows Firewall isn't blocking the app
  - Check: Settings → Firewall → Allow an app through firewall

**Fix:** If still not working, restart the app on each computer.

### "Python not found"
- Visit https://www.python.org/downloads/
- Download Python 3.8 or higher
- During installation, **CHECK** the box "Add Python to PATH"
- Restart your computer
- Run `setup.bat` again

### "Messages not appearing"
- Check that all users are on **same local network**
- If using corporate network, ask IT if UDP ports 27001-27002 are allowed
- Messages are saved locally (check Chat box history)

## Network Requirements

✅ Works on:
- Home Wi-Fi
- Office LAN
- Ethernet network
- VPN (if all users on same VPN)

❌ Doesn't work across:
- The Internet (between offices)
- Different networks
- 4G/5G networks

**Local Network = Same Wi-Fi or Connected to Same Router**

## Uninstall

1. Delete the application folder
2. Optional: Delete `%APPDATA%\ServerActivityMonitor` to remove messages

## Tips

- **Keep running**: Leave the app running so others can see you
- **Messages persist**: Close and reopen, old messages still there
- **Automatic discovery**: New users join automatically, no setup needed
- **Lightweight**: Uses very little CPU/internet

## Next Steps

- Read [README.md](README.md) for detailed features
- Read [TECHNICAL.md](TECHNICAL.md) for how it works
- Read [BUILD.md](BUILD.md) to create .exe installer for distribution

---

**Need Help?** Check the README.md or TECHNICAL.md files for more information.
