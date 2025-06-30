import streamlit as st
import requests   #Ye python ka built in module ha jo ksi bhi Api se data lene aur bhejne k kaam aata ha.Yani hum Groq Api se bat is k zariye krte han.
import os          #Ye bhi aik api module ha jo humain system ki cheezain access krne deta ha jaise (Api keys wagaira).
from langchain_groq import ChatGroq   #langchain_groq ek integration library hai jo LangChain ko Groq ke LLMs ke sath connect karti hai.Groq ek “super fast AI engine” hai jo AI ko rocket speed pe chalata hai.ChatGroq = LangChain ka aik bridge class jo Groq ke fast models ko use karta hai chat ke liye.
from dotenv import load_dotenv  #ye .env se secret files load krta ha.
load_dotenv()      #ab .env files se sb keys system ke andr load ho jae gi.

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]  #.getenv ye system se Api key uthata ha. GROQ_API_KEY aik variabe ha jis main tumhari key store ho gayi han.

GROQ_MODEL = "llama3-8b-8192"  #is ka kam ha swalon k jwab dena,chat krna, Text smjhana aur likhna,chatbots,summarizer,translators wagaira main use hota ha.
                               #llama3 ye third version ha llama model ka aur 8b ka mtlb ha 8billion parameters aur 8192 ka mtlb ha k ye 8192 tokens tak ka text smjh skta ha.

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
if "messages" not in st.session_state:  #Yahan hum keh rahe han k agar pehle se koi message nahi hai to ek default system message daal do jo AI ko batata hai ke vo friendly medical assistant ban ke behave kare.
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a friendly and professional medical assistant. Help the user book appointments by asking about symptoms, preferred date/time, and doctor preferences. Keep it short and clear."
        }
    ]

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})   #jb user message bhejta ha to hum use list main add kr lete han.

    # Groq API call
    response = requests.post(   ##post request bhejna 
        "https://api.groq.com/openai/v1/chat/completions",  #ye Groq ka api address ha jahan tumhara message ja rha ha.
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",  #Authorization: tum Api key bhej rhe ho ,jisse Groq tumhe pehchane.(Tumara account)
            "Content-Type": "application/json"   #content-Type: ye tum  Bata rahe ho ke tum JSON format mein data bhej rahe ho.
        },             
        json={        # Ye teen cheezein tum bhej rahe ho Groq ko:
            "model": GROQ_MODEL,
            "messages": st.session_state.messages,  #ye pura chat ka history bhej rahe ho (user + assistant ke messages).
            "temperature": 0.6  #ye creativity level hota ha na ziada boring na ziada creative balance mein.
        }
    )

    if response.status_code == 200:   #200 ka matlab hota hai:  OK / Success Yani request sahi chal gayi, data mil gaya.
        bot_reply = response.json()["choices"][0]["message"]["content"]   #Ye line us JSON data se reply nikaalti hai:response.json() → pura JSON object, ["choices"][0] → pehla reply, ["message"]["content"] → uska actual text (chatbot ka jawab).  
    else:
        bot_reply = "Sorry, there was an error connecting to Groq API."

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})  ##bot ka rply chat history main dalna.

# Show chat messages
for msg in st.session_state.messages[1:]:  # Ye for loop har message ko ek ek karke dikhata hai 
    if msg["role"] == "user":   #agr user message bheje to
        with st.chat_message("user", avatar="🧑‍💻"):   #chat box bnain ge hum
            st.markdown(
                f"<div style='background-color:	#E6E6FA; color:black; padding:10px; border-radius:10px;'>{msg['content']}</div>",
                unsafe_allow_html=True
            )
    elif msg["role"] == "assistant":    # Agar reply bot ka hai to:
        with st.chat_message("assistant", avatar="💬"):   #to chat box bnainge hum
            st.markdown(
                f"<div style='background-color:#444654; color:white; padding:10px; border-radius:10px;'>{msg['content']}</div>",
                unsafe_allow_html=True  #Streamlit ko allow karna ke wo HTML code render kare (dikhaye), jo normally wo security ki wajah se block karta hai.
            )




