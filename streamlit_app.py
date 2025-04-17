import streamlit as st
from openai import OpenAI
import time

# 0) CSS override injected into the main page,
#    so the chat_input container becomes static.
st.markdown(
    """
    <style>
      /* make the chat_input render inline instead of fixed */
      .stChatFloatingInputContainer {
        position: static !important;
        bottom: auto !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# 1) Show title and description.
st.title("💬 Chatbot")
st.write(
    "Welcome to Chatbot, a new OpenAI-powered chatbot! "
    "Feel free to ask me anything!"
)

# 2) API key and client setup.
openai_api_key = st.secrets["openai_api_key"]
client = OpenAI(api_key=openai_api_key)

# 3) Persisted chat history.
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4) Render past messages.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5) Now the chat_input appears right here, in‑flow.
if prompt := st.chat_input("What would you like to know today?"):
    # record & display user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # stream assistant reply
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        stream=True,
    )
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                response_container.markdown(full_response)

    # save assistant
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# 6) Finally — your footer, *below* the input.
st.markdown(
    """
    <div style="
        width: 100%;
        background: #f9f9f9;
        padding: 12px 0;
        text-align: center;
        border-top: 1px solid #eaeaea;
        font-size: 0.9rem;
        font-family: sans-serif;
    ">
      💡🧠🤓 <strong>Want to learn how I come up with responses?</strong>
      <a href="https://ai.meta.com/tools/system-cards/ai-systems-that-generate-text/"
         style="color:#007BFF; text-decoration:none; margin-left:6px;"
         target="_blank">
        Read more here →
      </a>
    </div>
    """,
    unsafe_allow_html=True,
)
