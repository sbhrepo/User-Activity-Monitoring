"""Messaging module for local network communication"""
import socket
import json
import threading
from datetime import datetime
from config import MESSAGE_PORT

class MessageServer:
    """Server for receiving messages"""
    
    def __init__(self, username, on_message_callback=None):
        self.username = username
        self.on_message_callback = on_message_callback
        self.running = False
        self.server_thread = None
        self.server_socket = None
    
    def start(self):
        """Start message server"""
        if self.running:
            return
        
        self.running = True
        self.server_thread = threading.Thread(target=self._server_loop, daemon=True)
        self.server_thread.start()
    
    def stop(self):
        """Stop message server"""
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        if self.server_thread:
            self.server_thread.join(timeout=2)
    
    def _server_loop(self):
        """Main server loop for receiving messages"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('', MESSAGE_PORT))
            self.server_socket.settimeout(1)
            
            while self.running:
                try:
                    data, addr = self.server_socket.recvfrom(4096)
                    message = json.loads(data.decode())
                    
                    if self.on_message_callback:
                        self.on_message_callback(message)
                
                except socket.timeout:
                    pass
                except Exception as e:
                    print(f"Error receiving message: {e}")
        
        except Exception as e:
            print(f"Error starting message server: {e}")


class MessageClient:
    """Client for sending messages"""
    
    @staticmethod
    def send_message(ip_address, sender, message):
        """Send a message to another user"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            msg_obj = {
                'type': 'message',
                'sender': sender,
                'content': message,
                'timestamp': datetime.now().isoformat()
            }
            
            sock.sendto(
                json.dumps(msg_obj).encode(),
                (ip_address, MESSAGE_PORT)
            )
            sock.close()
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
