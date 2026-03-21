import os
from groq import Groq
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Groq Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Gemini Configuration
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def ask_agent(question):
    # Try Gemini First
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model.generate_content(question).text
    except:
        # Fallback to Groq
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": question}],
                model="llama-3.3-70b-versatile",
            )
            return response.choices[0].message.content
        except:
            return "Agent offline."

def generate_explanation(ticker: str, analysis_data: dict) -> str:
    prompt = f"Act as an expert financial analyst. Analyze the following data for {ticker} and provide a concise, professional explanation for the investment signal. Data: {analysis_data}. Provide a 2-3 paragraph explanation."
    # Try Gemini First
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model.generate_content(prompt).text
    except:
        # Fallback to Groq
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
            return response.choices[0].message.content
        except:
            return "Explanation engine offline."

def get_analyst_response(user_query: str, chat_history: list, context_data: dict = None) -> str:
    system_instruction = "You are the StockVision AI Senior Investment Strategist. Provide precise, data-driven financial advice."
    current_content = f"CONTEXT: {context_data}\n\nUSER: {user_query}" if context_data else user_query

    # Try Gemini First
    try:
        model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=system_instruction)
        gemini_history = []
        for msg in chat_history[-10:]:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [msg["content"]]})
        chat = model.start_chat(history=gemini_history)
        return chat.send_message(current_content).text
    except:
        try:
            # Fallback to Groq
            messages = [{"role": "system", "content": system_instruction}]
            for msg in chat_history[-10:]:
                messages.append({"role": msg["role"], "content": msg["content"]})
            messages.append({"role": "user", "content": current_content})
            resp = client.chat.completions.create(messages=messages, model="llama-3.3-70b-versatile")
            return resp.choices[0].message.content + "\n\n*(Note: Powered by Groq fallback)*"
        except:
            return "Intelligence core completely offline."

def conduct_research_debate(ticker: str, analysis_data: dict) -> dict:
    context = f"Ticker: {ticker}, Data: {analysis_data}"
    prompts = {
        "bull": f"Provide the strongest BULL case for {ticker} based on {context}.",
        "bear": f"Provide the strongest BEAR case for {ticker} based on {context}.",
        "judge": "Synthesize the bull and bear cases and provide a final verdict with conviction score 1-10."
    }
    # Try Gemini First
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        chat = model.start_chat()
        return {
            "bull_case": chat.send_message(prompts["bull"]).text,
            "bear_case": chat.send_message(prompts["bear"]).text,
            "verdict": chat.send_message(prompts["judge"]).text
        }
    except:
        try:
            res = {}
            for k, v in prompts.items():
                r = client.chat.completions.create(messages=[{"role": "user", "content": v}], model="llama-3.3-70b-versatile")
                res[k] = r.choices[0].message.content
            return {"bull_case": res["bull"], "bear_case": res["bear"], "verdict": res["judge"] + "\n\n*(Groq fallback)*"}
        except:
            return {"error": "Debate engine offline."}

def decode_executive_tone(ticker: str, news_items: list) -> str:
    if not news_items: return "No recent executive data."
    prompt = f"Analyze executive tone for {ticker} (Confident, Defensive, or Uncertain) based on headlines: {news_items}"
    # Try Gemini First
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model.generate_content(prompt).text
    except:
        try:
            resp = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
            return resp.choices[0].message.content
        except:
            return "Tone analysis unavailable."
