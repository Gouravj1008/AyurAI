"""Flask API for the Jarvis Ayurveda React frontend.

This server keeps the application dosha-first:
- users must provide or detect a dosha at signup
- the dosha is saved with the account
- chat responses are routed through the user's dosha profile

Auth uses stateless JWT tokens (HS256):
- signed with JWT_SECRET from .env
- expiry controlled by JWT_EXPIRY_HOURS (default 24h)
- tokens survive server restarts (no in-memory session store)
"""

from __future__ import annotations

import os
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Optional

import jwt
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

from auth_manager import AuthManager

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
load_dotenv()

JWT_SECRET: str = os.getenv("JWT_SECRET", "change-me-in-production")
JWT_ALGORITHM: str = "HS256"
JWT_EXPIRY_HOURS: int = int(os.getenv("JWT_EXPIRY_HOURS", "24"))

VALID_DOSHAS = {"vata", "pitta", "kapha"}
MIN_CONSTITUTION_WORDS = 10
MIN_CONSTITUTION_CHARS = 45

auth_manager = AuthManager()
brain = None


def is_useful_constitution_answer(value: str) -> bool:
    """Return True when the signup answer has enough real signal to detect dosha."""
    normalized = " ".join(value.split())
    if len(normalized) < MIN_CONSTITUTION_CHARS:
        return False
    words = [word for word in normalized.split() if any(char.isalpha() for char in word)]
    if len(words) < MIN_CONSTITUTION_WORDS:
        return False

    vague_answers = {
        "i do not know",
        "i dont know",
        "don't know",
        "dont know",
        "no idea",
        "not sure",
        "nothing",
        "none",
        "test",
        "asdf",
    }
    return normalized.lower() not in vague_answers


def get_allowed_origins() -> list[str]:
    allowed = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        r"https://.*\.vercel\.app",
        r"https://.*\.netlify\.app",
        r"https://.*\.onrender\.com",
    ]
    origins = os.getenv("CORS_ORIGINS", "").strip()
    if origins:
        allowed.extend(origin.strip().rstrip("/") for origin in origins.split(",") if origin.strip())
    return allowed


# ---------------------------------------------------------------------------
# JWT helpers
# ---------------------------------------------------------------------------

