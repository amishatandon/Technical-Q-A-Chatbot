import streamlit as st
import os
from dotenv import load_dotenv

# Import the necessary components from Langchain for Gemini
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables (like your API key) from a .env file
load_dotenv()

# Streamlit UI configuration
st.set_page_config(page_title="Technical Q&A Chatbot", layout="wide")
st.title("Technical Q&A with Gemini")
st.markdown("Ask a question about code, algorithms, or technical concepts.")

# Check if the GOOGLE_API_KEY is set
if "GOOGLE_API_KEY" not in os.environ:
    st.error("Please set the GOOGLE_API_KEY environment variable.")
else:
    # Initialize the ChatGoogleGenerativeAI model
    # Note: Using "gemini-1.5-flash-latest" which is suitable for text-based chat.
    chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.5)

    # Initialize session state for conversational history
    if 'flowmessages' not in st.session_state:
        st.session_state['flowmessages'] = [
            # The system message is now tailored for technical and coding topics.
            SystemMessage(content="You are a specialized technical assistant. Your purpose is to provide concise, accurate, and helpful information related to programming, software development, algorithms, and technical concepts. Always provide code examples when relevant.")
        ]

    # Function to get the model response
    def get_chatmodel_response(question):
        """
        Sends the user's question to the Gemini model and updates the chat history.
        """
        st.session_state['flowmessages'].append(HumanMessage(content=question))
        # The 'chat' object is callable with a list of messages.
        answer = chat(st.session_state['flowmessages'])
        st.session_state['flowmessages'].append(AIMessage(content=answer.content))
        return answer.content

    # User input text box
    input_text = st.text_input("Input:", key="input")

    # Ask button
    submit = st.button("Ask the question")

    # If the ask button is clicked, get the response and display it
    if submit and input_text:
        with st.spinner("Thinking..."):
            response = get_chatmodel_response(input_text)
        
        st.subheader("The Response Is:")
        st.write(response)
