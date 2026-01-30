# Installation Checklist

## Pre-Installation
- [ ] Windows 11 operating system
- [ ] Network access (Wi-Fi or Ethernet)
- [ ] Administrator access (for first-time setup)
- [ ] 500 MB free disk space
- [ ] All target computers on same network

## Installation Verification

### Computer 1
- [ ] Run `setup.bat` completes without errors
- [ ] Run `run.bat` opens application window
- [ ] Enter name and click "Continue"
- [ ] Application window shows empty user list (normal at start)
- [ ] Close application (Alt+F4 or X button)

### Computer 2
- [ ] Copy application folder from Computer 1
- [ ] Run `setup.bat`
- [ ] Run `run.bat`
- [ ] Enter a different name
- [ ] **Within 10 seconds**, you should see "Computer1's Name" in the Users list
- [ ] Computer 1 should see "Computer2's Name" in its list

### Both Computers
- [ ] Computer 1: Change status - verify Computer 2 sees the change
- [ ] Computer 2: Change status - verify Computer 1 sees the change
- [ ] Computer 1: Type message, press Enter
- [ ] Computer 2: Verify message appears in chat
- [ ] Computer 2: Send message back
- [ ] Computer 1: Verify message appears
- [ ] Both: Close apps and restart - messages should still be there

## Firewall Configuration (If needed)

### Windows Defender Firewall
- [ ] Open Windows Defender Firewall with Advanced Security
- [ ] Click "Inbound Rules" in left panel
- [ ] Click "New Rule" in right panel
- [ ] Select "Port" → Next
- [ ] Select "UDP" and enter ports: 27001,27002
- [ ] Select "Allow" → Next → Next
- [ ] Name: "Server Activity Monitor" → Finish
- [ ] Repeat for Outbound Rules

**OR** (Easier)
- [ ] Search: "Allow an app through firewall"
- [ ] Click "Allow another app"
- [ ] Browse to `run.bat` and add it
- [ ] Make sure "Private" is checked
- [ ] Restart application

## Deployment Verification

### Small Team (5 computers)
- [ ] Each computer: run setup.bat and run.bat
- [ ] Each user enters different name
- [ ] Wait 15 seconds
- [ ] All computers: verify seeing 4 other users
- [ ] All computers: try sending messages
- [ ] All computers: change status and verify others see it

### Large Team (20+ computers)
- [ ] Pre-test with 5 computers first
- [ ] Create network copy of application
- [ ] Verify each new computer can discover existing ones
- [ ] Check network performance (should be minimal)

## Post-Installation

- [ ] Create shortcut to `run.bat` on each Desktop
- [ ] Send QUICKSTART.md to all users
- [ ] Set up internal documentation
- [ ] Schedule team training (optional)
- [ ] Gather feedback and suggestions

## Troubleshooting Checklist

### If users can't see each other:
- [ ] Verify ping works between computers (use Windows Command Prompt)
  ```
  ping [other-computer-ip]
  ```
- [ ] Check Firewall is not blocking application
- [ ] Restart both applications
- [ ] Try different network (test with hotspot)

### If installation fails:
- [ ] Check Python version: `python --version` (should be 3.8+)
- [ ] Reinstall dependencies: Delete folder and re-run setup.bat
- [ ] Check disk space
- [ ] Disable antivirus temporarily and try again

### If messages don't appear:
- [ ] Verify both users online (check user list)
- [ ] Ensure message wasn't filtered by firewall
- [ ] Check timestamps in chat (message may have been sent earlier)
- [ ] Restart application

## Maintenance Tasks

### Weekly
- [ ] Verify application still running on key machines
- [ ] Check for any error messages

### Monthly
- [ ] Backup configuration folder: `%APPDATA%\ServerActivityMonitor`
- [ ] Archive old messages if needed
- [ ] Gather feedback from users

### As Needed
- [ ] Update application (copy new version to all computers)
- [ ] Add new statuses or features
- [ ] Troubleshoot network issues

## Success Criteria - Full Checklist

### Functionality
- [ ] Users automatically discover each other
- [ ] Status changes visible in real-time
- [ ] Messages sent and received successfully
- [ ] Chat history persists
- [ ] Color coding matches status

### Performance
- [ ] Application uses minimal CPU (<1% idle)
- [ ] Memory usage reasonable (~100 MB)
- [ ] No noticeable network lag
- [ ] No crashes during normal use

### Usability
- [ ] First-time setup intuitive
- [ ] User interface clear and responsive
- [ ] Status dropdown easy to change
- [ ] Chat box easy to use
- [ ] Users list easy to read

### Reliability
- [ ] Application recovers from network interruptions
- [ ] Works after computer sleep/wake
- [ ] Survives app restart
- [ ] Works on multiple network types

## Documentation Checklist

For each location/team:
- [ ] Distribute README.md to all users
- [ ] Distribute QUICKSTART.md to all users
- [ ] Post TECHNICAL.md for IT team
- [ ] Archive DEVELOPMENT.md for future modifications
- [ ] Save these checklists for reference

## Deployment Complete When:

✅ All users on all computers can see each other  
✅ All users can successfully send and receive messages  
✅ All users can change status and see changes reflected  
✅ No critical errors reported  
✅ Users report comfortable with the interface  

---

**Date Deployed:** _______________  
**Deployed By:** _______________  
**Number of Computers:** _______________  
**Team Name/Location:** _______________  
**Support Contact:** _______________  

For support, refer to [TECHNICAL.md](TECHNICAL.md) for IT and [QUICKSTART.md](QUICKSTART.md) for users.