def create_jwt(username: str) -> str:
    """Create a signed JWT for *username* valid for JWT_EXPIRY_HOURS."""
    now = datetime.now(tz=timezone.utc)
    exp = now + timedelta(hours=JWT_EXPIRY_HOURS)
    payload = {
        "sub": username,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_jwt(token: str) -> Optional[str]:
    """Decode *token* and return the username (sub), or None if invalid/expired."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        print("[AUTH] Token expired")
        return None
    except jwt.InvalidTokenError as e:
        print(f"[AUTH] Invalid token: {e}")
        return None
    except Exception as e:
        print(f"[AUTH] Unexpected JWT error: {e}")
        return None


# ---------------------------------------------------------------------------
# Request helpers
# ---------------------------------------------------------------------------

def resolve_token() -> Optional[str]:
    """Extract the raw JWT from Authorization header or JSON body."""
    auth_header = request.headers.get("Authorization", "")
    if auth_header:
        print(f"[AUTH] Header found: {auth_header[:20]}...")
        if auth_header.startswith("Bearer "):
            return auth_header[len("Bearer "):].strip()
    
    payload = request.get_json(silent=True) or {}
    token = payload.get("token")
    if token:
        print(f"[AUTH] Token found in JSON body: {token[:10]}...")
    return token


def resolve_username_from_token() -> Optional[str]:
    """Validate the JWT from the request and return the username."""
    token = resolve_token()
    if not token:
        print("[AUTH] No token found in request")
        return None
    username = decode_jwt(token)
    if not username:
        print(f"[AUTH] Failed to decode token: {token[:15]}...")
    return username


# ---------------------------------------------------------------------------
# AI brain (lazy-loaded)
# ---------------------------------------------------------------------------

def get_brain_instance():
    """Lazily import and initialize the AI brain only when first needed."""
    global brain
    if brain is None:
        from ai_brain_ayurveda import get_brain  # heavy import deferred
        brain = get_brain()
    return brain


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------

def serialize_user(username: str, user: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": username,
        "name": user.get("full_name") or username,
        "email": user.get("email") or username,
        "dosha": user.get("dosha"),
        "constitution": user.get("constitution", ""),
        "dosha_source": user.get("dosha_source"),
    }


def build_auth_response(username: str, token: str) -> Dict[str, Any]:
    user = auth_manager.get_user(username)
    return {
        "success": True,
        "token": token,
        "expiresIn": JWT_EXPIRY_HOURS * 3600,  # seconds, useful for frontend
        "user": serialize_user(username, user or {}),
    }


# ---------------------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------------------

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(
        app,
        origins=get_allowed_origins(),
        methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )

    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------
    @app.get("/api/health")
    def health():
        return jsonify({"success": True, "status": "ok"})

    # ------------------------------------------------------------------
    # Signup
    # ------------------------------------------------------------------
    @app.post("/api/auth/signup")
    def signup():
        payload = request.get_json(silent=True) or {}
        name = (payload.get("name") or "").strip()
        email = (payload.get("email") or "").strip().lower()
        password = payload.get("password") or ""
        constitution = (payload.get("constitution") or payload.get("description") or "").strip()
        selected_dosha = (payload.get("dosha") or payload.get("selectedDosha") or "").strip().lower()

        if not name or not email or not password:
            return jsonify({"success": False, "error": "Name, email, and password are required."}), 400

        if len(password) < 6:
            return jsonify({"success": False, "error": "Password must be at least 6 characters."}), 400

        resolved_dosha = selected_dosha if selected_dosha in VALID_DOSHAS else None

        if not resolved_dosha and constitution:
            if not is_useful_constitution_answer(constitution):
                return jsonify({
                    "success": False,
                    "error": "Please describe real body, digestion, sleep, skin, energy, and mood patterns in at least 10 words so dosha detection is not guessed.",
                }), 400

            try:
                brain_instance = get_brain_instance()
                resolved_dosha = brain_instance.detect_dosha(constitution)
            except Exception:
                return jsonify({
                    "success": False,
                    "error": "Could not detect dosha right now. Please select Vata, Pitta, or Kapha and try again.",
                }), 503

        if not resolved_dosha:
            return jsonify({
                "success": False,
                "error": "I could not detect a dosha from that answer without guessing. Please add more real details or select Vata, Pitta, or Kapha.",
            }), 400

        username = email
        success, message = auth_manager.register(
            username=username,
            email=email,
            password=password,
            full_name=name,
            dosha=resolved_dosha,
            constitution=constitution,
            dosha_source="signup-selected" if selected_dosha in VALID_DOSHAS else "signup-detected",
        )

        if not success:
            return jsonify({"success": False, "error": message}), 400

        token = create_jwt(username)
        return jsonify(build_auth_response(username, token))

    # ------------------------------------------------------------------
    # Login
    # ------------------------------------------------------------------
    @app.post("/api/auth/login")
    def login():
        payload = request.get_json(silent=True) or {}
        email_or_user = (payload.get("email") or "").strip().lower()
        password = payload.get("password") or ""

        if not email_or_user or not password:
            return jsonify({"success": False, "error": "Email and password are required."}), 400

        # Login logic in AuthManager handles email-to-username lookup
        success, message = auth_manager.login(email_or_user, password)
        if not success:
            return jsonify({"success": False, "error": message}), 401

        # We must use the canonical username (the key in self.users) for the token
        # to ensure get_user(username) works in future requests.
        canonical_username = email_or_user
        user_by_email = auth_manager.get_user_by_email(email_or_user)
        if user_by_email:
            # Find the key for this user
            for k, v in auth_manager.users.items():
                if v == user_by_email:
                    canonical_username = k
                    break

        token = create_jwt(canonical_username)
        return jsonify(build_auth_response(canonical_username, token))

    # ------------------------------------------------------------------
    # Logout  (JWT is stateless — client drops the token; server confirms)
    # ------------------------------------------------------------------
    @app.post("/api/auth/logout")
    def logout():
        username = resolve_username_from_token()
        if not username:
            return jsonify({"success": False, "error": "No valid token provided."}), 401
        return jsonify({"success": True, "message": "Logged out successfully."})

    # ------------------------------------------------------------------
    # Token refresh  (issue a fresh JWT without re-entering credentials)
    # ------------------------------------------------------------------
    @app.post("/api/auth/refresh")
    def refresh():
        username = resolve_username_from_token()
        if not username:
            return jsonify({"success": False, "error": "Unauthorized or token expired."}), 401
        new_token = create_jwt(username)
        return jsonify(build_auth_response(username, new_token))

    # ------------------------------------------------------------------
    # Profile
    # ------------------------------------------------------------------
    @app.get("/api/user/profile")
    def profile():
        username = resolve_username_from_token()
        if not username:
            return jsonify({"success": False, "error": "Unauthorized"}), 401

        user = auth_manager.get_user(username) or {}
        return jsonify({"success": True, "user": serialize_user(username, user)})

    # ------------------------------------------------------------------
    # Chat history
    # ------------------------------------------------------------------
    @app.get("/api/chat/history")
    def chat_history():
        username = resolve_username_from_token()
        if not username:
            return jsonify({"success": False, "error": "Unauthorized"}), 401

        user = auth_manager.get_user(username) or {}
        history = user.get("chat_history", [])
        return jsonify({"success": True, "messages": history})

    # ------------------------------------------------------------------
    # Chat
    # ------------------------------------------------------------------
    @app.post("/api/chat")
    def chat():
        payload = request.get_json(silent=True) or {}
        username = resolve_username_from_token()
        if not username:
            return jsonify({"success": False, "error": "Unauthorized"}), 401

        message = (payload.get("message") or "").strip()
        if not message:
            return jsonify({"success": False, "error": "Message is required."}), 400

        user = auth_manager.get_user(username) or {}
        dosha = (payload.get("dosha") or user.get("dosha") or "").strip().lower()
        constitution = (payload.get("constitution") or user.get("constitution") or "").strip()

        if dosha not in VALID_DOSHAS:
            detected = get_brain_instance().detect_dosha(constitution or message)
            if detected:
                dosha = detected
                auth_manager.update_user_dosha(username, dosha, dosha_source="chat-detected")

        if dosha not in VALID_DOSHAS:
            return jsonify({
                "success": False,
                "error": "Please complete dosha detection first so I can give dosha-specific Ayurvedic guidance.",
            }), 400

        brain_instance = get_brain_instance()
        brain_instance.set_user_profile(dosha)
        answer = brain_instance.respond_for_user(message, dosha=dosha, constitution=constitution)

        auth_manager.append_chat_history(username, message, answer)

        return jsonify({
            "success": True,
            "message": answer,
            "dosha": dosha,
            "vaidya": brain_instance.suggest_vaidya(),
        })

    return app


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run_api_server(host: str = "0.0.0.0", port: Optional[int] = None):
    port = port or int(os.getenv("PORT", "5000"))
    app = create_app()
    app.run(host=host, port=port, debug=False, use_reloader=False)


if __name__ == "__main__":
    run_api_server()
