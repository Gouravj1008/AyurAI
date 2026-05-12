# Jarvis Ayurveda - Getting Started Checklist

## ✅ Pre-Check (Verify Setup)

### System Requirements
- [ ] Windows/Mac/Linux with Command Line access
- [ ] Node.js 16+ installed (`node --version` to check)
- [ ] Python 3.14+ installed (`python --version` to check)
- [ ] npm installed (comes with Node.js)
- [ ] 2GB free disk space
- [ ] 8GB+ RAM recommended

### Check Node.js & npm
```bash
node --version      # Should be v16.0.0 or higher
npm --version       # Should be 7.0.0 or higher
```

If not installed: https://nodejs.org/

---

## 🚀 Step 1: Start Backend (5 minutes)

### 1.1 Open PowerShell or Command Prompt
- Windows: Press `Win + R`, type `powershell`, press Enter
- Or: Open Command Prompt

### 1.2 Navigate to Project
```bash
cd e:\Jarvis
```

### 1.3 Activate Virtual Environment
```bash
.\venv\Scripts\Activate.ps1
```

**Expected output:** You should see `(venv)` at the beginning of your command prompt

### 1.4 Start Backend
```bash
python run_jarvis_improved.py
```

**Expected output:**
```
[INFO] Python Version: 3.14.3
[INFO] Checking dependencies...
[OK] All dependencies found
[OK] Pre-launch diagnostics passed
[*] Launching Chat UI...
```

**Backend is now running!** ✅

