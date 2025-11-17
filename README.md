# 🚀 Full-Stack Prototype Boilerplate

This repository contains a modern, secure boilerplate for building full-stack applications, featuring Docker Compose for easy deployment, a decoupled API/Frontend, and optional Firebase authentication.

## 📦 Stack Overview

| Component | Port (Dev) | Framework/Tool | Purpose |
| :--- | :--- | :--- | :--- |
| **Frontend** | `5173` | Vue 3 (Vite) | Client-side UI |
| **Backend API** | `8000` | FastAPI (Python) | High-performance API |
| **Database** | *(Internal)* | MongoDB | Persistent data storage |

## 🔑 Initial Setup (The First 5 Minutes)

### 1. Configure Environment Variables

Create a root `.env` file by copying the template, and fill in the values. **This file is git-ignored and contains secrets.**

```bash
cp .env.example .env
````

**⚠️ IMPORTANT SECRETS:** You *must* fill in the following:

  * `MONGO_USERNAME` & `MONGO_PASSWORD`
  * `FIREBASE_SERVICE_ACCOUNT_JSON` (Your Admin SDK JSON, as a single-line string)

### 2\. Configure Frontend Public Config

Configure the necessary public API URL and Firebase settings. **These are safe to commit.**

| File | Purpose | Key Variable to Check |
| :--- | :--- | :--- |
| `frontend/.env.development` | **Local Testing** | `VITE_API_URL=http://localhost:8000` |
| `frontend/.env.production` | **Production Build** | `VITE_API_URL=https://api.yourdomain.com` |

### 3\. Build & Run the Stack

Bring all services up:

```bash
docker compose up --build
```

## 🛠️ Development Endpoints

| Service | Access URL | Status Check |
| :--- | :--- | :--- |
| **Frontend (Vue)** | `http://localhost:5173` | UI is live. |
| **Backend (FastAPI)** | `http://localhost:8000` | Basic API access (CORS-restricted). |
| **MongoDB** | *(Internal Only)* | Accessible only by the `api` service. |

## 💡 Security Notes & Switches (For Future Me)

### 1\. Authentication Toggle

The entire application's authentication can be enabled/disabled using environment variables.

  * **Frontend:** `VITE_AUTH_ENABLED=true/false` (In `frontend/.env.*`)
  * **Backend:** `AUTH_ENABLED=true/false` (In root `.env`)

### 2\. Security Hardeners

  * **CORS Protection:** The `api` service is restricted to the domain defined by `CORS_ORIGIN` (e.g., `http://localhost:5173` or `https://www.prod-domain.com`).
  * **Database Isolation:** The MongoDB port (`27017`) is **not exposed** to the host machine for security. Use internal Docker network connections only.
  * **Production Deployment:** For production, remember to remove the `ports: 8000:8000` mapping on the `api` service and route traffic via a reverse proxy (e.g., Caddy).
