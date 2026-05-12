"""
User Authentication Manager
Handles user registration, login, and session management
"""

import json
import hashlib
import os
from datetime import datetime
from typing import Optional, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class AuthManager:
    """Manages user authentication"""
    
    DB_FILE = "users_data.json"
    
    def __init__(self):
        self.users = self._load_users()
    
    def _load_users(self) -> Dict:
        """Load users from database"""
        if os.path.exists(self.DB_FILE):
            try:
                with open(self.DB_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_users(self):
        """Save users to database"""
        try:
            with open(self.DB_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save users: {e}")
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(
        self,
        username: str,
        email: str,
        password: str,
        full_name: str = "",
        dosha: str = "",
        constitution: str = "",
        dosha_source: str = "signup",
    ) -> Tuple[bool, str]:
        """
        Register a new user
        Returns: (success, message)
        """
        # Validation
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        if not email or '@' not in email:
            return False, "Invalid email address"
        
        if username in self.users:
            return False, "Username already exists"
        
        # Check if email already registered
        for user_data in self.users.values():
            if user_data.get('email') == email:
                return False, "Email already registered"
        
        # Create user
        self.users[username] = {
            'email': email,
            'password': self._hash_password(password),
            'full_name': full_name,
            'created_at': datetime.now().isoformat(),
            'dosha': dosha or None,
            'dosha_source': dosha_source,
            'constitution': constitution,
            'chat_history': [],
            'preferences': {}
        }
        
        self._save_users()
        logger.info(f"User registered: {username}")
        return True, "Registration successful!"
    
    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Login user
        Returns: (success, message)
        """
        # Backward-compatible login:
        # - new flow uses email as username key
        # - older data may store a non-email username with email field
        user = self.users.get(username)
        if user is None:
            for key, value in self.users.items():
                if value.get("email", "").strip().lower() == username.strip().lower():
                    username = key
                    user = value
                    break

        if user is None:
            return False, "Invalid email or password"

        if user['password'] != self._hash_password(password):
            return False, "Invalid email or password"
        
        logger.info(f"User logged in: {username}")
        return True, "Login successful!"
    
    def get_user(self, username: str) -> Optional[Dict]:
        """Get user data"""
        return self.users.get(username)

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user data by email address"""
        for user in self.users.values():
            if user.get('email') == email:
                return user
        return None
    
    def update_user_dosha(self, username: str, dosha: str, dosha_source: str = "detected"):
        """Update user's detected dosha"""
        if username in self.users:
            self.users[username]['dosha'] = dosha
            self.users[username]['dosha_source'] = dosha_source
            self._save_users()

    def append_chat_history(self, username: str, user_message: str, assistant_message: str):
        """Append a chat turn to the user profile"""
        if username not in self.users:
            return

        history = self.users[username].setdefault('chat_history', [])
        history.append({
            'user': user_message,
            'assistant': assistant_message,
            'timestamp': datetime.now().isoformat(),
        })
        self._save_users()
    
    def update_user_preferences(self, username: str, preferences: Dict):
        """Update user preferences"""
        if username in self.users:
            self.users[username]['preferences'].update(preferences)
            self._save_users()
    
    def user_exists(self, username: str) -> bool:
        """Check if user exists"""
        return username in self.users
    
    def get_user_full_name(self, username: str) -> str:
        """Get user's full name"""
        if username in self.users:
            return self.users[username].get('full_name', username)
        return username
