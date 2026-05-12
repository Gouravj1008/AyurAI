# Jarvis Ayurveda Frontend

Modern React-based web interface for the Jarvis Ayurveda AI Chatbot with landing page, authentication, and ChatGPT-style chat interface.

## Features

- **Landing Page**: Beautiful landing page with features showcase
- **Authentication**: User login and signup with form validation
- **Chat Interface**: ChatGPT-style messaging with send button
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Chat**: Message display with typing indicators
- **User Sidebar**: Chat history and user management
- **Tailwind CSS**: Modern, responsive UI styling

## Tech Stack

- **React 18**: UI library
- **Vite**: Fast build tool and dev server
- **React Router**: Client-side routing
- **Zustand**: State management
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client (for API calls)

## Setup

### Prerequisites

- Node.js 16+ and npm/yarn

### Installation

1. **Navigate to frontend directory**:
   ```bash
   cd e:\Jarvis\frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Create environment file**:
   ```bash
   cp .env.example .env
   ```

4. **Update `.env` if needed**:
   ```env
   VITE_API_BASE_URL=http://localhost:5000/api
   ```

### Development

Start the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/           # Reusable components
│   │   ├── ChatMessage.jsx  # Message display component
│   │   └── Sidebar.jsx      # Chat sidebar
│   ├── pages/                # Page components
│   │   ├── Landing.jsx      # Landing page
│   │   ├── Login.jsx        # Login page
│   │   ├── Signup.jsx       # Signup page
│   │   └── Chat.jsx         # Main chat interface
│   ├── store/                # State management
│   │   └── authStore.js     # Auth state with Zustand
│   ├── App.jsx              # Main app with routing
│   ├── main.jsx             # Entry point
│   └── index.css            # Tailwind styles
├── index.html               # HTML template
├── package.json             # Dependencies
├── vite.config.js           # Vite configuration
├── tailwind.config.js       # Tailwind configuration
├── postcss.config.js        # PostCSS configuration
└── README.md                # This file
```

## Available Routes

- `/` - Landing page (public)
- `/login` - Login page (public, redirects to chat if authenticated)
- `/signup` - Signup page (public, redirects to chat if authenticated)
- `/chat` - Chat interface (protected, redirects to login if not authenticated)

## Integration with Backend

### Setting up API calls

The frontend is configured to proxy API calls to `http://localhost:5000` by default.

Example API call in a component:

```javascript
import axios from 'axios'

const response = await axios.post('/api/chat', {
  message: userMessage,
  token: authStore.token,
})
```

### Authentication Flow

1. User signs up or logs in
2. Backend returns authentication token
3. Token is stored in Zustand store (persisted to localStorage)
4. Token is sent in headers for authenticated requests

## Features to Implement

### 1. API Integration

- Connect login/signup to backend
- Connect chat messages to Jarvis backend
- Add loading states and error handling

### 2. User Dashboard

- View conversation history
- Delete conversations
- View user settings and preferences

### 3. Enhanced Chat Features

- Message editing
- Message deletion
- Copy to clipboard
- Regenerate responses

### 4. Dosha Assessment

- Create interactive dosha quiz
- Display dosha results with recommendations
- Save dosha profile

### 5. Additional Pages

- Settings page
- Profile management
- Wellness dashboard
- Diet plans library

## Backend Connection

To connect with the Python Jarvis backend:

1. **Start backend server** (if not running):
   ```bash
   cd e:\Jarvis
   python run_jarvis_improved.py
   ```

2. **Create backend API** (Flask/FastAPI) with endpoints:
   - `POST /api/auth/login` - Login user
   - `POST /api/auth/signup` - Create new user
   - `POST /api/chat` - Send message to chatbot
   - `GET /api/chat/history` - Get chat history
   - `GET /api/user/profile` - Get user info

3. **Update frontend API calls** in `authStore.js` and `Chat.jsx`

## Troubleshooting

### Port already in use

If port 3000 is already in use, change it in `vite.config.js`:

```javascript
server: {
  port: 3001, // Change this
}
```

### CORS errors

Make sure backend has CORS enabled for `http://localhost:3000`

### Styles not loading

Rebuild Tailwind CSS:

```bash
npm install
```

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Connect repo to Vercel
3. Set environment variables
4. Deploy

### Other Platforms

- **Netlify**: Similar to Vercel
- **GitHub Pages**: For static hosting
- **Docker**: Containerize the app

Example Dockerfile:

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

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest version
- Mobile browsers: iOS Safari 12+, Chrome Mobile

## Performance Optimization

- Code splitting enabled by default (Vite)
- Lazy loading for routes
- Image optimization recommended
- CSS purging via Tailwind

## Security Considerations

- Never commit `.env` files with secrets
- Use HTTPS in production
- Implement CSRF protection on backend
- Validate all user inputs
- Use secure HTTP-only cookies for tokens
- Implement rate limiting on backend

## Contributing

1. Create a new branch: `git checkout -b feature-name`
2. Make changes and test
3. Commit: `git commit -m "Add feature"`
4. Push: `git push origin feature-name`
5. Open a pull request

## License

This project is part of Jarvis Ayurveda. See main README for license.

## Support

For issues and questions, contact the development team or open an issue on the repository.

---

**Built with ❤️ using React + Vite + Tailwind CSS**
