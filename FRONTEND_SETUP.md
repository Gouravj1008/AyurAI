# Jarvis Ayurveda - React Frontend Setup Guide

This guide will help you set up and run the React frontend for the Jarvis Ayurveda chatbot.

## Quick Start (3 minutes)

### Windows Users
1. Navigate to the frontend folder: `cd e:\Jarvis\frontend`
2. Double-click `setup.bat`
3. Wait for installation to complete
4. Run `npm run dev`
5. Open `http://localhost:3000` in your browser

### Mac/Linux Users
1. Navigate to the frontend folder: `cd e/Jarvis/frontend`
2. Run `bash setup.sh`
3. Wait for installation to complete
4. Run `npm run dev`
5. Open `http://localhost:3000` in your browser

## Manual Setup

### Prerequisites

Ensure you have installed:
- **Node.js** 16 or higher ([Download](https://nodejs.org/))
- **npm** (comes with Node.js)

Check installation:
```bash
node --version
npm --version
```

### Step 1: Navigate to Frontend Directory

```bash
cd e:\Jarvis\frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

This may take 2-5 minutes depending on your internet speed.

### Step 3: Create Environment File

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Edit `.env` if needed (for most cases, defaults are fine):
```env
VITE_API_BASE_URL=http://localhost:5000/api
```

### Step 4: Start Development Server

```bash
npm run dev
```

You should see:
```
VITE v5.0.8  ready in 234 ms

➜  Local:   http://localhost:3000/
➜  press h to show help
```

### Step 5: Open in Browser

Open `http://localhost:3000` in your web browser.

## Available Commands

### Development
```bash
npm run dev          # Start development server (http://localhost:3000)
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
```

## Project Pages

After starting the server, you can access:

- **Home/Landing** - `http://localhost:3000/`
- **Login** - `http://localhost:3000/login`
- **Sign Up** - `http://localhost:3000/signup`
- **Chat** - `http://localhost:3000/chat` (requires login)

### Demo Credentials

On the login page, click "Demo: Click to fill demo credentials" to auto-fill test credentials.

- Email: `demo@example.com`
- Password: `demo123`

## File Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatMessage.jsx       # Message component
│   │   └── Sidebar.jsx           # Chat sidebar
│   ├── pages/
│   │   ├── Landing.jsx           # Landing page
│   │   ├── Login.jsx             # Login page
│   │   ├── Signup.jsx            # Signup page
│   │   └── Chat.jsx              # Chat interface
│   ├── store/
│   │   └── authStore.js          # Auth state management
│   ├── App.jsx                   # Main app component
│   ├── main.jsx                  # Entry point
│   └── index.css                 # Tailwind styles
├── index.html                    # HTML template
├── package.json                  # Dependencies
├── vite.config.js               # Vite config
├── tailwind.config.js           # Tailwind config
├── .env.example                 # Example environment
└── README.md                    # Frontend README
```

## Features

### ✅ Implemented
- [x] Landing page with features showcase
- [x] Beautiful login page with validation
- [x] Signup page with form validation
- [x] ChatGPT-style chat interface
- [x] Send button for messages
- [x] Message display with timestamps
- [x] User sidebar with chat history
- [x] Responsive design (mobile-friendly)
- [x] Dark theme UI
- [x] User authentication state management
- [x] Auto-scroll to latest messages
- [x] Loading indicators

### 📋 Todo - Connect to Backend
- [ ] Connect login API
- [ ] Connect signup API
- [ ] Connect chat messages to Jarvis backend
- [ ] Display actual Dosha assessment
- [ ] Show real wellness plans
- [ ] Save chat history to database
- [ ] User profile management

## Connecting to Backend

### Setting up Backend API

The frontend expects the backend to run on `http://localhost:5000`.

Update your backend to have these endpoints:

```
POST   /api/auth/login       - Login user
POST   /api/auth/signup      - Register user
POST   /api/chat             - Send message
GET    /api/chat/history     - Get chat history
POST   /api/dosha/detect     - Detect Dosha
GET    /api/user/profile     - Get user info
```

### Backend Response Format

**Login Response:**
```json
{
  "success": true,
  "token": "jwt-token-here",
  "user": {
    "id": "user-id",
    "email": "user@example.com",
    "name": "User Name"
  }
}
```

**Chat Response:**
```json
{
  "success": true,
  "message": "Bot response text",
  "timestamp": "2026-05-08T10:30:00Z"
}
```

## Troubleshooting

### "Port 3000 is already in use"

Change the port in `vite.config.js`:
```javascript
server: {
  port: 3001,  // Change to 3001 or any unused port
}
```

### "npm: command not found"

Make sure Node.js is installed. Download from https://nodejs.org/

Restart your terminal after installing Node.js.

### "Module not found" error

Try clearing node_modules and reinstalling:
```bash
rm -r node_modules
npm install
```

### CORS errors in browser console

The backend needs to have CORS enabled for `http://localhost:3000`.

In your Flask backend, add:
```python
from flask_cors import CORS
CORS(app, origins=["http://localhost:3000"])
```

### Styles not working

Make sure Tailwind CSS is properly configured:
```bash
npm install -D tailwindcss postcss autoprefixer
npm run dev
```

## Performance Tips

1. **Use Chrome DevTools** for performance monitoring
2. **Enable code splitting** (already enabled by Vite)
3. **Lazy load routes** if adding more pages
4. **Optimize images** before adding to project
5. **Monitor bundle size**: `npm run build`

## Production Deployment

### Build for Production

```bash
npm run build
```

This creates an optimized `dist/` folder.

### Deploy to Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel --prod
```

### Deploy to Netlify

1. Build: `npm run build`
2. Upload `dist/` folder to Netlify
3. Set environment variables in Netlify dashboard

### Using Docker

Create `Dockerfile`:
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

Build and run:
```bash
docker build -t jarvis-frontend .
docker run -p 3000:3000 jarvis-frontend
```

## Browser Requirements

- Chrome/Edge: Version 90+
- Firefox: Version 88+
- Safari: Version 14+
- Mobile: iOS Safari 12+, Chrome Android 90+

## Additional Resources

- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com)
- [React Router Documentation](https://reactrouter.com)
- [Zustand Documentation](https://github.com/pmndrs/zustand)

## Support

For issues or questions:
1. Check the README.md in the frontend directory
2. Review error messages in browser console (F12)
3. Check Vite dev server output
4. Check backend server logs

## Next Steps

1. ✅ Frontend is ready
2. ⬜ Connect backend APIs
3. ⬜ Add real Jarvis chatbot responses
4. ⬜ Implement Dosha detection
5. ⬜ Add user dashboard
6. ⬜ Deploy to production

---

**Happy coding! 🚀**
