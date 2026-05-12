# Backend Integration Guide for Jarvis Ayurveda Frontend

This guide explains how to connect the React frontend with the Python Jarvis backend.

## Architecture Overview

```
┌─────────────────────┐
│  React Frontend     │
│ (http://localhost:3000)
│                     │
│  - Landing page     │
│  - Login/Signup     │
│  - Chat interface   │
│  - Send button      │
└──────────┬──────────┘
           │ API calls
           │ (axios)
           │
    ┌──────▼──────┐
    │  Vite Proxy │ (localhost:3000 → localhost:5000)
    └──────┬──────┘
           │ HTTP
           │
┌──────────▼─────────────┐
│ Flask/FastAPI Backend  │
│(http://localhost:5000) │
│                        │
│ - Auth endpoints       │
│ - Chat endpoints       │
│ - User endpoints       │
└──────────┬─────────────┘
           │
┌──────────▼─────────────────┐
│  Python Jarvis Brain        │
│                             │
│ - ai_brain_ayurveda.py      │
│ - TinyLlama 1.1B model      │
│ - Medical LoRA adapter      │
│ - Vosk STT                  │
│ - Dosha detection           │
└─────────────────────────────┘
```

## Frontend API Expectations

The frontend makes these API calls:

### Authentication Endpoints

#### POST /api/auth/signup
Create new user account

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "user_123",
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Email already registered"
}
```

---

#### POST /api/auth/login
Authenticate user and get token

**Request:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "user_123",
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Invalid credentials"
}
```

---

### Chat Endpoints

#### POST /api/chat
Send message and get Jarvis response

**Request:**
```json
{
  "message": "What should I eat for breakfast?"
}
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "message": "Based on your Dosha type, I recommend...",
  "timestamp": "2026-05-08T10:30:45Z",
  "dosha": "pitta"
}
```

---

#### GET /api/chat/history
Get previous messages

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "messages": [
    {
      "id": "msg_1",
      "type": "user",
      "content": "Hello",
      "timestamp": "2026-05-08T10:25:00Z"
    },
    {
      "id": "msg_2",
      "type": "bot",
      "content": "Namaste! How can I help you?",
      "timestamp": "2026-05-08T10:25:05Z"
    }
  ]
}
```

---

### User Endpoints

#### GET /api/user/profile
Get authenticated user information

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": "user_123",
    "name": "John Doe",
    "email": "john@example.com",
    "dosha": "pitta",
    "created_at": "2026-05-01T00:00:00Z"
  }
}
```

---

## Implementation Checklist

### Phase 1: Backend Setup

- [ ] Create Flask/FastAPI application
- [ ] Set up database (MongoDB recommended - see project structure)
- [ ] Create models for User, Message, Session
- [ ] Implement CORS support for `http://localhost:3000`

### Phase 2: Authentication

- [ ] Implement user registration endpoint
- [ ] Implement user login endpoint
- [ ] Add JWT token generation and validation
- [ ] Create authentication middleware
- [ ] Store hashed passwords (use bcrypt)
- [ ] Add token expiration logic

### Phase 3: Chat Integration

- [ ] Create chat message endpoint
- [ ] Integrate with existing `ai_brain_ayurveda.py`
- [ ] Add message history retrieval
- [ ] Implement chat session management
- [ ] Add Dosha detection endpoint

### Phase 4: Testing

- [ ] Test signup flow
- [ ] Test login flow
- [ ] Test chat messages
- [ ] Test token validation
- [ ] Test CORS headers
- [ ] Load test with multiple users

### Phase 5: Deployment

- [ ] Set up production database
- [ ] Configure environment variables
- [ ] Deploy backend server
- [ ] Test frontend-backend connection
- [ ] Monitor logs and errors

## Flask Implementation Example

