import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
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

if "conversation" not in st.session_state or "llm_model" not in st.session_state:
    st.session_state.llm_model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    st.session_state.temperature = float(os.getenv("LLM_TEMPERATURE", 0.7))
    st.session_state.conversation = None

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    
    # Model selection
    model = st.selectbox(
        "Select Model",
        ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview", "gemini-2.0-flash"],
        index=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview", "gemini-2.0-flash"].index(st.session_state.llm_model) if st.session_state.llm_model in ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview", "gemini-2.0-flash"] else 0
    )
    st.session_state.llm_model = model
    
    # Temperature slider
    temperature = st.slider("Temperature", 0.0, 1.0, st.session_state.temperature, 0.1)
    st.session_state.temperature = temperature
    
    # API key input for Gemini
    if "gemini_api_key" not in st.session_state:
        st.session_state.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY", "")

    if model.startswith("gemini"):
        gemini_api_key = st.text_input("Gemini API Key", value=st.session_state.gemini_api_key, type="password")
        st.session_state.gemini_api_key = gemini_api_key
    else:
        api_key = st.text_input("OpenAI API Key", value=st.session_state.openai_api_key, type="password")
        st.session_state.openai_api_key = api_key

    # Show status for both keys
    st.markdown("---")
    st.subheader("API Key Status")
    def mask_key(key):
        if not key:
            return "[not set]"
        if len(key) <= 8:
            return key
        return key[:4] + "..." + key[-4:]
    st.write(f"**Selected Model:** `{st.session_state.llm_model}`")
    st.write(f"**OpenAI Key:** `{mask_key(st.session_state.openai_api_key)}`")
    st.write(f"**Gemini Key:** `{mask_key(st.session_state.gemini_api_key)}`")
    if st.session_state.openai_api_key:
        st.success("✅ OpenAI API key configured")
    else:
        st.warning("⚠️ OpenAI API key not found!")
    if st.session_state.gemini_api_key:
        st.success("✅ Gemini API key configured")
    else:
        st.warning("⚠️ Gemini API key not found!")

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        if st.session_state.conversation:
            st.session_state.conversation.memory.clear()
        st.rerun()

# Initialize the conversation chain if needed
if st.session_state.conversation is None or st.session_state.llm_model != st.session_state.get("active_model") or st.session_state.temperature != st.session_state.get("active_temperature"):
    try:
        if st.session_state.llm_model.startswith("gemini"):
            llm = ChatGoogleGenerativeAI(
                model=st.session_state.llm_model,
                temperature=st.session_state.temperature,
                google_api_key=st.session_state.get("gemini_api_key", "")
            )
        else:
            llm = ChatOpenAI(
                model=st.session_state.llm_model,
                temperature=st.session_state.temperature,
                openai_api_key=st.session_state.get("openai_api_key", "")
            )
        memory = ConversationBufferMemory()
        st.session_state.conversation = ConversationChain(
            llm=llm,
            memory=memory,
            verbose=False
        )
        st.session_state.active_model = st.session_state.llm_model
        st.session_state.active_temperature = st.session_state.temperature
    except Exception as e:
        st.error(f"Error initializing chatbot: {e}")
        st.session_state.conversation = None

# Header
st.title("🤖 LangChain Chatbot")
st.markdown("A simple chatbot built with LangChain, OpenAI, and Gemini")

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
        debug_info = f"**[DEBUG] Model:** `{st.session_state.llm_model}`  "
        if st.session_state.llm_model.startswith("gemini"):
            debug_info += f"**Gemini Key:** `{mask_key(st.session_state.gemini_api_key)}`"
        else:
            debug_info += f"**OpenAI Key:** `{mask_key(st.session_state.openai_api_key)}`"
        st.info(debug_info)
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
        Built with ❤️ using LangChain, OpenAI, Gemini, and Streamlit
    </div>
    """,
    unsafe_allow_html=True
) 