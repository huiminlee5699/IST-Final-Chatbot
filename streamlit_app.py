import streamlit as st
from openai import OpenAI

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

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
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

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
with st.chat_message("assistant"):
    response_container = st.empty()  # placeholder for streaming text
    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            full_response += chunk.choices[0].delta.content
            response_container.markdown(full_response)

    # After streaming, check word count and append message if needed
    word_count = len(full_response.split())
    if word_count > 100:
        full_response += (
            "\n\nWant to get inside my brain? Click here to find out more: "
            "https://ai.meta.com/tools/system-cards/ai-systems-that-generate-text/"
        )
        response_container.markdown(full_response)

st.session_state.messages.append({"role": "assistant", "content": full_response})
