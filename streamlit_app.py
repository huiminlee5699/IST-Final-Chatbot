import streamlit as st
from pathlib import Path
from openai import OpenAI
import time

# 0) UN‑PIN st.chat_input so it lives where you call it:
st.markdown(
    """
    <style>
      [data-testid="stChatFloatingInputContainer"] {
        position: static !important;
        bottom: auto !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# 1) Your header
st.title("💬 Chatbot")
st.write(
    "Welcome to Chatbot, a new OpenAI-powered chatbot! "
    "Feel free to ask me anything!"
)

# 2) OpenAI client setup
openai_api_key = st.secrets["openai_api_key"]
client = OpenAI(api_key=openai_api_key)

# 3) Message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4) Render past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5) The in‑flow chat input
if prompt := st.chat_input("What would you like to know today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        stream=True,
    )
    with st.chat_message("assistant"):
        container = st.empty()
        text = ""
        for chunk in stream:
            if c := chunk.choices[0].delta.content:
                text += c
                container.markdown(text)
    st.session_state.messages.append({"role": "assistant", "content": text})

# 6) Load & render your standalone footer.html **below** the input
footer_path = Path(__file__).parent / "footer.html"
if footer_path.exists():
    st.markdown(footer_path.read_text(), unsafe_allow_html=True)
else:
    st.error(f"Could not find footer.html at {footer_path}")
