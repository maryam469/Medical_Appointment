import streamlit as st
import requests
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = "llama3-8b-8192"


st.set_page_config(page_title="Medical Chatbot", layout="wide")

with st.sidebar:
    st.title("Medical Bot")
    st.markdown("""
    Use this chatbot to:
    - Book doctor appointments  
    - Ask health questions  
    - Get intelligent responses  
    """)

# Title
st.markdown("<h1 style='text-align:center;'>Medical Appointment Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Talk to your AI assistant for booking and advice.</p><hr>", unsafe_allow_html=True)

# Message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a friendly and professional medical assistant. Help the user book appointments by asking about symptoms, preferred date/time, and doctor preferences. Keep it short and clear."
        }
    ]

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Groq API call
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": GROQ_MODEL,
            "messages": st.session_state.messages,
            "temperature": 0.6
        }
    )

    if response.status_code == 200:
        bot_reply = response.json()["choices"][0]["message"]["content"]
    else:
        bot_reply = "Sorry, there was an error connecting to Groq API."

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# Show chat messages
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(
                f"<div style='background-color:	#E6E6FA; color:black; padding:10px; border-radius:10px;'>{msg['content']}</div>",
                unsafe_allow_html=True
            )
    elif msg["role"] == "assistant":
        with st.chat_message("assistant", avatar="💬"):
            st.markdown(
                f"<div style='background-color:#444654; color:white; padding:10px; border-radius:10px;'>{msg['content']}</div>",
                unsafe_allow_html=True
            )




