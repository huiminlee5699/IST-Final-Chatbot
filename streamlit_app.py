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

# Display the existing chat messages via st.chat_message.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
bottom_note = st.empty()
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

    time.sleep(1)
    
    # Stream the assistant response while building it up
    with st.chat_message("assistant"):
        response_container = st.empty()  # placeholder for streaming text
        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                response_container.markdown(full_response)

        # Count previous assistant messages
        assistant_messages = [
            msg for msg in st.session_state.messages if msg["role"] == "assistant"
        ]

        response_container.markdown(full_response)

    # Store the final response in session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})

footer_path = Path(__file__).parent / "footer.html"
if footer_path.exists():
    footer_html = footer_path.read_text()
    # You can use st.markdown or components.html; 
    # here we use components.html to avoid any trimming.
    components.html(footer_html, height=80, scrolling=False)
else:
    st.error(f"Could not find footer.html at {footer_path}")
