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

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message.
if prompt := st.chat_input("What would you like to know today?"):
    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
        ],
        stream=True,
    )
    
    time.sleep(1)
    
    # Stream the assistant response while building it up
    with st.chat_message("assistant"):
        response_container = st.empty()  # placeholder for streaming text
        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                response_container.markdown(full_response)
        
        # Final display of the complete response
        response_container.markdown(full_response)
        
        # Store the final response in session state
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Add custom CSS to position a fixed element above the chat input
st.markdown("""
<style>
.stChatInputContainer {
    padding-top: 60px !important;
}
</style>
""", unsafe_allow_html=True)

# Use components.html to create a fixed message above the chat input
components.html("""
<div style="
    position: fixed;
    bottom: 75px;
    left: 0;
    right: 0;
    background: #f9f9f9;
    padding: 15px;
    box-shadow: 0 -4px 8px rgba(0, 0, 0, 0.1);
    font-size: 0.9rem;
    font-family: sans-serif;
    text-align: center;
    z-index: 9999;
">
    💡🧠🤓 <strong>Want to learn how I come up with responses?</strong>
    <a href="https://ai.meta.com/tools/system-cards/ai-systems-that-generate-text/" target="_blank" style="color: #007BFF; text-decoration: none;">
        Read more here →
    </a>
</div>
""", height=100)
