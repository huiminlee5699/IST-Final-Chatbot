import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
import time

st.set_page_config(
    page_title="💬 CHATBOT AI",
)

# CSS for styling
st.markdown("""
<style>
    /* Import fonts */
    @import url("https://fonts.googleapis.com/css2?family=Inria+Sans:ital,wght@0,300;0,400;0,700;1,300;1,400;1,700&display=swap");
    @import url("https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap");
    
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
    
    /* Footer styling */
    .footer-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: transparent;
        padding: 15px;
        text-align: center;
        z-index: 998;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .footer-text {
        margin-bottom: 5px;
        font-size: 0.9rem;
    }
    
    /* Add padding to prevent content being hidden by footer */
    .main .block-container {
        padding-bottom: 80px;
    }
    
    /* Ensure chat input stays above footer */
    .stChatInputContainer {
        z-index: 999;
        position: relative;
        background: transparent;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Show title and description
st.markdown("<h1>💬 CHATBOT AI</h1>", unsafe_allow_html=True)

st.write(
    "Welcome to Chatbot, a new OpenAI-powered chatbot! "
    "Feel free to ask me anything!"
)

# Initialize OpenAI client
openai_api_key = st.secrets["openai_api_key"]
client = OpenAI(api_key=openai_api_key)

# Initialize chat messages in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input field
if prompt := st.chat_input("What would you like to know today?"):
    # Store and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response using OpenAI API
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
        ],
        stream=True,
    )
    
    time.sleep(1)
    
    # Stream the assistant response
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                response_container.markdown(full_response)
        
        # Store final response
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Function to handle "Learn More" click
def open_transparency_card():
    external_url = "https://www.figma.com/proto/ZeWFZShKd7Pu8N3Wwj8wri/Transparency-card?page-id=0%3A1&node-id=1-2&p=f&viewport=54%2C476%2C0.2&t=z8tiRCZcXZC9N553-8&scaling=min-zoom&content-scaling=fixed&hide-ui=1"
    js = f"window.open('{external_url}', '_blank')"
    components.html(f"<script>{js}</script>", height=0)

# Footer with "Learn More" button
st.markdown(
    """
    <div class="footer-container">
        <div class="footer-text">💡🧠🤓 <strong>Want to learn how I come up with responses?</strong></div>
    </div>
    """, 
    unsafe_allow_html=True
)

# Place the button below the footer text
if st.button("Read more here →"):
    open_transparency_card()
