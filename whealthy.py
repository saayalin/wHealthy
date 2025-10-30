import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# -------------------- LOAD ENV --------------------
load_dotenv()

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Whealthy 🥗", page_icon="🥗", layout="centered")

# -------------------- CUSTOM CSS --------------------
custom_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f2f7f3;
    background-image: linear-gradient(180deg, #f4f9f5 0%, #e5f2e7 100%);
    color: #2e5339;
}
.main-block {
    background-color: rgba(255, 255, 255, 0.92);
    border-radius: 18px;
    box-shadow: 0 8px 30px rgba(82, 104, 89, 0.08);
    padding: 25px;
    margin-top: 25px;
    backdrop-filter: blur(4px);
}
.chat-message {
    border-radius: 18px;
    padding: 14px 18px;
    margin: 8px 0;
    max-width: 85%;
    line-height: 1.5;
    word-wrap: break-word;
    font-size: 16px;
}
.chat-message.user {
    background-color: #e3f2e1;
    color: #2e5339;
    align-self: flex-end;
    border: 1px solid #b5d1b1;
}
.chat-message.assistant {
    background-color: #ffffff;
    border: 1px solid #c9dcc5;
    color: #2e5339;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}
h1 {
    color: #2e5339 !important;
    font-family: 'Poppins', sans-serif !important;
    text-align: center;
}
p { color: #496c50; }
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown("""
    <div class="main-block">
        <h1>🥗 Whealthy — Your AI Salad Assistant 🌿</h1>
        <p style='text-align:center; font-size:17px;'>
        Personalized salad and nutrition suggestions made with care 💚
        </p>
    </div>
""", unsafe_allow_html=True)

# -------------------- API KEY --------------------
if "GROQ_API_KEY" not in st.session_state:
    st.session_state.GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

if not st.session_state.GROQ_API_KEY:
    st.markdown("### 🔑 Enter your Groq API Key to start chatting")
    api_key_input = st.text_input("Groq API Key", type="password", placeholder="gsk_xxxxxxxxxxxxxxxxxxxxxx")
    if api_key_input:
        st.session_state.GROQ_API_KEY = api_key_input
    else:
        st.warning("⚠️ Please enter your Groq API key above to start chatting.")
        st.stop()

# -------------------- CHAT HISTORY --------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hey there! 🥬 I’m Whealthy, your AI nutrition buddy. What kind of meal are you craving today?"}
    ]

for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "assistant"
    st.markdown(f"<div class='chat-message {role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

# -------------------- QUERY FUNCTION --------------------
def query_llm(prompt, api_key):
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are Whealthy 🥗, a friendly AI nutrition coach that suggests healthy, delicious salads and meals with macros and emojis."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"⚠️ API Error: {e}"

# -------------------- CHAT INPUT --------------------
if user_input := st.chat_input("Ask me about your meal plan..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f"<div class='chat-message user'>{user_input}</div>", unsafe_allow_html=True)

    conversation = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    prompt = f"""
    You are Whealthy 🥗, a warm and encouraging AI nutrition assistant.
    Suggest creative, healthy meal or salad ideas based on the user's request.
    Always include:
    - Name of the dish 🥗
    - Ingredients 🧺
    - Approximate macros (calories, protein, fat, carbs)
    - Short motivating message 🌱
    
    Conversation so far:
    {conversation}
    """

    with st.spinner("Whealthy is mixing your perfect salad... 🥗"):
        response = query_llm(prompt, st.session_state.GROQ_API_KEY)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.markdown(f"<div class='chat-message assistant'>{response}</div>", unsafe_allow_html=True)
