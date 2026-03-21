# StockVision AI 📈
**Intelligence-First Trading Terminal**

StockVision AI is a premium, institutional-grade trading dashboard that combines real-time market data with cutting-edge artificial intelligence. It utilizes state-of-the-art predictive neural networks and Large Language Models (LLMs) to provide deep financial insights, stock forecasts, and comprehensive business health analyses.

## 🚀 Key Features

*   **Premium Interactive Terminal**: A sleek, dark-themed Streamlit UI featuring instant, single-click dynamic charts and an infinite global ticker tape tracking major US and Indian movers.
*   **AI Reasoning & Debate Engine**: Powered by **Google Gemini 1.5 Flash** (with a Groq Llama-3.3-70B fallback). It synthesizes complex financial data and simulates a debate between a "Bull" and "Bear" investor, providing a final verdict and conviction score.
*   **Predictive Neural Engine**: Utilizes advanced forecasting models including **PatchTST (Transformer)**, **LSTM**, and **ARIMA** via a FastAPI backend to predict short-term price movements.
*   **Business Health Architecture**: Instant visibility into critical financial metrics: Market Cap, ROE, ROA, P/E Ratios, Debt-to-Equity, Quick Ratios, and Operating Margins.
*   **Market Context Intelligence**: Real-time aggregation of top news headlines and a "Retail Hype Score" based on social media (Reddit) pulse.
*   **Global Shareholding**: Deep dive into institutional and major shareholder breakdowns.
*   **AI Strategist Chat**: An integrated conversational AI advisor for personalized, context-aware financial research.

## 🛠️ Technology Stack
*   **Frontend**: Streamlit, Altair (Charting)
*   **Backend API**: FastAPI, Uvicorn
*   **AI & LLMs**: Google Generative AI (Gemini 1.5 Flash), Groq API (Llama 3.3)
*   **Machine Learning**: PyTorch, NeuralForecast (PatchTST), Scikit-learn, Statsmodels
*   **Data Sources**: yfinance, custom sentiment APIs

## 📁 Project Structure
```text
stockvision-ai/
├── app/
│   ├── agents/          # LLM integrations (Gemini, Groq)
│   ├── api/             # FastAPI server and routes
│   ├── data/            # Data ingestion (yfinance, news, tickers)
│   ├── features/        # Feature engineering & technical indicators
│   ├── models/          # ML Models (LSTM, ARIMA, Transformer)
│   └── services/        # Core business logic and intelligence aggregation
├── dashboard/
│   └── streamlit_app.py # Premium Streamlit Terminal UI
├── main.py              # Main execution script
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables (API Keys)
```

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/stockvision-ai.git
   cd stockvision-ai
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your API keys:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   GROQ_API_KEY=your_groq_api_key
   # Add other required keys (e.g., Alpha Vantage, Groww) if active
   ```

5. **Run the Application:**
   First, start the backend neural engine (FastAPI):
   ```bash
   uvicorn app.api.server:app --port 8000 &
   ```
   Then, launch the Premium Terminal:
   ```bash
   streamlit run dashboard/streamlit_app.py
   ```

## ⚠️ Disclaimer
StockVision AI is strictly for research and educational purposes. It does not constitute financial or regulated investment advice.
