# StockVision AI 📈
**The Ultimate Intelligence-First Trading Terminal**

StockVision AI is a comprehensive, all-in-one financial research and prediction platform. It bridges the gap between institutional-grade analytics and retail trading by combining real-time data from multiple high-fidelity sources with state-of-the-art Artificial Intelligence and Machine Learning models.

## 🌟 Why StockVision AI? (All-In-One Platform)
Unlike traditional trading tools, StockVision AI doesn't just show you data—it **thinks** about it. By integrating technical forecasting, social sentiment, and LLM-driven reasoning, it provides a 360-degree view of any asset.

### 📊 Massive Asset Coverage
*   **2,000+ Stocks & Assets**: Support for the **entire NSE (India) master list**, the full **S&P 500 (US)**, major global indices (^NSEI, ^GSPC, ^N225), and top Cryptocurrencies (BTC, ETH).
*   **Instant Search**: A centralized command center to switch between global markets in milliseconds.

## 🚀 Advanced AI & Machine Learning Features

### 1. Dual-Core AI Intelligence Engine
*   **Primary Brain**: **Google Gemini 1.5 Flash**—Optimized for complex financial reasoning, executive tone decoding, and conversational research.
*   **Fail-Safe Engine**: **Groq (Llama 3.3 70B)**—A high-speed fallback system that ensures the platform remains operational even if Gemini hits rate limits.

### 2. Predictive Neural Network Suite
The platform runs a specialized FastAPI backend that trains and executes an ensemble of models for every prediction request:
*   **PatchTST (Transformer)**: A state-of-the-art transformer model for long-term time-series forecasting.
*   **LSTM (Long Short-Term Memory)**: Captures sequential patterns and market momentum.
*   **ARIMA**: Classic statistical modeling for baseline trend analysis.

### 3. AI Research Debate Engine
Simulates an institutional investment committee:
*   **Bull Agent**: Builds the strongest possible growth case.
*   **Bear Agent**: Identifies hidden risks, debt issues, and overvaluation.
*   **Judge Agent**: Synthesizes both cases into a final verdict and a conviction score (1-10).

## 📡 Multi-Source Data Integrations (API Ecosystem)
StockVision AI pulls from a diverse array of APIs to provide "Alpha" insights:
*   **Reddit Social Pulse**: Real-time scanning of subreddits (r/wallstreetbets, r/IndianStreetBets, r/stocks) to calculate a **Retail Hype Score**.
*   **Alpha Vantage**: Specialized global news sentiment analysis and upcoming earnings calendars.
*   **Groww API**: Deep integration for zero-latency Indian market quotes and simulated order execution.
*   **Yahoo Finance**: Core infrastructure for historical price data, financial statements, and institutional shareholding patterns.
*   **Custom News Aggregator**: Real-time decoding of "Executive Tone" (Confident vs. Uncertain) from management communications.

## 💻 Premium Terminal Experience
*   **Modern UI Fragments**: Built with Streamlit 1.55+ fragments for **instant, single-click updates**. No more double-loading charts.
*   **Infinite Global Ticker**: A sleek, animated tape tracking 40+ global movers across US and Indian markets.
*   **Business Health Architecture**: Deep-dive into 12+ real-time metrics: ROE, ROA, Debt-to-Equity, Operating Margins, Quick Ratios, and P/B Ratios.
*   **AI Strategist Chat**: A context-aware advisor that knows your current ticker's fundamentals and helps you build step-by-step investment rationales.

## 📁 Project Architecture
```text
stockvision-ai/
├── app/
│   ├── agents/          # Brain: Gemini & Groq LLM logic
│   ├── api/             # Nerve Center: FastAPI prediction server
│   ├── data/            # Ingestion: Multi-API data pipelines (Reddit, Groww, AV)
│   ├── features/        # Engineering: Technical indicators & math
│   ├── models/          # ML: PatchTST, LSTM, ARIMA implementations
│   ├── sentiment/       # Analysis: NLP-based news & social scoring
│   └── services/        # Logic: Intelligence synthesis & trending engines
├── dashboard/
│   └── streamlit_app.py # UI: The Premium Trading Terminal
├── lightning_logs/      # (Ignored) Model training checkpoints
└── requirements.txt     # All-in-one dependency list
```

## ⚙️ Quick Start

1. **Clone & Install**:
   ```bash
   git clone https://github.com/yourusername/stockvision-ai.git
   pip install -r requirements.txt
   ```

2. **Configure API Keys (.env)**:
   ```env
   GEMINI_API_KEY=...
   GROQ_API_KEY=...
   GROWW_API_KEY=...
   ALPHA_VANTAGE_API_KEY=...
   ```

3. **Launch Platform**:
   *   **Backend**: `uvicorn app.api.server:app --port 8000`
   *   **Frontend**: `streamlit run dashboard/streamlit_app.py`

## Project Demo
Demo Link : https://youtu.be/xH7hLXebkPg 

## Author
Aayush Tripathi
