import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
import time

# Set page config first
st.set_page_config(
    page_title="💬 CHATBOT AI",
)

# Original styling - unchanged
st.markdown("""
<style>
    /* Import fonts */
    @import url("https://fonts.googleapis.com/css2?family=Inria+Sans:ital,wght@0,300;0,400;0,700;1,300;1,400;1,700&display=swap");
    @import url("https://fonts.googleapis.com/css2?family=Inria+Sans:ital,wght@0,300;0,400;0,700;1,300;1,400;1,700&family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap");
    
    /* Title font (Inria Sans) */
    .main h1 {
        font-family: 'Inria Sans', sans-serif !important; 
        color: #3f39e3 !important;
    }
    /* Additional selectors to ensure title styling */
    .st-emotion-cache-10trblm h1, 
    .stMarkdown h1 {
        font-family: 'Inria Sans', sans-serif !important; 
        color: #3f39e3 !important;
    }
    
    /* All other text (Inter) */
    body, p, div, span, li, a, button, input, textarea, .stTextInput label {
        font-family: 'Inter', sans-serif !important;
    } 
</style>
""", unsafe_allow_html=True)

# Show title and description.
st.markdown("<h1 style='font-family: \"Inria Sans\", sans-serif; color: #3f39e3;'>💬 CHATBOT AI</h1>", unsafe_allow_html=True)

st.write(
    "Welcome to Chatbot, a new OpenAI-powered chatbot! "
    "Feel free to ask me anything!"
)

# Add custom CSS for a fixed footer at the bottom of the page
st.markdown("""
<style>
footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: transparent;
    padding: 15px;
    font-size: 0.9rem;
    font-family: sans-serif;
    text-align: center;
    z-index: 998;
}

/* Add padding to the bottom of the page to prevent content from being hidden by the footer */
.main .block-container {
    padding-bottom: 80px;
}

/* Ensure the chat input stays above the footer */
.stChatInputContainer {
    z-index: 999;
    position: relative;
    background: white;
    margin-bottom: 10px;
}
</style>

<footer>
    💡🧠🤓 <strong>Want to learn how I come up with responses?</strong>
    <a href="https://ai.meta.com/tools/system-cards/ai-systems-that-generate-text/" target="_blank" style="color: #007BFF; text-decoration: none;">
        Read more here →
    </a>
</footer>
""", unsafe_allow_html=True)

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