Keep this terminal open (don't close it).

---

## 🌐 Step 2: Start Frontend (5 minutes)

### 2.1 Open New Terminal/PowerShell
(Don't close the backend terminal!)

### 2.2 Navigate to Frontend
```bash
cd e:\Jarvis\frontend
```

### 2.3 Install Dependencies (First time only)
This may take 2-5 minutes...

```bash
npm install
```

**Expected output:**
```
added 1000+ packages in 180s
```

### 2.4 Start Development Server
```bash
npm run dev
```

**Expected output:**
```
VITE v5.0.8  ready in 234 ms

➜  Local:   http://localhost:3000/
➜  press h to show help
```

**Frontend is now running!** ✅

---

## 🌍 Step 3: Open in Browser (1 minute)

### 3.1 Open Browser
- Chrome, Firefox, Safari, or Edge

### 3.2 Visit Frontend
```
http://localhost:3000
```

**You should see the Jarvis Ayurveda landing page!** 🎉

---

## 🧪 Step 4: Test Features (10 minutes)

### 4.1 Test Landing Page
- [ ] View hero section
- [ ] Click "Sign In" button → goes to login page
- [ ] Click "Get Started" button → goes to signup page
- [ ] Scroll down to see features
- [ ] Check responsiveness (resize browser window)

### 4.2 Test Sign Up
- [ ] Click "Sign Up" on landing page
- [ ] Enter your name: `John Doe`
- [ ] Enter email: `john@example.com`
- [ ] Enter password: `password123`
- [ ] Confirm password: `password123`
- [ ] Click "Sign Up"
- [ ] Should redirect to Chat page

### 4.3 Test Login
If you need to log in again:
- [ ] Go to `http://localhost:3000/login`
- [ ] Click "Demo" button to auto-fill credentials
- [ ] Click "Log In"
- [ ] Should go to Chat page

### 4.4 Test Chat
- [ ] Type a message: "Hello"
- [ ] Click the **Send button** (arrow icon) or press Enter
- [ ] See your message appear in green on right
- [ ] See bot response in dark bubble on left
- [ ] Messages have timestamps
- [ ] Try Shift+Enter to add newline
- [ ] Click "New Chat" to start fresh

### 4.5 Test Sidebar
- [ ] Look at left sidebar
- [ ] See chat history sections
- [ ] Click "Settings" link
- [ ] Click "Help" link
- [ ] Click "Logout" to logout

### 4.6 Test Mobile Responsiveness
- [ ] Resize browser window to mobile size
- [ ] Sidebar should toggle with button
- [ ] All text should be readable
- [ ] Buttons should be easy to tap

---

## 🔄 Terminal Commands Reference

### Stop Backend
In backend terminal: Press `Ctrl + C`

### Stop Frontend
In frontend terminal: Press `Ctrl + C`

### Restart Backend
```bash
# In backend terminal
python run_jarvis_improved.py
```

### Restart Frontend
```bash
# In frontend terminal
npm run dev
```

---

## 📋 Troubleshooting

### "Port 3000 already in use"
```bash
# Try port 3001 instead
# Edit vite.config.js and change port: 3000 to port: 3001
npm run dev
# Visit http://localhost:3001
```

### "npm: command not found"
- Node.js not installed or not in PATH
- Restart your terminal after installing Node.js
- Verify: `node --version`

### "Python: command not found"
- Python not installed or not in PATH
- Download from https://nodejs.org/
- Restart terminal after installing

### "Module not found" error
```bash
# Clear and reinstall
cd e:\Jarvis\frontend
rm -r node_modules
rm package-lock.json
npm install
npm run dev
```

### "Backend not responding" error
- Check if backend terminal still shows running output
- If stopped, restart it: `python run_jarvis_improved.py`
- Verify: http://localhost:5000 should not be accessible (backend doesn't have web interface yet)

### Styles not showing
- Restart dev server: `npm run dev`
- Clear browser cache: Ctrl+Shift+Delete
- Try different browser: Chrome or Firefox

### Can't login with demo credentials
- Open browser DevTools: F12
- Check "Console" tab for error messages
- Check "Network" tab to see if requests are being sent

---

## 📁 File Locations Quick Reference

| What | Where |
|------|-------|
| Backend Main File | `e:\Jarvis\run_jarvis_improved.py` |
| Frontend Files | `e:\Jarvis\frontend\src\` |
| Configuration | `e:\Jarvis\config.py` |
| Models | `e:\Jarvis\models\` |
| Training Data | `e:\Jarvis\data\` |
| Frontend Config | `e:\Jarvis\frontend\vite.config.js` |
| Auth Store | `e:\Jarvis\frontend\src\store\authStore.js` |

---

## 🎯 Next Steps After Testing

### Option 1: Explore More Features
1. Try different messages in chat
2. Test mobile view
3. Check browser DevTools (F12)
4. Review code in `src/pages/Chat.jsx`

### Option 2: Connect Real Backend API
1. Read `BACKEND_INTEGRATION.md`
2. Create Flask REST API
3. Update `authStore.js` with API calls
4. Test full integration

### Option 3: Customize Frontend
1. Edit colors in `tailwind.config.js`
2. Modify pages in `src/pages/`
3. Add new components in `src/components/`
4. Update styling in `src/index.css`

---

## 📖 Documentation Guide

Need help? Check these files:

| Question | File |
|----------|------|
| How do I set up the frontend? | `FRONTEND_SETUP.md` |
| How do I create backend API? | `BACKEND_INTEGRATION.md` |
| What's the project status? | `PROJECT_STATUS.md` |
| What's available? | `QUICK_REFERENCE.md` |
| API documentation? | `frontend/README.md` |

---

## ✅ Success Checklist

By the end, you should have:

- [ ] Backend terminal running without errors
- [ ] Frontend terminal running on port 3000
- [ ] Browser showing landing page at http://localhost:3000
- [ ] Able to click through pages (Landing → Signup → Chat)
- [ ] Able to type and send messages
- [ ] Send button working
- [ ] Messages displaying correctly
- [ ] Sidebar visible with chat history
- [ ] Logout button working

---

## 🎓 Understanding the Architecture

### What's Running Where?

```
Your Computer
├── Terminal 1 (Backend)
│   └── Python Backend (port 5000)
│       ├── TinyLlama 1.1B model
│       ├── Medical LoRA adapter
│       └── Vosk speech-to-text
│
├── Terminal 2 (Frontend)
│   └── Vite Dev Server (port 3000)
│       ├── React components
│       ├── Tailwind styling
│       └── Zustand state management
│
└── Browser (Frontend)
    └── http://localhost:3000
        ├── Landing page
        ├── Login/Signup pages
        ├── Chat interface
        └── Send button
```

### How It Works

1. **Landing Page** - Static content, no backend needed
2. **Login/Signup** - Currently mock (no real backend connection yet)
3. **Chat** - Messages update in real-time, currently mock responses
4. **Send Button** - Sends message, gets mock response back

### Next Phase

When backend API is created:
- Login will call `/api/auth/login`
- Signup will call `/api/auth/signup`
- Chat messages will call `/api/chat`
- Responses will come from Jarvis AI brain

---

## 🔍 Checking Everything Works

### Verify Backend
```bash
# Check if running
netstat -ano | findstr :5000

# If port 5000 is listening, backend is running ✅
```

### Verify Frontend
```bash
# Check if running
netstat -ano | findstr :3000

# If port 3000 is listening, frontend is running ✅
```

### Check Browser Console
1. Open http://localhost:3000
2. Press F12 to open DevTools
3. Click "Console" tab
4. Should show no red errors (warnings are OK)

---

## 💾 Saving Your Work

### Backend Changes
- Edit Python files
- Restart backend to see changes
- Models auto-reload

### Frontend Changes
- Edit React components
- Dev server auto-refreshes (hot reload)
- Changes appear instantly in browser

### Don't Forget
```bash
# When done for the day, close both terminals
# Backend terminal: Ctrl+C
# Frontend terminal: Ctrl+C
```

---

## 🚀 You're Ready!

**Congratulations!** You now have:

✅ Working Python backend with AI models
✅ Beautiful React frontend with all pages
✅ ChatGPT-style chat interface
✅ Send button for messages
✅ Dark theme UI
✅ Form validation
✅ Responsive design

**Next:** Create the backend REST API to connect everything!

---

## 📞 Still Need Help?

1. **Check the docs:**
   - `FRONTEND_SETUP.md` - Frontend help
   - `BACKEND_INTEGRATION.md` - Backend help
   - `PROJECT_STATUS.md` - Project overview

2. **Check browser DevTools (F12):**
   - Console tab for error messages
   - Network tab to see API calls
   - Elements tab to inspect HTML

3. **Check terminal output:**
   - Backend terminal shows model loading status
   - Frontend terminal shows dev server status
   - Both show error messages if something fails

---

**Happy coding! 🎉**

**Last Updated:** This session
