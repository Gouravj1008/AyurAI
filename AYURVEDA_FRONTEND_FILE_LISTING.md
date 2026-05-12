# Ayurveda Frontend - Complete File Structure & Analysis

## Directory Tree

```
ayurveda-frontend/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   └── auth/
│   │   │       ├── login/
│   │   │       │   └── route.ts
│   │   │       └── register/
│   │   │           └── route.ts
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── globals.css
│   │   └── favicon.ico
│   │
│   ├── components/
│   │   ├── AuthModal.tsx
│   │   ├── AyurvedaOrb.tsx
│   │   ├── DoshaCards.tsx
│   │   ├── FloatingChatbot.tsx
│   │   ├── HeroSection.tsx
│   │   ├── ServicesTimeline.tsx
│   │   ├── SmoothScroll.tsx
│   │   └── UserChatPage.tsx
│   │
│   └── middleware.ts
│
├── package.json
├── tsconfig.json
├── next.config.ts
├── postcss.config.mjs
├── eslint.config.mjs
├── next-env.d.ts
├── README.md
└── .gitignore
```

---

## Key Files Analysis

### **Root App Files**

| File | Type | Purpose | Status |
|------|------|---------|--------|
| [src/app/layout.tsx](src/app/layout.tsx) | TypeScript | Root layout wrapper, font imports, metadata | ✅ Clean |
| [src/app/page.tsx](src/app/page.tsx) | TypeScript | Home page component | ⚠️ See Below |
| [src/app/globals.css](src/app/globals.css) | CSS | Global styles | ✅ |
| [src/middleware.ts](src/middleware.ts) | TypeScript | Next.js middleware | ✅ Minimal |

---

### **Components - Detailed Analysis**

#### 1. **[FloatingChatbot.tsx](src/components/FloatingChatbot.tsx)** - 200 lines
- **Purpose**: Floating chat widget in bottom-right corner
- **State Management**: 
  - `isOpen` (boolean)
  - `messages` (Message[])
  - `input` (string)
  - `isTyping` (boolean)
- **Hooks Used**: `useState`, `useRef`, `useEffect`, `useAnimatePresence`
- **Animation Library**: Framer Motion
- **Status**: ✅ Safe
- **Notes**: 
  - `useEffect` dependency array includes `[messages, isTyping]` - appropriate for scroll-to-bottom
  - Mock 2.5s timeout for bot response simulation
  - Properly structured message rendering with keys

#### 2. **[UserChatPage.tsx](src/components/UserChatPage.tsx)** - Full page
- **Purpose**: Logged-in user chat interface
- **State Management**:
  - `messages` (Message[])
  - `input` (string)
  - `isTyping` (boolean)
- **Hooks**: `useState`, `useRef`, `useEffect`
- **Props**: `user` (AuthUser), `onLogout` callback
- **Status**: ✅ Safe
- **Notes**:
  - Scroll behavior on messages/typing changes is intentional
  - Mock 1.2s timeout for bot response
  - Conditional rendering for logged-in users

#### 3. **[AuthModal.tsx](src/components/AuthModal.tsx)** - Full component
- **Purpose**: Login/Registration modal dialog
- **State Management**:
  - `mode` ("login" | "signup")
  - Form fields: `username`, `password`, `email`, `fullName`
  - `isLoading`, `error`, `success`
- **Hooks**: `useState`, `useEffect`
- **Status**: ⚠️ Potential Issue
- **Issues Found**:
  - **`useEffect` resets state on mode/isOpen change** (lines 34-42)
    - Uses `queueMicrotask` which is good
    - Pattern: Clears form when modal opens/mode changes
    - **Risk**: Should also clear `username`, `password`, `email`, `fullName` to avoid stale data
  - API calls to `/api/auth/login` and `/api/auth/register` happen on submit
  - Form submission is properly debounced with `isLoading` flag

#### 4. **[HeroSection.tsx](src/components/HeroSection.tsx)** - ~150 lines
- **Purpose**: Hero section with auth buttons and 3D background
- **State Management**:
  - `isAuthOpen` (boolean)
  - `authMode` ("login" | "signup")
- **Animations**: Framer Motion - 8 animated leaf elements
- **Complex Elements**:
  - 8 floating leaves with staggered animations (duration: 12-19s each)
  - Rotating mandala background
- **Status**: ✅ Safe
- **Performance**: Heavy but optimized with `viewport={{ once: true }}`

#### 5. **[DoshaCards.tsx](src/components/DoshaCards.tsx)** - ~100 lines
- **Purpose**: Three dosha information cards
- **Animation**: Framer Motion scroll-triggered animations
- **Viewport Optimization**: `whileInView` with `once: true`
- **Status**: ✅ Safe
- **Notes**: Cards animate on scroll, only once per page load

#### 6. **[AyurvedaOrb.tsx](src/components/AyurvedaOrb.tsx)** - ~90 lines
- **Purpose**: 3D animated orb using Three.js
- **Libraries**: react-three-fiber, drei
- **State**: `canAnimate` (prefers-reduced-motion check)
- **Status**: ✅ Safe
- **Performance Optimizations**:
  - Respects `prefers-reduced-motion` media query
  - Fallback gradient render if animation disabled
  - Low power GPU preference: `powerPreference: "low-power"`
  - No antialias: `antialias: false`
  - DPR between 1-1.5

