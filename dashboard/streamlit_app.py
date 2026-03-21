import sys
import os
# Ensure the project root is in PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import yfinance as yf
import requests
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime
from app.data.ticker_db import get_ticker_list
from app.agents.financial_agent import get_analyst_response
from app.utils.formatters import format_large_number
from app.utils.currency_mapper import get_currency_symbol
from app.services.trending_service import TrendingService

# --- PERFORMANCE CACHING ---
@st.cache_data(ttl=3600)
def get_master_tickers():
    return get_ticker_list()

@st.cache_data(ttl=3600)
def get_institutional_metadata(ticker):
    try:
        t = yf.Ticker(ticker)
        info = t.info
        return {
            "name": info.get("longName") or info.get("shortName") or ticker,
            "currency": info.get("currency", "USD"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "summary": info.get("longBusinessSummary", "N/A"),
            "info": info
        }
    except:
        return {"name": ticker, "currency": "USD", "sector": "N/A", "industry": "N/A", "summary": "N/A", "info": {}}

@st.cache_data(ttl=3600)
def get_shareholders(ticker):
    try:
        t = yf.Ticker(ticker)
        inst = t.institutional_holders
        if inst is not None and not inst.empty: return inst
        maj = t.major_holders
        if maj is not None and not maj.empty: return maj
        return None
    except: return None

@st.cache_data(ttl=60)
def fetch_live_quote(ticker):
    try:
        t = yf.Ticker(ticker)
        fast = t.fast_info
        lp = float(fast.last_price)
        pc = float(fast.previous_close)
        cp = ((lp - pc) / pc * 100) if pc else 0.0
        return {"price": lp, "change": cp}
    except: return {"price": 0.0, "change": 0.0}

@st.cache_data(ttl=300)
def fetch_terminal_chart(ticker, period, interval):
    try:
        t = yf.Ticker(ticker)
        df = t.history(period=period, interval=interval)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df
    except: return pd.DataFrame()

@st.cache_data(ttl=600)
def get_trending_movers(region):
    ts = TrendingService()
    return ts.fetch_trending(region)

# --- TERMINAL CONFIGURATION ---
st.set_page_config(page_title="StockVision AI | Premium Terminal", layout="wide", initial_sidebar_state="expanded")

# Initialize Session States
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "selected_ticker" not in st.session_state: st.session_state.selected_ticker = "AAPL" 
if "run_analysis" not in st.session_state: st.session_state.run_analysis = False
if "show_chat" not in st.session_state: st.session_state.show_chat = False
if "analysis_results" not in st.session_state: st.session_state.analysis_results = None

# --- PREMIUM BLACK THEME ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;300;400;500;600;700;800&display=swap');
    html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif; background-color: #000000 !important; color: #FFFFFF !important; }
    header, footer, #MainMenu {visibility: hidden;}
    div[data-baseweb="select"] { margin-top: -5px !important; }
    div[data-testid="stMetric"] { background: rgba(255, 255, 255, 0.03); padding: 1.5rem !important; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.05); }
    .stTabs [data-baseweb="tab-list"] { gap: 2rem; border-bottom: 1px solid #1d1d1f; }
    .stTabs [data-baseweb="tab"] { color: #86868b; background-color: transparent !important; border: none !important; }
    .stTabs [aria-selected="true"] { color: #0A84FF !important; border-bottom: 2px solid #0A84FF !important; }
    .stButton button { background: #FFFFFF !important; color: #000000 !important; border-radius: 12px !important; padding: 0.75rem 2rem !important; font-weight: 600 !important; width: 100%; transition: all 0.3s ease; }
    .stButton button:hover { transform: scale(1.02); box-shadow: 0 0 25px rgba(255,255,255,0.25); }
    .stSelectbox div[data-baseweb="select"] > div { background-color: #1c1c1e !important; border-radius: 15px !important; border: 1px solid #2c2c2e !important; color: white !important; text-align: center; height: 55px; font-size: 1.2rem; display: flex; align-items: center; justify-content: center; }
    @keyframes ticker-scroll { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
    .ticker-wrap { width: 100%; overflow: hidden; background: rgba(10, 132, 255, 0.05); padding: 12px 0; margin-bottom: 2rem; border-radius: 100px; border: 1px solid rgba(10, 132, 255, 0.1); }
    .ticker-content { display: flex; width: fit-content; animation: ticker-scroll 60s linear infinite; }
    .ticker-item { flex-shrink: 0; padding: 0 3rem; font-size: 0.9rem; font-weight: 500; color: #86868b; }
    .ticker-item b { color: #FFFFFF; margin-right: 8px; }
    .ticker-item.up { color: #28a745; }
    .ticker-item.down { color: #dc3545; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h3 style='font-size: 0.85rem; color: #86868b; text-transform: uppercase; letter-spacing: 0.1em;'>Global Benchmarks</h3>", unsafe_allow_html=True)
    for idx, name in {"^NSEI": "NIFTY 50", "^GSPC": "S&P 500", "BTC-USD": "BTC"}.items():
        try:
            t = yf.Ticker(idx).fast_info
            st.metric(name, f"{t.last_price:,.2f}", f"{t.year_to_date_return*100:+.2f}% YTD")
        except: pass

# --- HERO ---
st.markdown("<h1 style='text-align: center; font-size: 4rem; font-weight: 800; letter-spacing: -0.06em; margin-top: 0;'>StockVision AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #86868b; font-size: 1.2rem; margin-bottom: 1rem;'>Intelligence-First Trading Terminal</p>", unsafe_allow_html=True)

# --- INFINITE TICKER ---
t_us = get_trending_movers("US")
t_in = get_trending_movers("IN")
all_t = (t_us if t_us else []) + (t_in if t_in else [])
if all_t:
    ticker_items = "".join([f'<div class="ticker-item"><b>{s["symbol"]}</b> <span class="{"up" if s["change"] > 0 else "down"}">{s["change"]:+.2f}%</span></div>' for s in (all_t + all_t)])
    st.markdown(f'<div class="ticker-wrap"><div class="ticker-content">{ticker_items}</div></div>', unsafe_allow_html=True)

# --- COMMAND CENTER ---
_, search_col, _ = st.columns([1, 2, 1])
with search_col:
    t_list = get_master_tickers()
    selected = st.selectbox("Ticker Search", options=t_list, index=t_list.index(st.session_state.selected_ticker) if st.session_state.selected_ticker in t_list else 0, label_visibility="collapsed", key="v11_search")
    if selected != st.session_state.selected_ticker:
        st.session_state.selected_ticker = selected
        st.session_state.run_analysis = False
        st.session_state.analysis_results = None
        st.rerun()
    
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    _, c_btn_2, _ = st.columns([1, 2, 1])
    with c_btn_2:
        if st.button("Generate Intelligence Report", key="gen_btn_v11"):
            st.session_state.run_analysis = True
            st.rerun()

# --- DATA DISPLAY ---
ticker = st.session_state.selected_ticker
metadata = get_institutional_metadata(ticker)
live = fetch_live_quote(ticker)

st.markdown(f"<h2 style='text-align: center; color: #FFFFFF; font-weight: 400; font-size: 2.5rem; margin-top: 1rem;'>{metadata['name']}</h2>", unsafe_allow_html=True)

c_sym = get_currency_symbol(metadata['currency'])
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("LTP", f"{c_sym}{live['price']:,.2f}", f"{live['change']:+.2f}%")

if st.session_state.run_analysis and st.session_state.analysis_results is None:
    with st.spinner("Synthesizing Intelligence..."):
        try:
            response = requests.get(f"http://127.0.0.1:8000/predict/{ticker}", timeout=120)
            if response.status_code == 200: st.session_state.analysis_results = response.json()
        except: st.error("Intelligence engine offline.")

res_data = st.session_state.analysis_results
if res_data:
    intel = res_data.get("intelligence", {})
    m2.metric("FORECAST", f"{intel.get('expected_price_change_pct', 0):+.2f}%")
    m3.metric("SIGNAL", intel.get("signal", "N/A"))
    m4.metric("CONFIDENCE", f"{intel.get('confidence', 0)}%")
    m5.metric("RISK", intel.get("risk_level", "N/A"))
else:
    m2.metric("FORECAST", "---"); m3.metric("SIGNAL", "STANDBY"); m4.metric("CONFIDENCE", "0%"); m5.metric("RISK", "PENDING")

st.divider()

# --- MODERN OUT-OF-THE-BOX DYNAMIC CHART FRAGMENT ---
@st.fragment
def render_performance_workspace(ticker, c_sym, metadata):
    chart_map = {"1D": "1d", "5D": "5d", "1M": "1mo", "3M": "3mo", "6M": "6mo", "1Y": "1y", "3Y": "3y", "5Y": "5y", "MAX": "max"}
    
    # 1. Timeline UI
    tr_c, _ = st.columns([1, 4])
    with tr_c:
        sel_range = st.selectbox("Timeline", options=list(chart_map.keys()), index=5, key="fragment_range_selector")
    
    # 2. Dynamic Fetch (Fast & Direct)
    intv = "5m" if sel_range == "1D" else "30m" if sel_range == "5D" else "1d"
    hist = fetch_terminal_chart(ticker, chart_map[sel_range], intv)
    
    if not hist.empty:
        df_p = hist.reset_index()
        x_ax = 'Datetime' if 'Datetime' in df_p.columns else 'Date'
        y_min, y_max = df_p['Close'].min() * 0.999, df_p['Close'].max() * 1.001
        chart = alt.Chart(df_p).mark_area(
            line={'color':'#0A84FF', 'strokeWidth':3},
            color=alt.Gradient(gradient='linear', stops=[alt.GradientStop(color='#0A84FF', offset=0), alt.GradientStop(color='transparent', offset=1)], x1=1, x2=1, y1=1, y2=0),
            interpolate='monotone'
        ).encode(
            x=alt.X(f'{x_ax}:T', title=None, axis=alt.Axis(grid=True, gridColor='#1d1d1f', labelColor='#86868b')),
            y=alt.Y('Close:Q', title='Price', scale=alt.Scale(zero=False, domain=[y_min, y_max]), axis=alt.Axis(grid=True, gridColor='#1d1d1f', labelColor='#86868b')),
            tooltip=[alt.Tooltip(f'{x_ax}:T', title='Time'), alt.Tooltip('Close:Q', title='Price')]
        ).properties(height=450).configure_view(stroke=None)
        st.altair_chart(chart, use_container_width=True)
    else:
        st.error("Live price stream temporarily disconnected.")

    # 3. Enhanced Quick Snap (More Data)
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown("### Business Health Architecture")
    info = metadata["info"]
    
    f1, f2, f3, f4 = st.columns(4)
    f1.metric("Market Cap", f"{c_sym}{format_large_number(info.get('marketCap'))}")
    f2.metric("ROE", f"{info.get('returnOnEquity', 0)*100:.2f}%")
    f3.metric("P/E Ratio", f"{info.get('forwardPE', 'N/A')}")
    f4.metric("Div. Yield", f"{info.get('dividendYield', 0)*100:.2f}%")
    
    f5, f6, f7, f8 = st.columns(4)
    f5.metric("Price to Book", f"{info.get('priceToBook', 'N/A')}")
    f6.metric("Debt to Equity", f"{info.get('debtToEquity', 'N/A')}")
    f7.metric("Quick Ratio", f"{info.get('quickRatio', 'N/A')}")
    f8.metric("Operating Margin", f"{info.get('operatingMargins', 0)*100:.2f}%")

# --- MAIN WORKSPACE GRID ---
col_left, col_right = st.columns([2.4, 1], gap="large")

with col_left:
    t_perf, t_ai, t_ctx, t_inst, t_funds = st.tabs(["PERFORMANCE", "AI REASONING", "MARKET CONTEXT", "SHAREHOLDING", "FINANCIALS"])
    
    with t_perf:
        # Call the dynamic fragment - this fixes the double click bug!
        render_performance_workspace(ticker, c_sym, metadata)

    with t_ai:
        if res_data:
            st.markdown("### 🤖 Intelligence Synthesis")
            debate = res_data.get("debate", {})
            col_bull, col_bear = st.columns(2)
            with col_bull: st.markdown("<h5 style='color: #28a745;'>🐂 THE BULL CASE</h5>", unsafe_allow_html=True); st.write(debate.get("bull_case"))
            with col_bear: st.markdown("<h5 style='color: #dc3545;'>🐻 THE BEAR CASE</h5>", unsafe_allow_html=True); st.write(debate.get("bear_case"))
            st.divider(); st.info(debate.get("verdict"))
        else: st.info("Run Intelligence Report for AI Reasoning.")

    with t_ctx:
        if res_data:
            st.markdown("### Market Context Intelligence")
            st.markdown(f"""<div style="background: rgba(255,255,255,0.03); padding: 1.5rem; border-radius: 15px; border: 1px solid rgba(255,255,255,0.05);">{res_data.get('executive_tone', 'Analyzing...')}</div>""", unsafe_allow_html=True)
            st.divider()
            n1, n2 = st.columns(2, gap="large")
            with n1:
                for n in res_data.get("recent_news", []): st.markdown(f"**[{n['title']}]({n['link']})**")
            with n2:
                social = res_data.get("social", {})
                st.metric("RETAIL HYPE", f"{social.get('hype_score', 0)}/100")
                for p in social.get("top_posts", []): st.markdown(f"r/{p['subreddit']} | **[{p['title']}]({p['url']})**")
        else: st.info("Run report for context.")

    with t_inst:
        st.markdown("### 🐋 Global Shareholding Pattern")
        holders = get_shareholders(ticker)
        if holders is not None: st.dataframe(holders, use_container_width=True)
        else: st.info("Shareholding data limited for this ticker.")

    with t_funds:
        st.markdown(f"### 📊 Full Financial Dataset: {metadata['name']}")
        info = metadata["info"]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"Market Cap: {c_sym}{format_large_number(info.get('marketCap'))}")
            st.write(f"Forward P/E: {info.get('forwardPE', 'N/A')}")
            st.write(f"Trailing P/E: {info.get('trailingPE', 'N/A')}")
        with col2:
            st.write(f"ROE: {info.get('returnOnEquity', 0)*100:.2f}%")
            st.write(f"Profit Margin: {info.get('profitMargins', 0)*100:.2f}%")
            st.write(f"Operating Margin: {info.get('operatingMargins', 0)*100:.2f}%")
        with col3:
            st.write(f"Rev. Growth: {info.get('revenueGrowth', 0)*100:.2f}%")
            st.write(f"Total Cash: {c_sym}{format_large_number(info.get('totalCash'))}")
            st.write(f"Total Debt: {c_sym}{format_large_number(info.get('totalDebt'))}")
        st.divider(); st.write(metadata["summary"])

with col_right:
    st.markdown("<h3 style='font-size: 1rem; color: #86868b; text-transform: uppercase;'>Intelligence Strategist</h3>", unsafe_allow_html=True)
    if not st.session_state.show_chat:
        st.markdown("<div style='background: rgba(255,255,255,0.02); padding: 3rem 1.5rem; border-radius: 30px; border: 1px solid rgba(10, 132, 255, 0.2); text-align: center;'>🧠<br><br><b>Strategic Core Online</b><br><span style='font-size:0.8rem; color:#86868b;'>Personalized Advice & Pattern Recognition</span></div>", unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        _, c_btn_r, _ = st.columns([1, 2.5, 1])
        with c_btn_r:
            if st.button("Initialize Advisor", key="init_v11"):
                st.session_state.show_chat = True
                st.rerun()
    else:
        chat_box = st.container(height=650)
        with chat_box:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]): st.write(msg["content"])
        if prompt := st.chat_input("Query advisor..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            ctx = {"ticker": ticker, "fundamentals": metadata["info"], "ltp": live['price'], "signal": res_data.get("intelligence", {}).get("signal") if res_data else None}
            resp = get_analyst_response(prompt, st.session_state.chat_history[:-1], ctx)
            st.session_state.chat_history.append({"role": "assistant", "content": resp})
            st.rerun()

st.markdown("<div style='text-align: center; color: #424245; font-size: 0.75rem; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 4rem; margin-top: 5rem;'>STOCKVISION AI • PREMIUM TERMINAL v5.2</div>", unsafe_allow_html=True)
