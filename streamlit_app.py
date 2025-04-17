import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
import time

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "Welcome to Chatbot, a new OpenAI-powered chatbot! "
    "Feel free to ask me anything!"
)

# Use the API key from Streamlit secrets
openai_api_key = st.secrets["openai_api_key"]

# Create an OpenAI client.
client = OpenAI(api_key=openai_api_key)

# Create a session state variable to store the chat messages.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 1) Inject CSS to make the chat_input render in-flow instead of fixed at bottom
components.html(
    """
    <style>
      .stChatFloatingInputContainer {
        position: static !important;
        bottom: auto !important;
      }
    </style>
    """,
    height=0,
    scrolling=False,
)

# 2) Render the chat input in the natural flow of the page
if prompt := st.chat_input("What would you like to know today?"):
    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Stream the assistant response while building it up
    with st.chat_message("assistant"):
        response_container = st.empty()  # placeholder for streaming text
        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                response_container.markdown(full_response)

    # Store the final response in session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# 3) Render your footer below the chat input
footer_html = """
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
"""
st.markdown(footer_html, unsafe_allow_html=True)