#### 7. **[SmoothScroll.tsx](src/components/SmoothScroll.tsx)** - ~30 lines
- **Purpose**: Smooth scrolling wrapper using Lenis library
- **Hooks**: `useEffect` with cleanup
- **Status**: ✅ Safe
- **Notes**:
  - Respects `prefers-reduced-motion`
  - Proper cleanup in return statement
  - No memory leaks

#### 8. **[ServicesTimeline.tsx](src/components/ServicesTimeline.tsx)** - ~120 lines
- **Purpose**: Timeline of 4 steps/benefits
- **Animation**: Scroll-triggered animations
- **State**: Uses `useScroll` and `useTransform` for parallax effect
- **Status**: ✅ Safe

---

### **API Routes**

#### 1. **[src/app/api/auth/login/route.ts](src/app/api/auth/login/route.ts)** - ~40 lines
- **Purpose**: User login endpoint
- **Method**: POST
- **Database**: Reads from `users_data.json`
- **Security**: Password hashed with SHA-256
- **Status**: ⚠️ Issues Found

**Issues**:
- ❌ **Weak password hashing**: Uses SHA-256 without salt
- ❌ **No rate limiting**: Vulnerable to brute force attacks
- ❌ **Case-sensitive lookups**: Normalizes to lowercase, but inconsistent
- ⚠️ **Synchronous file I/O**: Blocks event loop
- ✅ Proper error handling
- ✅ Input validation present

#### 2. **[src/app/api/auth/register/route.ts](src/app/api/auth/register/route.ts)** - ~60 lines
- **Purpose**: User registration endpoint
- **Method**: POST
- **Validation**: Username (3+ chars), Password (6+ chars), Email format
- **Status**: ⚠️ Issues Found

**Issues**:
- ❌ **Same weak hashing as login**
- ❌ **No rate limiting**
- ⚠️ **Synchronous file I/O**
- ❌ **Race condition**: Multiple concurrent registrations could overwrite data
- ✅ Checks for existing username
- ✅ Checks for existing email

---

## Performance & Render Loop Analysis

### **No Infinite Render Loops Detected** ✅

All components use proper dependency arrays and cleanup patterns. However:

### **Potential Performance Issues**:

| Issue | Component | Severity | Details |
|-------|-----------|----------|---------|
| Heavy 3D rendering | AyurvedaOrb.tsx | Medium | Three.js + Framer Motion on hero - optimized with low-power GPU setting |
| Multiple animations | HeroSection.tsx | Medium | 8 animated leaves + rotating background + gradient overlays |
| State resets on open | AuthModal.tsx | Low | Form fields not cleared when switching modes (user data persists) |
| Smooth scroll library | SmoothScroll.tsx | Low | Lenis adds overhead but well-implemented with cleanup |
| Chat message scrolling | FloatingChatbot.tsx + UserChatPage.tsx | Low | Scroll-on-every-message is intentional but could batch |

---

## State Management Issues

### **AuthModal Form State Reset** ⚠️
**Location**: `src/components/AuthModal.tsx` lines 34-42

```tsx
useEffect(() => {
    if (!isOpen) {
        return;
    }
    queueMicrotask(() => {
        setMode(initialMode);
        setError("");
        setSuccess("");
        // ❌ Missing: username, password, email, fullName NOT reset
    });
}, [initialMode, isOpen]);
```

**Problem**: When switching between login/signup modes, form values persist

**Solution**: Add form field resets:
```tsx
setUsername("");
setPassword("");
setEmail("");
setFullName("");
```

---

## API Security Issues ⚠️

### **Critical**: Weak Password Hashing
- Using SHA-256 without salt is vulnerable
- **Recommendation**: Use `bcrypt` or `argon2`

### **Critical**: No Rate Limiting
- Auth endpoints vulnerable to brute force
- **Recommendation**: Add rate limiting middleware

### **High**: Race Conditions
- Multiple concurrent requests can corrupt `users_data.json`
- **Recommendation**: Add file locking or use proper database

### **Medium**: Synchronous File I/O
- Blocks Node.js event loop
- **Recommendation**: Use async file operations

---

## Summary

### ✅ Safe Components (No Re-render Issues)
- FloatingChatbot.tsx
- UserChatPage.tsx
- AyurvedaOrb.tsx
- SmoothScroll.tsx
- HeroSection.tsx
- DoshaCards.tsx
- ServicesTimeline.tsx
- layout.tsx
- middleware.ts

### ⚠️ Components Needing Review
- **AuthModal.tsx** - Form state not cleared properly on mode switch
- **page.tsx** - Safe but heavy 3D rendering on hero

### 🔴 Backend Issues
- **login/route.ts** - Weak security
- **register/route.ts** - Weak security, race conditions

---

## Files by Complexity

| File | Lines | Complexity | Dependencies |
|------|-------|-----------|--------------|
| UserChatPage.tsx | ~150 | Medium | React, Framer Motion |
| FloatingChatbot.tsx | ~200 | Medium | React, Framer Motion, Lucide |
| AuthModal.tsx | ~220 | High | React, Framer Motion, API calls |
| HeroSection.tsx | ~150 | High | React, Framer Motion, 8 animations |
| AyurvedaOrb.tsx | ~90 | High | React Three Fiber, Three.js, Drei |
| DoshaCards.tsx | ~100 | Medium | React, Framer Motion |
| ServicesTimeline.tsx | ~120 | Medium | React, Framer Motion, Scroll API |
| SmoothScroll.tsx | ~30 | Low | Lenis |
| page.tsx | ~60 | Medium | React, localStorage, routing |
| layout.tsx | ~25 | Low | Next.js metadata |

