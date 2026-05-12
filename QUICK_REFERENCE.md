# Jarvis Ayurveda - Quick Reference Card

## 🚀 Start Commands

### Backend (Python)
```bash
cd e:\Jarvis
.\venv\Scripts\Activate.ps1
python run_jarvis_improved.py
```

### Frontend (React)
```bash
cd e:\Jarvis\frontend
npm install
npm run dev
```

**Frontend URL:** http://localhost:3000
**Backend URL:** http://localhost:5000

---

## 📋 Project Status

| Component | Status | Location |
|-----------|--------|----------|
| Python Backend | ✅ Ready | `e:\Jarvis\` |
| React Frontend | ✅ Ready | `e:\Jarvis\frontend\` |
| TinyLlama Model | ✅ Loaded | `models/vosk-model-small-en-us-0.15/` |
| Medical LoRA | ✅ Loaded | `models/medical-lora/` |
| Vosk STT | ✅ Ready | Pre-configured |
| Hotword Detection | ⚠️ Needs API Key | `models/porcupine/` |
| REST API | ⏳ Pending | Needs creation |
| Database | ⏳ Pending | Needs setup |

---

## 📁 Important Files

### Backend
- `run_jarvis_improved.py` - Main launcher (fixed unicode)
- `chat_ui_ayurveda.py` - Tkinter GUI (working)
- `ai_brain_ayurveda.py` - AI brain logic
- `config.py` - Configuration (fixed emoji)

### Frontend
- `src/App.jsx` - Main app & routing
- `src/pages/Landing.jsx` - Home page
- `src/pages/Login.jsx` - Login page
- `src/pages/Signup.jsx` - Signup page
- `src/pages/Chat.jsx` - ChatGPT-style chat
- `src/components/ChatMessage.jsx` - Message component
- `src/components/Sidebar.jsx` - Sidebar component
- `src/store/authStore.js` - Auth state (Zustand)

### Documentation
- `FRONTEND_SETUP.md` - Frontend setup guide
- `BACKEND_INTEGRATION.md` - Backend API guide
- `PROJECT_STATUS.md` - Project overview
- `frontend/README.md` - Frontend API docs

---

## 🔄 Frontend Pages

| Page | URL | Status | Auth Required |
|------|-----|--------|---|
| Landing | `/` | ✅ Ready | ❌ No |
| Login | `/login` | ✅ Ready | ❌ No |
| Signup | `/signup` | ✅ Ready | ❌ No |
| Chat | `/chat` | ✅ Ready | ✅ Yes |

---

## 🎨 UI Colors (Tailwind)

```css
Primary Green:  #10a37f
Dark Background: #343541
Darker Background: #202123
Input Background: #40414f
Text: #ECECF1
```

---

## 🔌 API Endpoints (To Create)

```
POST   /api/auth/signup         Create account
POST   /api/auth/login          Login
POST   /api/chat                Send message
GET    /api/chat/history        Get messages
GET    /api/user/profile        User info
POST   /api/dosha/detect        Dosha detection
```

---

## 🛠️ Dependencies

### Backend (40+ packages)
- PyTorch (CPU)
- Transformers
- PEFT
- Vosk
- TRL
- Datasets
- Sounddevice
- Pyttsx3

### Frontend (40+ packages)
- React 18
- Vite 5
- React Router 6
- Zustand
- Tailwind CSS 3
- Axios
- ESLint

---

## 🧪 Test Credentials

**Email:** demo@example.com
**Password:** demo123

*(Or click "Demo" button on login page)*

---

## 📱 Responsive Breakpoints

- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

All pages are fully responsive!

---

## ⚙️ Configuration Files

| File | Purpose |
|------|---------|
| `package.json` | Dependencies & scripts |
| `vite.config.js` | Build & proxy config |
| `tailwind.config.js` | Theme customization |
| `.env.example` | Environment template |
| `eslint.config.js` | Code quality rules |

---

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| Port 3000 in use | Change in `vite.config.js` |
| Backend not responding | Check if running on port 5000 |
| CORS errors | Enable CORS in Flask backend |
| npm module not found | Run `npm install` |
| Styles not loading | Restart dev server |
| Token invalid | Check localStorage for auth token |

---

## 📞 File Structure

```
e:\Jarvis\
├── venv/                          # Python environment
├── models/                        # AI models
├── data/                          # Training data
├── frontend/                      # React app
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── store/
│       └── ...
├── FRONTEND_SETUP.md              # Setup guide
├── BACKEND_INTEGRATION.md         # API guide
├── PROJECT_STATUS.md              # Status
└── (Python files)
```

---

## ✅ What's Complete

✅ Backend environment working
✅ TinyLlama model loaded
✅ Medical LoRA adapter ready
✅ Voice input functional
✅ React frontend complete
✅ All 4 pages implemented
✅ Send button working
✅ Dark theme applied
✅ Form validation done
✅ State management setup
✅ Documentation written

---

## ⏳ What's Pending

⏳ Create Flask/FastAPI REST API
⏳ Connect frontend to backend APIs
⏳ Set up database (MongoDB/PostgreSQL)
⏳ Deploy to production
⏳ Configure SSL/HTTPS
⏳ Set up custom domain

---

## 🎯 Next Immediate Steps

1. **Test Frontend:**
   ```bash
   cd e:\Jarvis\frontend
   npm install
   npm run dev
   ```

2. **Create Backend API:**
   See `BACKEND_INTEGRATION.md` for Flask examples

3. **Connect Endpoints:**
   Update `src/store/authStore.js` (TODO comments in place)

4. **Full Stack Test:**
   Test signup → login → chat flow

---

## 📚 Documentation Map

- **Getting Started:** `START_HERE.md` (root)
- **Frontend Setup:** `FRONTEND_SETUP.md` (root)
- **Backend Integration:** `BACKEND_INTEGRATION.md` (root)
- **Project Status:** `PROJECT_STATUS.md` (root)
- **Frontend Features:** `frontend/FEATURES.md`
- **Frontend API:** `frontend/README.md`
- **Quick Reference:** This file

---

## 🔐 Security Notes

- Use HTTPS in production
- Hash passwords with bcrypt
- Set short token expiry
- Validate all inputs
- Use environment variables for secrets
- Enable CORS only for frontend origin

---

## 📊 Performance Tips

1. Code splitting enabled by Vite
2. CSS minification in production
3. Lazy loading ready for routes
4. Image optimization ready
5. Monitor bundle size: `npm run build`

---

## 🚀 Deployment Options

### Frontend
- Vercel (recommended)
- Netlify
- GitHub Pages
- Docker

### Backend
- Heroku
- AWS EC2
- DigitalOcean
- PythonAnywhere

---

## 💡 Key Features

✨ Landing page with showcase
✨ Beautiful login/signup forms
✨ ChatGPT-style interface
✨ Send button with icon
✨ Message timestamps
✨ Chat sidebar
✨ Mobile responsive
✨ Dark theme
✨ Form validation
✨ State persistence

---

## 🎓 Learning Resources

- [React Docs](https://react.dev)
- [Vite Guide](https://vitejs.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [React Router](https://reactrouter.com)
- [Zustand](https://github.com/pmndrs/zustand)
- [Flask Guide](https://flask.palletsprojects.com)

---

## 📞 Support Files

1. **Frontend issues?** → `FRONTEND_SETUP.md`
2. **Backend issues?** → `BACKEND_INTEGRATION.md`
3. **General questions?** → `PROJECT_STATUS.md`
4. **API docs?** → `frontend/README.md`

---

**Last Updated:** This session
**Frontend Version:** 1.0.0
**Backend Version:** 1.0.0

**Status:** ✅ READY FOR TESTING & INTEGRATION
