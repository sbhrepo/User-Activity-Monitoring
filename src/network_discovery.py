"""Network discovery module using UDP broadcast"""
import socket
import json
import threading
from datetime import datetime, timedelta
from config import BROADCAST_PORT, BROADCAST_ADDRESS, BROADCAST_TIMEOUT, DISCOVERY_INTERVAL

class User:
    """Represents a user on the network"""
    def __init__(self, username, ip_address, status):
        self.username = username
        self.ip_address = ip_address
        self.status = status
        self.last_seen = datetime.now()
    
    def is_online(self, timeout_seconds=15):
        """Check if user is still online based on last seen time"""
        return (datetime.now() - self.last_seen).total_seconds() < timeout_seconds
    
    def __repr__(self):
        return f"User({self.username}, {self.ip_address}, {self.status})"


class NetworkDiscovery:
    """Handles network discovery and user detection"""
    
    def __init__(self, username, status_callback=None):
        self.username = username
        self.users = {}  # username -> User object
        self.status_callback = status_callback
        self.running = False
        self.discovery_thread = None
        self.listening_thread = None
    
    def start(self):
        """Start network discovery"""
        if self.running:
            return
        
        self.running = True
        
        # Start listening for broadcasts
        self.listening_thread = threading.Thread(target=self._listen_for_broadcasts, daemon=True)
        self.listening_thread.start()
        
        # Start sending discovery broadcasts
        self.discovery_thread = threading.Thread(target=self._send_broadcasts, daemon=True)
        self.discovery_thread.start()
    
    def stop(self):
        """Stop network discovery"""
        self.running = False
        if self.discovery_thread:
            self.discovery_thread.join(timeout=2)
        if self.listening_thread:
            self.listening_thread.join(timeout=2)
    
    def update_status(self, status):
        """Update local user status and broadcast it"""
        # This will be broadcast in the next discovery cycle
        pass
    
    def _send_broadcasts(self):
        """Send discovery broadcasts periodically"""
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                
                # Enable broadcasting
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                
                message = {
                    'type': 'discovery',
                    'username': self.username,
                    'timestamp': datetime.now().isoformat()
                }
                
                sock.sendto(
                    json.dumps(message).encode(),
                    (BROADCAST_ADDRESS, BROADCAST_PORT)
                )
                sock.close()
            except Exception as e:
                print(f"Error sending broadcast: {e}")
            
            # Wait before next broadcast
            for _ in range(DISCOVERY_INTERVAL * 10):
                if not self.running:
                    break
                threading.Event().wait(0.1)
    
    def _listen_for_broadcasts(self):
        """Listen for discovery broadcasts from other users"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind(('', BROADCAST_PORT))
            sock.settimeout(1)
            
            while self.running:
                try:
                    data, addr = sock.recvfrom(1024)
                    message = json.loads(data.decode())
                    
                    if message.get('type') == 'discovery':
                        username = message.get('username')
                        if username and username != self.username:
                            # Update user record
                            if username not in self.users:
                                self.users[username] = User(username, addr[0], '')
                            else:
                                self.users[username].last_seen = datetime.now()
                                self.users[username].ip_address = addr[0]
                            
                            if self.status_callback:
                                self.status_callback()
                except socket.timeout:
                    pass
                except Exception as e:
                    print(f"Error receiving broadcast: {e}")
        
        except Exception as e:
            print(f"Error in listen loop: {e}")
        finally:
            try:
                sock.close()
            except:
                pass
    
    def get_online_users(self):
        """Get list of online users"""
        # Remove offline users
        self.users = {
            username: user for username, user in self.users.items()
            if user.is_online()
        }
        return self.users
