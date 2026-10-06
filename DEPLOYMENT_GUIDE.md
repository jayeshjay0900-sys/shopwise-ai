# 🚀 Deploy ShopWise AI to the Cloud

## Deploy your app online in 10 minutes - NO localhost needed!

---

## 📋 What You'll Need

1. **GitHub Account** (free) - https://github.com
2. **Render Account** (free) - https://render.com
3. **Vercel Account** (free) - https://vercel.com
4. Your API Keys (already configured!)

---

## 🎯 Deployment Strategy

- **Backend** → Render (Free tier, always running)
- **Frontend** → Vercel (Free tier, lightning fast)

---

# PART 1: Deploy Backend to Render

## Step 1: Push Code to GitHub

### 1.1 Install Git (if not installed)
Download from: https://git-scm.com/download/win

### 1.2 Initialize Git Repository
Open Command Prompt in your project folder:

```bash
cd C:\Users\Lenovo\AppData\Local\Claude-3p\local-agent-mode-sessions\47427438\00000000\249a2052\outputs\shopwise-ai

git init
git add .
git commit -m "Initial commit - ShopWise AI"
```

### 1.3 Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `shopwise-ai`
3. Make it **Public** (required for free Render)
4. Click "Create repository"
5. Copy the commands shown and run them:

```bash
git remote add origin https://github.com/YOUR_USERNAME/shopwise-ai.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy Backend on Render

### 2.1 Create Render Account
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"

### 2.2 Configure Backend Service

**Connect Repository:**
- Select `shopwise-ai` repository
- Click "Connect"

**Settings:**
- **Name:** `shopwise-ai-backend`
- **Region:** Choose closest to you
- **Root Directory:** `backend`
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Instance Type:** `Free`

**Environment Variables:**
Click "Add Environment Variable" and add:
- Key: `GROQ_API_KEY`, Value: `YOUR_GROQ_API_KEY_HERE`
- Key: `TAVILY_API_KEY`, Value: `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`

### 2.3 Deploy!
- Click "Create Web Service"
- Wait 5-10 minutes for deployment
- You'll get a URL like: `https://shopwise-ai-backend.onrender.com`

✅ **Test your backend:**
Open: `https://shopwise-ai-backend.onrender.com/health`

You should see:
```json
{
  "status": "healthy",
  "groq_configured": true,
  "tavily_configured": true
}
```

**⚠️ IMPORTANT:** Copy your backend URL! You'll need it next.

---

# PART 2: Deploy Frontend to Vercel

## Step 1: Update Frontend Configuration

### 1.1 Update API URL

Open `frontend/src/api.ts` and change:

```typescript
// FROM:
const API_BASE_URL = '/api';

// TO:
const API_BASE_URL = 'https://shopwise-ai-backend.onrender.com';
```

Replace with YOUR actual Render URL!

### 1.2 Update vite.config.ts

Open `frontend/vite.config.ts` and update:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
  },
  // Remove the proxy section - not needed for production
})
```

### 1.3 Commit Changes

```bash
git add .
git commit -m "Update API URL for production"
git push
```

## Step 2: Deploy Frontend on Vercel

### 2.1 Create Vercel Account
1. Go to https://vercel.com
2. Sign up with GitHub
3. Click "Add New..." → "Project"

### 2.2 Import Repository
- Click "Import" next to `shopwise-ai`
- **Root Directory:** `frontend`
- **Framework Preset:** Vite
- **Build Command:** `npm run build`
- **Output Directory:** `dist`

### 2.3 Deploy!
- Click "Deploy"
- Wait 2-3 minutes
- You'll get a URL like: `https://shopwise-ai.vercel.app`

✅ **Your app is LIVE!** 🎉

---

# 🌐 Access Your Deployed App

Your ShopWise AI is now live at:
- **Frontend:** `https://shopwise-ai.vercel.app` (or your custom URL)
- **Backend:** `https://shopwise-ai-backend.onrender.com`

Share the frontend URL with anyone!

---

# 🧪 Test Your Deployment

1. Open your Vercel URL in browser
2. Try these queries:
   - `apple macbooks`
   - `best gaming laptop under 1 lakh`
   - `LOQ laptops under 2 lakhs`
   - `iPhone 17 vs Galaxy S26`

---

# 🔧 Troubleshooting

## Backend Issues

**"Application failed to start"**
- Check Render logs: Dashboard → Your service → Logs
- Verify environment variables are set correctly
- Make sure `requirements.txt` is in backend folder

**API requests failing:**
- Check CORS is enabled in `main.py` (it is!)
- Verify backend URL in frontend `api.ts`

## Frontend Issues

**Build fails:**
- Check all TypeScript errors are fixed
- Make sure `package.json` is correct
- Try building locally first: `npm run build`

**Can't connect to backend:**
- Double-check the API_BASE_URL in `api.ts`
- Make sure backend is running (check Render dashboard)
- Check browser console for errors (F12)

## Free Tier Limitations

**Render Free Tier:**
- Spins down after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds
- 750 hours/month (enough for constant use)

**Vercel Free Tier:**
- Unlimited deployments
- 100GB bandwidth/month
- Fast CDN delivery

---

# 🎨 Custom Domain (Optional)

## Add Custom Domain to Vercel

1. Go to Vercel Dashboard → Your project → Settings → Domains
2. Add your domain (e.g., `shopwise-ai.com`)
3. Update DNS records as instructed
4. Done! Your app will be at your custom domain

---

# 🔄 Update Your Deployment

Whenever you make changes:

```bash
# Make your changes
git add .
git commit -m "Description of changes"
git push

# Render and Vercel will auto-deploy!
```

Both platforms automatically redeploy when you push to GitHub!

---

# 📊 Monitor Your App

**Render Dashboard:**
- View logs: See all requests and errors
- Metrics: CPU, memory usage
- Manual deploy: Redeploy button

**Vercel Dashboard:**
- Analytics: Page views, performance
- Deployment history: Roll back if needed
- Preview deployments: Test before production

---

# 💰 Cost

**Everything is FREE!**
- GitHub: Free for public repos
- Render: Free tier (750 hours/month)
- Vercel: Free tier (unlimited deployments)

No credit card required for any of them!

---

# 🎉 You're Done!

Your ShopWise AI is now:
✅ Deployed online
✅ Accessible from anywhere
✅ Automatically updates when you push code
✅ Running on free cloud platforms
✅ Using your API keys securely

Share your URL and start shopping! 🛍️

---

**Deployed:** October 6, 2026  
**Stack:** React + TypeScript + FastAPI + Groq + Tavily  
**Hosting:** Vercel + Render

