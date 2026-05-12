# 🚀 PRODUCTION DEPLOYMENT GUIDE

## For Startup Launch - Production Ready

---

## 📦 Option 1: Standalone Executable (Windows/Mac/Linux)

Build a single executable file for distribution.

### Step 1: Install PyInstaller
```bash
pip install pyinstaller
```

### Step 2: Build Executable
```bash
pyinstaller \
  --onefile \
  --windowed \
  --icon=icon.ico \
  --name="Jarvis" \
  run_jarvis_improved.py
```

Output: `dist/Jarvis.exe` (Windows) or `dist/Jarvis` (Mac/Linux)

### Step 3: Package with Models
```bash
# Create distribution folder
mkdir dist/Jarvis_App
cp dist/Jarvis dist/Jarvis_App/
cp -r models dist/Jarvis_App/
cp -r data dist/Jarvis_App/
cp .env.example dist/Jarvis_App/.env
```

### Step 4: Share/Install
- Users download and extract folder
- Double-click executable to run
- Models included (no internet download needed)

---

## 🐳 Option 2: Docker Container

Deploy as containerized application.

### Step 1: Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    alsa-utils \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_complete.txt

# Create non-root user
RUN useradd -m jarvis && chown -R jarvis:jarvis /app
USER jarvis

# Expose port (if using API)
EXPOSE 5000

# Run application
CMD ["python", "run_jarvis_improved.py"]
```

### Step 2: Build Image
```bash
docker build -t jarvis-ayurveda:latest .
```

### Step 3: Run Container
```bash
docker run -it \
  --device /dev/snd \
  --volume ~/.Xauthority:/home/jarvis/.Xauthority:ro \
  --env DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  jarvis-ayurveda:latest
```

---

## ☁️ Option 3: Cloud Deployment (AWS/GCP/Azure)

Deploy to cloud for web/mobile access.

### Step 1: Create REST API Wrapper

File: `api_wrapper.py`
```python
from flask import Flask, request, jsonify
from ai_brain_ayurveda import get_brain
from error_handler import ErrorHandler

app = Flask(__name__)
brain = get_brain()

@app.route('/ask', methods=['POST'])
def ask():
    \"\"\"Chat endpoint\"\"\"
    try:
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({"error": "Question required"}), 400
        
        response = brain.ask_ayurveda(question)
        return jsonify({"response": response})
    except Exception as e:
        error = ErrorHandler.handle_exception(e, "API ask")
        return jsonify({"error": error}), 500

@app.route('/dosha', methods=['POST'])
def detect_dosha():
    \"\"\"Dosha detection endpoint\"\"\"
    try:
        data = request.json
        description = data.get('description', '')
        
        if not description:
            return jsonify({"error": "Description required"}), 400
        
        dosha = brain.detect_dosha(description)
        return jsonify({"dosha": dosha})
    except Exception as e:
        error = ErrorHandler.handle_exception(e, "API dosha")
        return jsonify({"error": error}), 500

@app.route('/diet/<dosha>', methods=['GET'])
def get_diet(dosha):
    \"\"\"Diet recommendation endpoint\"\"\"
    try:
        plan = brain.get_diet_recommendation(dosha)
        return jsonify({"diet_plan": plan})
    except Exception as e:
        error = ErrorHandler.handle_exception(e, "API diet")
        return jsonify({"error": error}), 500

