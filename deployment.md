# Traveller — Production Deployment Guide

This document provides step-by-step instructions for deploying the **Traveller** application: hosting the static frontend on **Vercel** and the FastAPI backend on **Railway**.

---

## 1. Architecture Overview

```
   ┌──────────────────────────────┐
   │      VERCEL FRONTEND         │
   │  Hosts static/index.html     │
   └──────────────┬───────────────┘
                  │ HTTPS Requests
                  ▼
   ┌──────────────────────────────┐
   │     RAILWAY BACKEND          │
   │  Hosts FastAPI /api/ plan    │
   └──────────────────────────────┘
```

* **Frontend**: Served as static assets on Vercel. Network requests target the backend via a secure CORS handshake.
* **Backend**: Hosted on Railway as a containerized Python service connected to the Google Gemini API.

---

## 2. Backend Deployment (Railway)

Railway automatically detects the Python project using the `requirements.txt` file, installs dependencies, and runs the application.

### Step 1: Connect Repository
1. Log in to your **[Railway Dashboard](https://railway.app/)**.
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Select your `Ai travel agent` repository.

### Step 2: Configure Environment Variables
In the **Variables** tab of your Railway service, add the following variables:

| Variable | Description | Example / Recommended Value |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | Your live Google AI Studio API Key | `AIzaSy...` (DO NOT share or commit this key) |
| `ALLOWED_ORIGINS` | Comma-separated list of allowed frontend origins (for CORS) | `https://your-app.vercel.app,http://localhost:8000` |
| `PORT` | Set automatically by Railway | *Do not set manually; Railway injects this.* |

### Step 3: Deployment Command
Railway will read your dependencies and launch the server. It will detect the `run.py` entry point. In case you need to customize the start command, use:
```bash
python run.py
```
*(Our [run.py](file:///c:/Projects/Ai%20travel%20agent/run.py) has been updated to automatically bind to `0.0.0.0` in production environments and listen on the correct port injected by Railway).*

---

## 3. Frontend Deployment (Vercel)

Vercel hosts the static HTML shell, map integration, and CSS assets.

### Step 1: Project Configuration
A [vercel.json](file:///c:/Projects/Ai%20travel%20agent/vercel.json) file has been created in your project root to handle routing:
* Routes the root URL (`/`) to load [static/index.html](file:///c:/Projects/Ai%20travel%20agent/static/index.html).
* Automatically proxies all `/api/*` network requests to your Railway backend URL, avoiding CORS cross-origin errors in the browser.

### Step 2: Deploy to Vercel
1. Log in to the **[Vercel Dashboard](https://vercel.com/)**.
2. Click **Add New** -> **Project**.
3. Import your `Ai travel agent` repository.
4. Keep the **Framework Preset** as **Other** (Vercel will detect it as a static project).
5. In **Root Directory**, you can keep it as the project root (thanks to `vercel.json` routing).
6. Click **Deploy**.

---

## 4. Code Optimizations Completed

To support this deployment architecture, we implemented the following changes:

### A. CORS Security in Backend
In [app/main.py](file:///c:/Projects/Ai%20travel%20agent/app/main.py#L14), we read allowed origins from the environment variable:
```python
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]
```
This enables secure CORS checks in production while retaining open settings for local testing.

### B. Production Host Binding in Uvicorn
In [run.py](file:///c:/Projects/Ai%20travel%20agent/run.py#L6), we configured the server to bind to `0.0.0.0` and disable code reloading in production:
```python
port = int(os.environ.get("PORT", 8000))
is_prod = os.environ.get("PORT") is not None or os.environ.get("RAILWAY_ENVIRONMENT") is not None
host = "0.0.0.0" if is_prod else "127.0.0.1"
uvicorn.run("app.main:app", host=host, port=port, reload=not is_prod)
```

### C. Dynamic Endpoint Configuration in Frontend
In [static/index.html](file:///c:/Projects/Ai%20travel%20agent/static/index.html#L676), we added a dynamic `API_BASE_URL` config:
```javascript
const API_BASE_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.hostname === '::1')
    ? ''
    : 'https://traveller-backend-production.up.railway.app'; // Update this with your Railway backend URL
```
This ensures the client automatically targets the correct API regardless of whether it is running on your local machine or deployed live.
