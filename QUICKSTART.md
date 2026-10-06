# ShopWise AI - Quick Start Guide

## 📦 Project Structure
```
shopwise-ai/
├── backend/          # FastAPI backend
├── frontend/         # React + TypeScript frontend
└── README.md         # Full documentation
```

## 🚀 Quick Start (3 Steps)

### Step 1: Setup Backend

1. Open terminal in `shopwise-ai/backend/`
2. Create virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate it:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create `.env` file and add your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

### Step 2: Setup Frontend

1. Open terminal in `shopwise-ai/frontend/`
2. Install dependencies:
   ```bash
   npm install
   ```

### Step 3: Run the Application

**Terminal 1 (Backend):**
```bash
cd shopwise-ai/backend
python main.py
```
✅ Backend running at: http://localhost:8000

**Terminal 2 (Frontend):**
```bash
cd shopwise-ai/frontend
npm run dev
```
✅ Frontend running at: http://localhost:3000

**Open browser:** http://localhost:3000

## 🧪 Run Tests

```bash
cd shopwise-ai/backend
pytest test_requirement_extractor.py -v
pytest test_filter_scorer.py -v
```

## 📝 Try These Queries

- `apple macbooks` (no budget)
- `best gaming laptop under 1 lakh`
- `LOQ laptops under 2 lakhs`
- `best phone for camera under ₹50,000`
- `laptop for coding`
- `iPhone 17 vs Galaxy S26` (comparison)

## 🔑 Getting API Keys

1. **Groq API Key**: https://console.groq.com/keys
2. **Tavily API Key**: https://app.tavily.com/

## ❓ Troubleshooting

**Backend won't start:**
- Check if port 8000 is available
- Verify API keys in `.env` file
- Check Python version (3.8+)

**Frontend won't start:**
- Check if port 3000 is available
- Verify Node.js version (18+)
- Try `npm install` again

**No results:**
- Verify API keys are correct
- Check internet connection
- Check backend console for errors

## 📚 Full Documentation

See `README.md` for complete documentation including:
- Architecture details
- API endpoints
- All accuracy rules
- Testing guide
- Troubleshooting

---

**Built with:** React, TypeScript, FastAPI, Groq AI & Tavily