@app.route('/wellness/<dosha>/<condition>', methods=['GET'])
def get_wellness(dosha, condition):
    \"\"\"Wellness plan endpoint\"\"\"
    try:
        plan = brain.create_wellness_plan(dosha, condition)
        return jsonify({"wellness_plan": plan})
    except Exception as e:
        error = ErrorHandler.handle_exception(e, "API wellness")
        return jsonify({"error": error}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
```

### Step 2: Deploy to AWS EC2
```bash
# 1. Create EC2 instance (Ubuntu 22.04, GPU if needed)
# 2. SSH in and run:

git clone <your-repo>
cd Jarvis
python -m venv venv
source venv/bin/activate
pip install flask -r requirements_complete.txt
python api_wrapper.py
```

### Step 3: Add Load Balancer & Domain
- Use AWS ALB to distribute traffic
- Point domain to ALB
- Add SSL certificate
- Use CloudFront for CDN

### Step 4: Client-Side Access
```python
import requests

api_url = "https://your-domain.com"

response = requests.post(f"{api_url}/ask", json={
    "question": "What is Vata Dosha?"
})

print(response.json()["response"])
```

---

## 📱 Option 4: Web Application (Flask)

Create web UI for browser access.

### File: `web_app.py`
```python
from flask import Flask, render_template, request, jsonify
from ai_brain_ayurveda import get_brain
import json

app = Flask(__name__)
brain = get_brain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    question = request.json.get('message', '')
    response = brain.ask_ayurveda(question)
    return jsonify({"response": response})

@app.route('/api/dosha', methods=['POST'])
def detect_dosha():
    description = request.json.get('description', '')
    dosha = brain.detect_dosha(description)
    profile = brain.get_health_summary() if dosha else ""
    return jsonify({"dosha": dosha, "profile": profile})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
```

### Deploy with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

---

## 🔐 Security Best Practices

### 1. Environment Secrets
```bash
# Never commit .env file
echo ".env" >> .gitignore

# Use secrets management
# AWS: AWS Secrets Manager
# Azure: Azure Key Vault
# GCP: Secret Manager
```

### 2. API Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/ask')
@limiter.limit("10 per minute")
def ask():
    # Your code
    pass
```

### 3. Authentication
```python
from functools import wraps
from flask import abort

API_KEYS = {"valid_key_123": "user1"}

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get('X-API-Key')
        if not key or key not in API_KEYS:
            abort(401)
        return f(*args, **kwargs)
    return decorated

@app.route('/ask', methods=['POST'])
@require_api_key
def ask():
    # Your code
    pass
```

### 4. HTTPS/SSL
```bash
# Let's Encrypt (free SSL)
sudo certbot certonly --standalone -d your-domain.com

# Use in Flask
from OpenSSL import SSL
context = SSL.Context(SSL.SSLv23)
context.use_privatekey_file('key.pem')
context.use_certificate_file('cert.pem')
app.run(ssl_context=context)
```

---

## 📊 Monitoring & Logging

### 1. Cloud Logging
```python
import logging
from google.cloud import logging as cloud_logging

client = cloud_logging.Client()
client.setup_logging()

logger = logging.getLogger(__name__)
logger.info("Application started")
```

### 2. Error Tracking (Sentry)
```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    "your_sentry_dsn",
    integrations=[FlaskIntegration()]
)
```

### 3. Performance Metrics
```python
from prometheus_client import Counter, Histogram

request_count = Counter('requests_total', 'Total requests')
request_duration = Histogram('request_duration_seconds', 'Request duration')

@app.route('/ask')
@request_duration.time()
def ask():
    request_count.inc()
    # Your code
```

---

## 🧪 Pre-Production Checklist

- [ ] All tests pass: `python validate_system.py`
- [ ] No hardcoded secrets (use .env)
- [ ] Error handling comprehensive
- [ ] Logging configured
- [ ] Rate limiting implemented
- [ ] Authentication added (if needed)
- [ ] HTTPS/SSL configured
- [ ] Database backups (if using DB)
- [ ] Monitoring set up
- [ ] Documentation complete
- [ ] Load testing done
- [ ] Security audit passed

---

## 🚀 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements_complete.txt
      - run: python validate_system.py

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: docker build -t jarvis:latest .
      - run: docker push registry.example.com/jarvis:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: kubectl set image deployment/jarvis jarvis=registry.example.com/jarvis:latest
```

---

## 📈 Scaling Strategy

### Horizontal Scaling (Multiple Instances)
```yaml
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jarvis
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: jarvis
        image: jarvis:latest
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
```

### Vertical Scaling (More Power)
- Use GPU instances for faster inference
- Increase CPU/RAM per instance
- Use model quantization (4-bit) for smaller footprint

### Caching Strategy
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_cached_diet(dosha):
    return brain.get_diet_recommendation(dosha)
```

---

## 💰 Cost Optimization

| Approach | Cost | Performance | Complexity |
|----------|------|-------------|-----------|
| CPU-only | Low | Slow | Simple |
| GPU instance | Medium | Fast | Medium |
| Serverless | Variable | Slow-Medium | Complex |
| Multi-region | High | Very Fast | Complex |

**Recommendation for startup**: Start with single GPU instance, scale as needed.

---

## 📞 Support & Maintenance

### Regular Tasks
- [ ] Monitor logs daily
- [ ] Check error rates
- [ ] Update dependencies monthly
- [ ] Back up data weekly
- [ ] Review metrics weekly
- [ ] Security audit quarterly

### When Things Break
1. Check logs: `tail -f jarvis.log`
2. Validate system: `python validate_system.py`
3. Restart service: `systemctl restart jarvis` (or equivalent)
4. Scale down if needed to prevent cascading failures
5. Investigate root cause
6. Deploy fix
7. Monitor for recurrence

---

**🎉 Your Jarvis chatbot is now production-ready! 🚀**

For questions, check README_AYURVEDA.md or visit documentation.

Good luck with your startup! 🌿
