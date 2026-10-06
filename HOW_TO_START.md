# 🚀 STEP-BY-STEP STARTUP GUIDE

## The ERR_CONNECTION_REFUSED error means the servers aren't started yet!

Follow these steps to start your ShopWise AI:

---

## 📍 STEP 1: Open the Project Folder

1. Press `Windows + R`
2. Paste this path:
   ```
   C:\Users\Lenovo\AppData\Local\Claude-3p\local-agent-mode-sessions\47427438\00000000\249a2052\outputs\shopwise-ai
   ```
3. Press Enter

---

## 🔧 STEP 2: Start Backend Server

1. Open **Command Prompt** or **PowerShell** in the project folder
2. Run these commands **one by one**:

```bash
cd backend
python -m pip install fastapi uvicorn python-dotenv pydantic httpx groq --user
python main.py
```

✅ You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

⚠️ **IMPORTANT:** Leave this window open! Don't close it.

---

## 🎨 STEP 3: Start Frontend Server

1. Open a **NEW** Command Prompt/PowerShell window
2. Navigate to the project folder again
3. Run these commands:

```bash
cd frontend
npm install
npm run dev
```

✅ You should see:
```
  VITE v5.0.8  ready in 2000 ms

  ➜  Local:   http://localhost:3000/
```

⚠️ **IMPORTANT:** Leave this window open too!

---

## 🌐 STEP 4: Open Your Browser

Open Chrome/Edge and go to:
```
http://localhost:3000
```

---

## 🐛 If It Still Doesn't Work:

### Backend Issues:
```bash
# Check if Python is installed
python --version

# If that fails, try:
python3 --version

# Or:
py --version
```

### Frontend Issues:
```bash
# Check if Node.js is installed
node --version

# If not installed, download from:
# https://nodejs.org/
```

### Port Already in Use:
If you see "port already in use", change the ports:

**Backend** - Edit `backend/main.py`, change line at bottom:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed from 8000
```

**Frontend** - Edit `frontend/vite.config.ts`, change:
```typescript
server: {
  port: 3001,  // Changed from 3000
```

---

## 📋 Quick Checklist:

- [ ] Python installed (3.8+)
- [ ] Node.js installed (18+)
- [ ] Opened project folder
- [ ] Started backend (python main.py)
- [ ] Started frontend (npm run dev)
- [ ] Both terminal windows still open
- [ ] Opened http://localhost:3000

---

## 💡 Still Having Issues?

**Option 1: Check if servers are running**
- Backend: Open http://localhost:8000/health in browser
- Should show: `{"status":"healthy","groq_configured":true,"tavily_configured":true}`

**Option 2: Check for errors**
- Look at the terminal windows for error messages
- Share the error messages if you need help

**Option 3: Restart everything**
- Close both terminal windows
- Start fresh from STEP 2

---

## ✅ Once It's Working:

Try these example searches:
- `apple macbooks`
- `best gaming laptop under 1 lakh`
- `LOQ laptops under 2 lakhs`
- `iPhone 17 vs Galaxy S26`

---

**Your API keys are already configured! Just start the servers and you're good to go!** 🚀