### Step 1: Create Flask App

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Mock user database (use real database in production)
users = {}
```

### Step 2: Add Authentication Routes

```python
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    
    if email in users:
        return jsonify({'success': False, 'error': 'Email already registered'}), 400
    
    # In production: hash password with bcrypt
    users[email] = {
        'id': len(users) + 1,
        'name': name,
        'email': email,
        'password': password,  # Hash this!
    }
    
    token = jwt.encode(
        {'email': email, 'exp': datetime.utcnow() + timedelta(days=30)},
        app.config['SECRET_KEY']
    )
    
    return jsonify({
        'success': True,
        'token': token,
        'user': {
            'id': users[email]['id'],
            'name': name,
            'email': email
        }
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if email not in users or users[email]['password'] != password:
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    
    token = jwt.encode(
        {'email': email, 'exp': datetime.utcnow() + timedelta(days=30)},
        app.config['SECRET_KEY']
    )
    
    user = users[email]
    return jsonify({
        'success': True,
        'token': token,
        'user': {
            'id': user['id'],
            'name': user['name'],
            'email': email
        }
    })
```

### Step 3: Add Chat Routes

```python
from ai_brain_ayurveda import AyurvedicChatbot

# Initialize chatbot
chatbot = AyurvedicChatbot()

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')
    
    # Verify token
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        email = decoded['email']
    except:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    # Get response from Jarvis brain
    try:
        response = chatbot.ask_ayurveda(message)
        
        return jsonify({
            'success': True,
            'message': response,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'user': email
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/chat/history', methods=['GET'])
def chat_history():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    # Return empty history (store in database)
    return jsonify({
        'success': True,
        'messages': []
    })

@app.route('/api/user/profile', methods=['GET'])
def user_profile():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        email = decoded['email']
        user = users[email]
        
        return jsonify({
            'success': True,
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': email,
                'created_at': '2026-05-01T00:00:00Z'
            }
        })
    except:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Step 4: Update Frontend Stores

Edit `src/store/authStore.js`:

```javascript
import axios from 'axios'
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const API_BASE = process.env.VITE_API_BASE_URL || 'http://localhost:5000/api'

export const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: async (email, password) => {
        try {
          const response = await axios.post(`${API_BASE}/auth/login`, {
            email,
            password,
          })
          if (response.data.success) {
            set({
              user: response.data.user,
              token: response.data.token,
              isAuthenticated: true,
            })
            return response.data
          }
        } catch (error) {
          console.error('Login error:', error)
          throw error
        }
      },

      signup: async (name, email, password) => {
        try {
          const response = await axios.post(`${API_BASE}/auth/signup`, {
            name,
            email,
            password,
          })
          if (response.data.success) {
            set({
              user: response.data.user,
              token: response.data.token,
              isAuthenticated: true,
            })
            return response.data
          }
        } catch (error) {
          console.error('Signup error:', error)
          throw error
        }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        })
      },

      setUser: (user) => {
        set({ user })
      },
    }),
    {
      name: 'auth-store',
    }
  )
)
```

## Environment Variables

Create `.env` in project root:

```env
# Backend
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key-very-secure

# Database (if using MongoDB)
MONGODB_URI=mongodb://localhost:27017/jarvis_ayurveda

# Jarvis Config
DEVICE=-1
ADAPTER_PATH=models/medical-lora
AYURVEDA_MODE=true
```

## Testing the Integration

### 1. Start Backend
```bash
cd e:\Jarvis
python -m flask run --port 5000
```

### 2. Start Frontend
```bash
cd e:\Jarvis\frontend
npm run dev
```

### 3. Test Sign Up
1. Open http://localhost:3000/signup
2. Fill in name, email, password
3. Click Sign Up
4. Should redirect to chat

### 4. Test Login
1. Open http://localhost:3000/login
2. Use credentials from previous signup
3. Click Log In
4. Should redirect to chat

### 5. Test Chat
1. Type a message: "What is my dosha?"
2. Click Send button
3. Should get Jarvis response

### 6. Check Browser Console
- F12 to open Developer Tools
- Network tab to see API calls
- Console tab for any errors

## Common Issues

### CORS Error
**Error:** `Access to XMLHttpRequest has been blocked by CORS policy`

**Solution:** Add CORS to Flask:
```python
from flask_cors import CORS
CORS(app, origins=["http://localhost:3000"])
```

### Token Invalid
**Error:** `Unauthorized` 401

**Solution:** Ensure token is sent in header:
```javascript
axios.post('/api/chat', data, {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})
```

### Backend Not Responding
**Error:** `Failed to fetch` or `ERR_CONNECTION_REFUSED`

**Solution:** Ensure backend is running on port 5000:
```bash
python app.py  # or: flask run --port 5000
```

### Wrong Port
**Error:** Frontend and backend not connecting

**Solution:** Update `vite.config.js`:
```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      // ...
    }
  }
}
```

## Production Deployment

### Backend Deployment Options

1. **Heroku**
   ```bash
   heroku login
   heroku create jarvis-ayurveda-backend
   git push heroku main
   ```

2. **AWS EC2**
   - Launch EC2 instance
   - Install Python, Flask
   - Run with Gunicorn
   - Set up Nginx reverse proxy

3. **DigitalOcean**
   - Create Droplet
   - Deploy Docker container
   - Set up Nginx

4. **PythonAnywhere**
   - Upload files
   - Configure web app
   - Enable reload

### Frontend Deployment Options

1. **Vercel** (Recommended for Vite)
   ```bash
   npm install -g vercel
   vercel --prod
   ```

2. **Netlify**
   - Connect GitHub repo
   - Set build command: `npm run build`
   - Set publish directory: `dist`

3. **GitHub Pages**
   ```bash
   npm run build
   # Deploy dist/ folder
   ```

## Security Considerations

1. **Password Hashing**
   ```python
   import bcrypt
   hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
   ```

2. **HTTPS Only** - Use SSL certificates in production

3. **Token Expiration** - Set short expiry times

4. **Rate Limiting** - Prevent abuse
   ```python
   from flask_limiter import Limiter
   ```

5. **Input Validation** - Sanitize all inputs

6. **Environment Variables** - Never commit secrets

## Next Steps

1. ✅ Frontend ready at localhost:3000
2. ⬜ Create Flask backend with auth endpoints
3. ⬜ Integrate with `ai_brain_ayurveda.py`
4. ⬜ Test full stack integration
5. ⬜ Deploy to production

---

For questions, check:
- [FRONTEND_SETUP.md](../FRONTEND_SETUP.md)
- [frontend/README.md](./README.md)
- [Python Backend Files](../ai_brain_ayurveda.py)
