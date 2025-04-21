import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
import time

st.set_page_config(
    page_title="💬 CHATBOT AI",
)

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
    background: transparent;
    margin-bottom: 10px;
}
</style>


# Initialize click tracking variable in session state
if 'link_clicked' not in st.session_state:
    st.session_state.link_clicked = False

# Function to handle link click
def link_click():
    st.session_state.link_clicked = True
    external_url = "https://www.figma.com/proto/ZeWFZShKd7Pu8N3Wwj8wri/Transparency-card?page-id=0%3A1&node-id=1-2&p=f&viewport=54%2C476%2C0.2&t=z8tiRCZcXZC9N553-8&scaling=min-zoom&content-scaling=fixed&hide-ui=1"
    js = f"window.open('{external_url}', '_blank')"
    components.html(f"<script>{js}</script>", height=0)

# Replace your footer link with a Streamlit button:
footer_html = """
<footer>
    💡🧠🤓 <strong>Want to learn how I come up with responses?</strong>
    <a href=\"https://www.figma.com/proto/haXTVr4wZaeSC344BqDBpR/Text-Transparency-Card?page-id=0%3A1&node-id=1-33&p=f&viewport=144%2C207%2C0.47&t=Hp8ZCw5Fg7ahsiq1-8&scaling=min-zoom&content-scaling=fixed&hide-ui=1\" target=\"_blank\" style=\"color: #007BFF; text-decoration: none;\">\n
    Read more here →\n
</footer>
"""

st.markdown(footer_html, unsafe_allow_html=True)

if st.button("Read more here →"):
    link_click()

# For testing purposes, you can display if the link was clicked:
st.write(f"Link clicked: {st.session_state.link_clicked}")






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
        model="gpt-4o-mini",
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
