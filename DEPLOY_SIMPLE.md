# 🚀 SIMPLE DEPLOYMENT - One Platform Only!

Deploy your entire ShopWise AI on **ONE** Render instance - frontend + backend together!

---

## ✅ Project Size: PERFECT for Render!
- Backend: 72KB
- Frontend: 30KB  
- **Total with dependencies: ~150MB** (well under Render's 512MB limit!)

---

## 📋 What You Need
1. **GitHub Account** (free) - https://github.com
2. **Render Account** (free) - https://render.com
3. That's it! No Vercel needed!

---

# 🎯 DEPLOYMENT STEPS (15 minutes)

## Step 1: Push to GitHub

### 1.1 Open Command Prompt in project folder
```bash
cd C:\Users\Lenovo\AppData\Local\Claude-3p\local-agent-mode-sessions\47427438\00000000\249a2052\outputs\shopwise-ai
```

### 1.2 Initialize Git
```bash
git init
git add .
git commit -m "ShopWise AI - Ready for deployment"
```

### 1.3 Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `shopwise-ai`
3. Make it **Public** (required for free Render)
4. Click "Create repository"

### 1.4 Push Code
```bash
git remote add origin https://github.com/YOUR_USERNAME/shopwise-ai.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy on Render (Everything in One!)

### 2.1 Sign Up for Render
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub

### 2.2 Create Web Service
1. Click "New +" → "Web Service"
2. Click "Connect" next to your `shopwise-ai` repository
3. If you don't see it, click "Configure account" and grant access

### 2.3 Configure Service

**Basic Settings:**
- **Name:** `shopwise-ai`
- **Region:** Choose closest to you (e.g., Singapore, Oregon, Frankfurt)
- **Branch:** `main`
- **Root Directory:** Leave empty (we'll use build script)
- **Runtime:** `Python 3`

**Build & Deploy:**
- **Build Command:**
```bash
cd frontend && npm install && npm run build && cd .. && mkdir -p backend/static && cp -r frontend/dist/* backend/static/ && cd backend && pip install -r requirements.txt
```

- **Start Command:**
```bash
cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Instance Type:**
- Select **Free** ($0/month)

### 2.4 Add Environment Variables

Click "Advanced" → "Add Environment Variable"

Add these TWO variables:
- **Key:** `GROQ_API_KEY`  
  **Value:** `YOUR_GROQ_API_KEY_HERE`

- **Key:** `TAVILY_API_KEY`  
  **Value:** `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`

### 2.5 Deploy!
1. Click "Create Web Service"
2. Wait 5-10 minutes (Render will build everything)
3. Watch the logs - you'll see:
   - Installing Node packages
   - Building React frontend
   - Installing Python packages
   - Starting server

### 2.6 Get Your URL
Once deployed, you'll get a URL like:
```
https://shopwise-ai.onrender.com
```

**🎉 That's it! Your app is LIVE!**

---

## 🌐 Test Your Deployment

1. Open your Render URL: `https://shopwise-ai.onrender.com`
2. You should see the ShopWise AI interface!
3. Try searching:
   - `apple macbooks`
   - `best gaming laptop under 1 lakh`
   - `LOQ laptops under 2 lakhs`

---

## 🔧 How It Works

**Single Server Setup:**
- FastAPI serves the API endpoints (`/search`, `/health`)
- FastAPI also serves the built React app as static files
- Frontend makes API calls to the same domain (no CORS issues!)
- Everything runs on ONE Render instance

**What Happens During Build:**
1. Installs Node.js packages
2. Builds React app (creates optimized production files)
3. Copies built files to `backend/static/`
4. Installs Python packages
5. Starts FastAPI server
6. FastAPI serves frontend at `/` and API at `/search`, `/health`

---

## 💰 Cost Breakdown

**Render Free Tier:**
- ✅ 750 hours/month (more than enough for 24/7 uptime)
- ✅ 512 MB RAM
- ✅ 0.1 CPU
- ✅ Auto-sleep after 15 min inactivity
- ✅ Free custom domains
- ✅ Free SSL certificate

**Total Cost: $0/month** 🎉

**Note:** Free tier spins down after 15 minutes of inactivity. First request after sleep takes ~30-60 seconds to wake up.

---

## 🔄 Update Your App

Whenever you make changes:

```bash
git add .
git commit -m "Your changes description"
git push
```

Render automatically redeploys! (takes ~5 minutes)

---

## 🐛 Troubleshooting

### Build Fails

**Error: "npm not found"**
- Render automatically installs Node.js, wait for it to finish

**Error: "Module not found"**
- Check that all files are committed to Git
- Verify `requirements.txt` and `package.json` are present

### App Doesn't Load

**Check the logs:**
1. Go to Render Dashboard
2. Click your service
3. Click "Logs" tab
4. Look for errors in red

**Common issues:**
- Environment variables not set (check Settings → Environment)
- Build didn't complete (check full log)
- Port not binding (should use `$PORT` variable)

### API Requests Fail

**Check:**
- Backend is running (green status in dashboard)
- Environment variables are set correctly
- Open `/health` endpoint: `https://your-app.onrender.com/health`
- Should return: `{"status":"healthy","groq_configured":true,"tavily_configured":true}`

### Slow First Load

This is normal! Free tier spins down after 15 min inactivity.
- First request: 30-60 seconds (waking up)
- Subsequent requests: Fast!

**Solutions:**
- Use cron-job.org to ping your app every 10 minutes (keeps it awake)
- Upgrade to paid tier ($7/month - never sleeps)

---

## 📊 Monitor Your App

**Render Dashboard Shows:**
- ✅ Deployment status
- ✅ Live logs (see all requests)
- ✅ Metrics (CPU, memory, bandwidth)
- ✅ Recent deploys
- ✅ Environment variables

**Logs show:**
- All API requests
- Errors and stack traces
- Startup messages
- User searches

---

## 🎨 Custom Domain (Optional)

Want `shopwise.yourdomain.com`?

1. Go to Render Dashboard → Your service
2. Click "Settings" → "Custom Domains"
3. Click "Add Custom Domain"
4. Enter your domain
5. Add DNS record (Render shows you what to add)
6. Done! Free SSL included!

---

## ⚡ Quick Reference

**Your URLs:**
- Main app: `https://shopwise-ai.onrender.com/`
- Health check: `https://shopwise-ai.onrender.com/health`
- API endpoint: `https://shopwise-ai.onrender.com/search`

**Update deployment:**
```bash
git add .
git commit -m "Update"
git push
```

**View logs:**
Render Dashboard → Your service → Logs

**Restart service:**
Render Dashboard → Manual Deploy → "Clear build cache & deploy"

---

## ✅ Advantages of Single Platform

✅ **Simpler** - One platform instead of two  
✅ **No CORS** - Frontend and backend on same domain  
✅ **Cheaper** - Free tier is enough  
✅ **Faster** - No cross-domain requests  
✅ **Easier** - One place to manage everything  

---

## 🎉 You're Done!

Your ShopWise AI is now:
- ✅ Deployed online at one URL
- ✅ Accessible from anywhere in the world
- ✅ Running on free cloud infrastructure
- ✅ Auto-updating when you push code
- ✅ Serving both frontend and backend

**Share your URL and start shopping!** 🛍️

---

**Deployed:** October 6, 2026  
**Platform:** Render (Single Instance)  
**Stack:** React + TypeScript + FastAPI + Groq + Tavily  
**Hosting Cost:** $0/month

