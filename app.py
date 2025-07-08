import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="LangChain Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation" not in st.session_state:
    # Initialize the conversation chain
    try:
        llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        memory = ConversationBufferMemory()
        st.session_state.conversation = ConversationChain(
            llm=llm,
            memory=memory,
            verbose=False
        )
    except Exception as e:
        st.error(f"Error initializing chatbot: {e}")
        st.session_state.conversation = None

# Header
st.title("🤖 LangChain Chatbot")
st.markdown("A simple chatbot built with LangChain and OpenAI")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    
    # Check if API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        st.error("⚠️ OpenAI API key not found!")
        st.info("Please set your OpenAI API key in the .env file")
        st.code("OPENAI_API_KEY=your_actual_api_key_here")
    else:
        st.success("✅ OpenAI API key configured")
    
    # Model selection
    model = st.selectbox(
        "Select Model",
        ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"],
        index=0
    )
    
    # Temperature slider
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        if st.session_state.conversation:
            st.session_state.conversation.memory.clear()
        st.rerun()

# Main chat interface
st.markdown("---")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if st.session_state.conversation:
            try:
                with st.spinner("Thinking..."):
                    response = st.session_state.conversation.predict(input=prompt)
                
                message_placeholder.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                error_message = f"Error: {str(e)}"
                message_placeholder.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
        else:
            error_message = "Chatbot not initialized. Please check your API key configuration."
            message_placeholder.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        Built with ❤️ using LangChain and Streamlit
    </div>
    """,
    unsafe_allow_html=True
) 