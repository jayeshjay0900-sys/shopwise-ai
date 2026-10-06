# ShopWise AI

A production-quality full-stack AI shopping agent that provides accurate, intelligent product recommendations.

## 🎯 Features

- **Accurate Requirement Extraction**: Parses natural language queries with precision
  - Budget parsing: ₹50,000, 50k, 1 lakh, 1.5 lakhs, under 2 lakh
  - Brand and model detection
  - Use case identification
  - Comparison mode support

- **Hard Filtering**: Products are filtered BEFORE ranking
  - Budget constraints strictly enforced
  - Brand and model requirements
  - Category filtering

- **Deterministic Scoring**: Python-based scoring algorithm
  - Brand match: 20 points
  - Model match: 20 points
  - Budget optimization: 15 points
  - Price availability: 10 points
  - Specifications: 10 points
  - Source reliability: 5 points

- **Price Validation**: Rejects corrupted prices (₹0, ₹1, ₹2, ₹5, ₹10)

- **Review Sentiment**: Only shown when available (never fabricated)

- **Professional UI**: Modern React+TypeScript+Tailwind interface

## 🏗️ Architecture

### Backend (FastAPI + Python)
- `main.py` - FastAPI application with CORS support
- `requirement_extractor.py` - Extract and parse shopping requirements
- `tavily_researcher.py` - Focused Tavily API research (minimized calls)
- `product_processor.py` - Extract products with LLM, validate with Python
- `product_filter.py` - Hard filtering before ranking
- `product_scorer.py` - Deterministic scoring algorithm
- `recommendation_generator.py` - Natural language recommendations
- `models.py` - Pydantic data models

### Frontend (React + TypeScript + Vite)
- Modern SaaS/AI interface
- Search bar with example queries
- Requirements display
- Product cards with specs, pros/cons, reviews
- AI-powered recommendations
- Error handling and loading states

## 📋 Requirements

- Python 3.8+
- Node.js 18+
- GROQ API Key
- Tavily API Key

## 🚀 Installation

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
```

5. Edit `.env` and add your API keys:
```
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## 🧪 Running Tests

### Backend Tests

```bash
cd backend
pytest test_requirement_extractor.py -v
pytest test_filter_scorer.py -v
```

## 🏃 Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
python main.py
```

Backend will run on: `http://localhost:8000`

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend will run on: `http://localhost:3000`

## 📝 Usage Examples

### Query Examples

1. **No Budget Query**
   ```
   apple macbooks
   ```
   - Expected: Budget = None, Brand = Apple

2. **Budget + Model Query**
   ```
   LOQ laptops under 2 lakhs
   ```
   - Expected: Budget = 200000, Model = LOQ

3. **Budget Only Query**
   ```
   laptops under 1 lakh
   ```
   - Expected: Budget = 100000, Category = laptop

4. **Use Case Query**
   ```
   best gaming laptop under 1 lakh
   ```
   - Expected: Use case = gaming, Budget = 100000

5. **Coding Use Case**
   ```
   laptop for coding
   ```
   - Expected: Use case = coding

6. **Comparison Query**
   ```
   iPhone 17 vs Galaxy S26
   ```
   - Expected: Comparison mode = True

## 🔍 Accuracy Rules

### Critical Rules Implemented

1. **Never invent a budget**: "apple macbooks" has `budget=null`
2. **Correct parsing**: ₹50,000, 50k, 1 lakh, 1.5 lakhs
3. **Hard filters BEFORE ranking**: Products failing requirements are rejected
4. **Price validation**: Reject ₹0, ₹1, ₹2, ₹5, ₹10
5. **Product/price/source mapping**: Always from same product
6. **No generic pages**: "Best Laptops Under 1 Lakh" rejected
7. **No fabricated reviews**: Return "Review sentiment unavailable"
8. **Comparison accuracy**: Only compare requested products
9. **Deterministic validation**: Python validation/filtering/scoring
10. **Minimize API calls**: Focused queries, avoid loops

## 🛠️ Tech Stack

**Backend:**
- FastAPI 0.104.1
- Groq (LLM)
- Tavily (Web Research)
- Pydantic (Data Validation)
- Python 3.8+

**Frontend:**
- React 18
- TypeScript 5
- Vite 5
- Tailwind CSS 3
- Axios

## 🧩 API Endpoints

### `POST /search`
Search for products based on natural language query.

**Request:**
```json
{
  "query": "best gaming laptop under 1 lakh"
}
```

**Response:**
```json
{
  "query": "best gaming laptop under 1 lakh",
  "requirements": {
    "category": "laptop",
    "budget_max": 100000,
    "use_case": "gaming",
    ...
  },
  "products": [...],
  "recommendation": "...",
  "comparison_mode": false,
  "error": null
}
```

### `GET /health`
Check API health status.

## 🔧 Development

### Backend Development
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Build Frontend for Production
```bash
cd frontend
npm run build
```

## 📊 Testing

### Run All Backend Tests
```bash
cd backend
pytest -v
```

### Test Coverage
- Requirement extraction (budget parsing, brand detection, etc.)
- Product filtering (brand, model, budget, category)
- Price validation (corrupt price rejection)
- Deterministic scoring

## ⚠️ Known Limitations

1. **API Dependencies**: Requires active Groq and Tavily API keys
2. **Indian Market Focus**: Primarily searches Indian e-commerce sites
3. **Search Depth**: Limited to top 5 results per query to minimize API costs
4. **Review Analysis**: Only available when review content is found in search results
5. **Product Images**: Not always available from search results

## 🐛 Error Handling

- Graceful API failure handling
- Invalid API key detection
- No results found messaging
- Timeout handling
- Malformed search result protection

## 📄 License

MIT

## 👥 Author

Built with React, TypeScript, FastAPI, Groq AI & Tavily

---

**Note**: This is a production-quality implementation following all accuracy rules and best practices for AI shopping agents.
