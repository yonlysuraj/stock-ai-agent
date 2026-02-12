# Deploying Stock AI Agent to Vercel

This guide explains how to deploy the Stock AI Agent (Frontend + Backend) to Vercel for free.

## Prerequisites

1.  **GitHub Account**: You need a GitHub account to connect the repository to Vercel.
2.  **Vercel Account**: Sign up at [vercel.com](https://vercel.com) using your GitHub account.
3.  **API Keys**: Ensure you have your Groq API Key ready.

## Steps to Deploy

### 1. Push Code to GitHub

First, make sure your code is pushed to a GitHub repository.

```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### 2. Import Project in Vercel

1.  Go to your [Vercel Dashboard](https://vercel.com/dashboard).
2.  Click **"Add New..."** -> **"Project"**.
3.  Import the `stock-ai-agent` repository from your GitHub.

### 3. Configure Project Settings

Vercel might now detect this as a Node.js project because I added a `package.json` to the root. This is GOOD.

*   **Framework Preset**: Select `Vite` (or `Other` if `Vite` isn't an option, but `Vite` is best).
*   **Root Directory**: Leave as `.` (the default root). 

### 4. Build & Output Settings (CRITICAL STEP)

**If you see the "Backend API" page instead of your app, this setting is wrong.**

Expand **Build and Output Settings** and ensure they match EXACTLY:

*   **Build Command**: `cd frontend && npm install && npm run build`
*   **Output Directory**: `frontend/dist`  <-- **THIS IS THE MOST COMMON ERROR**

If Vercel defaults `Output Directory` to `dist` or `public`, you **MUST** change it to `frontend/dist`.

### 5. Environment Variables

Expand the **Environment Variables** section and add the following keys:

| Key | Value | Description |
| :--- | :--- | :--- |
| `GROQ_API_KEY` | `your_groq_api_key_here` | Required for AI analysis |
| `VITE_API_BASE` | *(Leave empty)* | Leave value empty to use relative paths |

*   **Note**: `VITE_API_BASE` is used by the frontend to talk to the backend. By leaving it empty, the frontend will automatically make requests to `/api/...` on the same domain, which avoids CORS issues.

### 6. Modify Install Command (Fixing Dependency Installation)

Vercel's default install command for Python might conflict with the Node.js build. 
However, since we configured `vercel.json`, Vercel should handle the `api/` folder as Serverless Functions automatically (installing from `requirements.txt`).

If you encounter a "Module not found" error during the Python build, add `VERCEL_FORCE_NO_BUILD_CACHE=1` to environment variables to force a fresh install.

### 7. Deploy

Click **Deploy**. Vercel will:
1.  Build the Frontend (Vite -> `frontend/dist`).
2.  Build the Backend (Python -> Serverless Functions at `/api`).
3.  Deploy everything to a URL like `https://stock-ai-agent.vercel.app`.

## Troubleshooting

### "Module not found app"
If the backend fails to find the `app` module, ensure `api/index.py` exists (I created it for you) and requires `requirements.txt` at the root (also verified).

### Database Errors
The application is configured to default to no database if one cannot be created. Since Vercel is read-only, the local SQLite database feature will be disabled automatically. This will not affect the analysis features.

### Yahoo Finance Issues
Sometimes `yfinance` blocks requests from data center IPs (like Vercel). If you see "No data found" errors:
1.  Try adding `YFINANCE_CACHE_DIR=/tmp` to environment variables.
2.  If issues persist, you might need a different stock data provider or a residential proxy, but it often works for low volume.

## Local Development vs. Production

*   **Local**: Run frontend (`npm run dev`) and backend (`python main.py`) separately. Frontend connects to `localhost:8000`.
*   **Production**: Everything runs on one domain. Frontend connects to `/api` (relative path).
