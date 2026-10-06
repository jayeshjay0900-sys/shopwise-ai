# 🚀 ShopWise AI - Complete Setup Guide

## ✅ Your API Keys Are Configured!

Your Groq and Tavily API keys are already set up in `backend/.env` - no additional configuration needed!

## 📂 Project Location

```
C:\Users\Lenovo\AppData\Local\Claude-3p\local-agent-mode-sessions\47427438\00000000\249a2052\outputs\shopwise-ai
```

## 🎯 Two Ways to Run

### Option 1: Automated Setup (Easiest!) ⚡

1. **Navigate to the project folder**
2. **Double-click `setup.bat`** - This will:
   - Install all backend dependencies
   - Install all frontend dependencies
   - Takes ~5 minutes

3. **Double-click `start.bat`** - This will:
   - Start backend server
   - Start frontend server
   - Open browser automatically at http://localhost:3000

### Option 2: Manual Setup 🛠️

#### Backend Setup:
```bash
cd shopwise-ai/backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
✅ Backend runs at: http://localhost:8000

#### Frontend Setup (New Terminal):
```bash
cd shopwise-ai/frontend
npm install
npm run dev
```
✅ Frontend runs at: http://localhost:3000

## 🧪 Test the Application

Try these example queries:

1. **"apple macbooks"** - Tests no-budget handling (budget should be null)
2. **"best gaming laptop under 1 lakh"** - Tests budget parsing + use case
3. **"LOQ laptops under 2 lakhs"** - Tests model detection + budget
4. **"best phone for camera under ₹50,000"** - Tests feature + budget
5. **"laptop for coding"** - Tests use case detection
6. **"iPhone 17 vs Galaxy S26"** - Tests comparison mode

## 🧪 Run Tests

```bash
cd shopwise-ai/backend
pytest test_requirement_extractor.py -v
pytest test_filter_scorer.py -v
```

## 📊 What You Get

### Backend Features:
- ✅ Intelligent budget parsing (₹50k, 1 lakh, 1.5 lakhs)
- ✅ NEVER invents budgets ("apple macbooks" → budget=null)
- ✅ Hard filtering BEFORE ranking
- ✅ Price validation (rejects ₹0-₹10)
- ✅ Deterministic Python scoring
- ✅ Review sentiment only when available
- ✅ Minimized API calls (focused queries)
- ✅ Graceful error handling

### Frontend Features:
- ✅ Modern gradient UI design
- ✅ Search with example queries
- ✅ Detected requirements display
- ✅ Product cards with match scores
- ✅ Specifications, pros/cons
- ✅ Review sentiment visualization
- ✅ AI-powered recommendations
- ✅ Comparison mode support

### Test Coverage:
- ✅ 40+ unit tests
- ✅ Budget parsing tests
- ✅ No-budget query tests
- ✅ Brand/model detection tests
- ✅ Filtering tests
- ✅ Price validation tests
- ✅ Scoring tests

## 🎨 UI Features

- **Gradient background** - Purple to blue gradient
- **Responsive design** - Works on all screen sizes
- **Match scores** - Visual indicators (🥇🥈🥉)
- **Color-coded requirements** - Easy to scan
- **Review sentiment bars** - Visual percentage display
- **Loading states** - Animated spinner
- **Error handling** - User-friendly messages

## 📁 Project Structure

```
shopwise-ai/
├── setup.bat          ← Run this first!
├── start.bat          ← Then run this to start
├── QUICKSTART.md
├── README.md
├── GET_STARTED.md     ← You are here
├── backend/
│   ├── .env          ← Your API keys (configured!)
│   ├── main.py
│   ├── requirement_extractor.py
│   ├── tavily_researcher.py
│   ├── product_processor.py
│   ├── product_filter.py
│   ├── product_scorer.py
│   ├── recommendation_generator.py
│   ├── models.py
│   ├── requirements.txt
│   ├── test_requirement_extractor.py
│   └── test_filter_scorer.py
└── frontend/
    ├── package.json
    ├── vite.config.ts
    ├── tailwind.config.js
    ├── src/
    │   ├── App.tsx
    │   ├── main.tsx
    │   ├── api.ts
    │   ├── types.ts
    │   └── components/
    │       ├── SearchBar.tsx
    │       ├── Requirements.tsx
    │       ├── ProductList.tsx
    │       ├── Recommendation.tsx
    │       ├── LoadingState.tsx
    │       └── ErrorMessage.tsx
    └── ... (config files)
```

## ⚡ Quick Commands Reference

### Start Application:
```bash
# Backend
cd backend && venv\Scripts\activate && python main.py

# Frontend (new terminal)
cd frontend && npm run dev
```

### Stop Application:
- Press `Ctrl + C` in each terminal

### Run Tests:
```bash
cd backend
pytest -v
```

### Rebuild Frontend:
```bash
cd frontend
npm run build
```

## 🔍 Verification Checklist

After starting, verify:
- [ ] Backend health: http://localhost:8000/health
- [ ] Frontend loads: http://localhost:3000
- [ ] Search works with example queries
- [ ] Requirements display correctly
- [ ] Products show with match scores
- [ ] Recommendation appears
- [ ] No console errors

## 🐛 Troubleshooting

**Backend won't start:**
- Verify Python 3.8+ installed: `python --version`
- Check if port 8000 is available
- Verify .env file exists in backend/
- Check API keys are valid

**Frontend won't start:**
- Verify Node.js 18+ installed: `node --version`
- Check if port 3000 is available
- Try deleting node_modules and running `npm install` again

**No results:**
- Check backend console for errors
- Verify API keys in .env are correct
- Check internet connection
- Try a simpler query like "apple macbooks"

**Tests fail:**
- Make sure pytest is installed: `pip install pytest pytest-asyncio`
- Run from backend directory
- Check Python path

## 📞 Support

If you encounter issues:
1. Check the backend console for error messages
2. Check the browser console (F12) for frontend errors
3. Verify API keys are active and have credits
4. Try restarting both servers

## 🎉 You're Ready!

Your ShopWise AI is configured and ready to run!

**Next Steps:**
1. Run `setup.bat` (first time only)
2. Run `start.bat` (every time)
3. Start shopping! 🛍️

---

**Built on:** October 6, 2026
**Tech Stack:** React, TypeScript, Vite, Tailwind CSS, FastAPI, Python, Groq AI, Tavily
