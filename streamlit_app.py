import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
import time

# THIS MUST BE THE VERY FIRST THING IN YOUR SCRIPT
# Create styles to ensure proper spacing for the footer
st.markdown(
    """
    <style>
    /* Add padding to the bottom of the page to make room for footer */
    .main .block-container {
        padding-bottom: 70px !important;
    }
    
    /* Hide default streamlit footer */
    footer {
        visibility: hidden !important;
    }
    
    /* Ensure chat input is properly positioned */
    .stChatInputContainer {
        padding-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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

# THIS MUST BE THE LAST ELEMENT IN YOUR SCRIPT
# Use components.html to create a true fixed footer at the bottom
components.html(
    """
    <div style="
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #f9f9f9;
        padding: 15px;
        text-align: center;
        box-shadow: 0 -4px 8px rgba(0,0,0,0.1);
        z-index: 9999999;
        font-family: sans-serif;
        font-size: 0.9rem;
    ">
        💡🧠🤓 <strong>Want to learn how I come up with responses?</strong>
        <a href="https://ai.meta.com/tools/system-cards/ai-systems-that-generate-text/" 
           target="_blank" style="color: #007BFF; text-decoration: none;">
            Read more here →
        </a>
    </div>
    """,
    height=0,
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

# Add padding to the bottom of the container to account for the fixed footer
st.markdown("<div style='height: 70px;'></div>", unsafe_allow_html=True)

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

# Add another padding element at the end to ensure enough space at the bottom
st.markdown("<div style='height: 70px;'></div>", unsafe_allow_html=True)
