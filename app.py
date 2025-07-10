import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_ollama import ChatOllama

# Load environment variables
load_dotenv()

# Helper function to mask API keys
def mask_key(key):
    if not key:
        return "[not set]"
    if len(key) <= 8:
        return key
    return key[:4] + "..." + key[-4:]

# List of all available providers
ALL_PROVIDERS = [
    "OpenAI",
    "Google Gemini",
    "Anthropic Claude",
    "Google Vertex AI",
    "Ollama (Llama3)",
]

# Set page title
st.set_page_config(
    page_title="Multi Model Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for chat history and API keys
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation" not in st.session_state or "llm_model" not in st.session_state:
    st.session_state.llm_model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    st.session_state.temperature = float(os.getenv("LLM_TEMPERATURE", 0.7))
    st.session_state.conversation = None

# Initialize API keys from environment variables
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY", "")
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
if "anthropic_api_key" not in st.session_state:
    st.session_state.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
if "claude_model" not in st.session_state:
    st.session_state.claude_model = os.getenv("CLAUDE_MODEL", "claude-3-haiku-20240307")
if "vertexai_project" not in st.session_state:
    st.session_state.vertexai_project = os.getenv("VERTEXAI_PROJECT_ID", "")
if "vertexai_region" not in st.session_state:
    st.session_state.vertexai_region = os.getenv("VERTEXAI_REGION", "us-central1")
if "vertexai_model" not in st.session_state:
    st.session_state.vertexai_model = os.getenv("VERTEXAI_MODEL", "chat-bison")
if "ollama_model" not in st.session_state:
    st.session_state.ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
if "ollama_temperature" not in st.session_state:
    st.session_state.ollama_temperature = float(os.getenv("OLLAMA_TEMPERATURE", 0.7))
# GOOGLE_APPLICATION_CREDENTIALS check
if "google_application_credentials" not in st.session_state:
    st.session_state.google_application_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
if "gac_set" not in st.session_state:
    st.session_state.gac_set = bool(st.session_state.google_application_credentials)
if "gac_exists" not in st.session_state:
    st.session_state.gac_exists = os.path.isfile(st.session_state.google_application_credentials) if st.session_state.gac_set else False


# Sidebar for API keys and model selection
with st.sidebar:
    st.title("🔑 API & Model Configuration")

    # Add a high-level toggle for single vs multi-model view
    view_mode = st.sidebar.radio(
        "Chat Mode",
        ["Single Model", "Multi-Model"],
        index=0,
    )

    # Model selection (multi-select)
    selected_providers = st.multiselect(
        "Select Model Providers",
        ALL_PROVIDERS,
        default=[ALL_PROVIDERS[0]],
    )
    if not selected_providers:
        st.warning("Please select at least one model provider.")
        st.stop()

    # Model provider selection for single model mode
    if view_mode == "Single Model":
        model_provider = st.selectbox(
            "Select Model Provider (Single Model Mode)",
            selected_providers,
            index=0,
        )
    else:
        model_provider = None  # Not used in multi-model mode

    provider_display_names = {
        "OpenAI": "🔵 OpenAI (GPT-3.5)",
        "Google Gemini": "🟣 Google Gemini (Gemini Pro)",
        "Anthropic Claude": "🟡 Anthropic Claude (Claude 3)",
        "Google Vertex AI": "🟢 Google Vertex AI (PaLM)",
        "Ollama (Llama3)": "🟠 Ollama (Llama 3)"
    }

    st.subheader("🔑 API Key Status")
    for prov in selected_providers:
        # Determine status and label
        if prov == "OpenAI":
            status = '✅' if st.session_state.get('openai_api_key') else '❌'
            label = f"OpenAI Key {status}"
            with st.expander(label, expanded=not st.session_state.get('openai_api_key')):
                openai_api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.get("openai_api_key", ""), key="openai_api_key_input")
                if openai_api_key:
                    st.session_state["openai_api_key"] = openai_api_key
        elif prov == "Google Gemini":
            status = '✅' if st.session_state.get('gemini_api_key') else '❌'
            label = f"Gemini Key {status}"
            with st.expander(label, expanded=not st.session_state.get('gemini_api_key')):
                gemini_api_key = st.text_input("Gemini API Key", type="password", value=st.session_state.get("gemini_api_key", ""), key="gemini_api_key_input")
                if gemini_api_key:
                    st.session_state["gemini_api_key"] = gemini_api_key
        elif prov == "Anthropic Claude":
            status = '✅' if st.session_state.get('anthropic_api_key') else '❌'
            label = f"Anthropic Key {status}"
            with st.expander(label, expanded=not st.session_state.get('anthropic_api_key')):
                anthropic_api_key = st.text_input("Anthropic API Key", type="password", value=st.session_state.get("anthropic_api_key", ""), key="anthropic_api_key_input")
                if anthropic_api_key:
                    st.session_state["anthropic_api_key"] = anthropic_api_key
                st.session_state.claude_model = st.text_input(
                    "Claude Model",
                    value=st.session_state.get("claude_model", "claude-3-haiku-20240307"),
                    key="claude_model_input"
                )
        elif prov == "Google Vertex AI":
            status_project = '✅' if st.session_state.get('vertexai_project') else '❌'
            status_region = '✅' if st.session_state.get('vertexai_region') else '❌'
            label = f"Vertex Project {status_project} / Region {status_region}"
            with st.expander(label, expanded=not (st.session_state.get('vertexai_project') and st.session_state.get('vertexai_region'))):
                vertexai_project = st.text_input("Vertex AI Project ID", value=st.session_state.get("vertexai_project", ""), key="vertexai_project_input")
                vertexai_region = st.text_input("Vertex AI Region", value=st.session_state.get("vertexai_region", "us-central1"), key="vertexai_region_input")
                if vertexai_project:
                    st.session_state["vertexai_project"] = vertexai_project
                if vertexai_region:
                    st.session_state["vertexai_region"] = vertexai_region
                st.session_state.vertexai_model = st.text_input(
                    "Vertex AI Model",
                    value=st.session_state.get("vertexai_model", "chat-bison"),
                    key="vertexai_model_input"
                )
        elif prov == "Ollama (Llama3)":
            status = '✅' if st.session_state.get('ollama_model') else '❌'
            label = f"Ollama Model {status}"
            with st.expander(label, expanded=not st.session_state.get('ollama_model')):
                ollama_model = st.text_input("Ollama Model", value=st.session_state.get("ollama_model", "llama3"), key="ollama_model_input")
                if ollama_model:
                    st.session_state["ollama_model"] = ollama_model
                st.session_state.ollama_temperature = st.slider(
                    "Ollama Temperature",
                    min_value=0.0,
                    max_value=1.0,
                    value=st.session_state.get("ollama_temperature", 0.7),
                    step=0.05,
                    key="ollama_temperature_input"
                )

    # Show masked keys for debugging
    st.markdown("---")
    st.subheader("🔍 Debug Info")
    st.write(f"**OpenAI:** `{mask_key(st.session_state.get('openai_api_key', ''))}`")
    st.write(f"**Gemini:** `{mask_key(st.session_state.get('gemini_api_key', ''))}`")
    st.write(f"**Anthropic:** `{mask_key(st.session_state.get('anthropic_api_key', ''))}`")
    st.write(f"**Vertex Project:** `{st.session_state.get('vertexai_project', '[not set]')}`")
    st.write(f"**Vertex Region:** `{st.session_state.get('vertexai_region', '[not set]')}`")
    if st.session_state.gac_set and st.session_state.gac_exists:
        st.write(f"**Google Vertex AI:** `{st.session_state.google_application_credentials or '[not set]'}`")
        st.write(f"**Google Vertex AI File Exists:** {'✅' if st.session_state.gac_exists else '❌'}")
    st.write(f"**Ollama Model:** `{st.session_state.get('ollama_model', '[not set]')}`")

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        if st.session_state.conversation:
            st.session_state.conversation.memory.clear()
        st.rerun()

# Helper: Check if provider has a valid API key/config
def provider_has_key(provider):
    if provider == "OpenAI":
        return bool(st.session_state.get("openai_api_key"))
    if provider == "Google Gemini":
        return bool(st.session_state.get("gemini_api_key"))
    if provider == "Anthropic Claude":
        return bool(st.session_state.get("anthropic_api_key"))
    if provider == "Google Vertex AI":
        return bool(st.session_state.get("vertexai_project")) and bool(st.session_state.get("vertexai_region"))
    if provider == "Ollama (Llama3)":
        return bool(st.session_state.get("ollama_model"))
    return False

# LLM selection logic
if view_mode == "Single Model":
    # Fallback logic for single model mode
    if not provider_has_key(model_provider):
        for prov in selected_providers:
            if provider_has_key(prov):
                model_provider = prov
                st.info(f"Falling back to {prov} as it has a valid API key/config.")
                break
        else:
            st.warning("No selected provider with a valid API key/config found. Please enter at least one API key.")
            st.stop()
    # LLM instantiation for single model
    if model_provider == "OpenAI":
        llm = ChatOpenAI(
            openai_api_key=st.session_state.get("openai_api_key"),
            model="gpt-3.5-turbo",
            temperature=0.7,
        )
    elif model_provider == "Google Gemini":
        llm = ChatGoogleGenerativeAI(
            google_api_key=st.session_state.get("gemini_api_key"),
            model="gemini-2.0-flash",
            temperature=0.7,
        )
    elif model_provider == "Anthropic Claude":
        llm = ChatAnthropic(
            anthropic_api_key=st.session_state.get("anthropic_api_key"),
            model=st.session_state.get("claude_model", "claude-3-haiku-20240307"),
            temperature=0.7,
        )
    elif model_provider == "Google Vertex AI":
        llm = ChatVertexAI(
            project=st.session_state.get("vertexai_project"),
            location=st.session_state.get("vertexai_region", "us-central1"),
            model=st.session_state.get("vertexai_model", "chat-bison"),
            temperature=0.7,
        )
    elif model_provider == "Ollama (Llama3)":
        llm = ChatOllama(
            model=st.session_state.get("ollama_model", "llama3"),
            temperature=st.session_state.get("ollama_temperature", 0.7),
        )
    else:
        st.error("No valid model provider selected.")
        st.stop()
else:
    # Multi-model mode: only use selected providers with valid keys/configs
    multi_llms = []
    for prov in selected_providers:
        if not provider_has_key(prov):
            continue
        if prov == "OpenAI":
            llm = ChatOpenAI(
                openai_api_key=st.session_state.get("openai_api_key"),
                model="gpt-3.5-turbo",
                temperature=0.7,
            )
        elif prov == "Google Gemini":
            llm = ChatGoogleGenerativeAI(
                google_api_key=st.session_state.get("gemini_api_key"),
                model="gemini-2.0-flash",
                temperature=0.7,
            )
        elif prov == "Anthropic Claude":
            llm = ChatAnthropic(
                anthropic_api_key=st.session_state.get("anthropic_api_key"),
                model=st.session_state.get("claude_model", "claude-3-haiku-20240307"),
                temperature=0.7,
            )
        elif prov == "Google Vertex AI":
            llm = ChatVertexAI(
                project=st.session_state.get("vertexai_project"),
                location=st.session_state.get("vertexai_region", "us-central1"),
                model=st.session_state.get("vertexai_model", "chat-bison"),
                temperature=0.7,
            )
        elif prov == "Ollama (Llama3)":
            llm = ChatOllama(
                model=st.session_state.get("ollama_model", "llama3"),
                temperature=st.session_state.get("ollama_temperature", 0.7),
            )
        else:
            continue
        multi_llms.append((prov, llm))
    if not multi_llms:
        st.warning("No selected provider with a valid API key/config found. Please enter at least one API key.")
        st.stop()

# After model_provider selection in the sidebar
if "active_provider" not in st.session_state:
    st.session_state.active_provider = model_provider

# Initialize the conversation chain if needed
if (
    st.session_state.conversation is None
    or st.session_state.llm_model != st.session_state.get("active_model")
    or st.session_state.temperature != st.session_state.get("active_temperature")
    or model_provider != st.session_state.get("active_provider")
):
    try:
        memory = ConversationBufferMemory()
        st.session_state.conversation = ConversationChain(
            llm=llm,
            memory=memory,
            verbose=False
        )
        st.session_state.active_model = st.session_state.llm_model
        st.session_state.active_temperature = st.session_state.temperature
        st.session_state.active_provider = model_provider
    except Exception as e:
        st.error(f"Error initializing chatbot: {e}")
        st.session_state.conversation = None

# Header
st.title("🤖 Multi Model Chatbot")
st.markdown("A simple chatbot built with LangChain and Streamlit and supporting multiple LLMs.")

# Add some spacing
st.markdown("---")

# Define avatar icons for each provider (same shape, different color)
PROVIDER_AVATARS = {
    "OpenAI": "🔵",           # Blue circle
    "Google Gemini": "🟣",    # Purple circle
    "Anthropic Claude": "🟡", # Yellow circle
    "Google Vertex AI": "🟢", # Green circle
    "Ollama (Llama3)": "🟠", # Orange circle
}

# Create a scrollable container for chat messages
chat_container = st.container()
with chat_container:
    # Add custom CSS for scrollable chat area
    st.markdown("""
    <style>
    .stChatMessage {
        max-height: 60vh;
        overflow-y: auto;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display chat messages in scrollable area
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            # Use the avatar for the provider that generated this message
            provider = message.get("provider", st.session_state.get("active_provider", "OpenAI"))
            avatar = PROVIDER_AVATARS.get(provider, "🤖")
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    if view_mode == "Single Model":
        # Single model mode (current behavior)
        avatar = PROVIDER_AVATARS.get(model_provider, "🤖")
        with st.chat_message("assistant", avatar=avatar):
            message_placeholder = st.empty()
            if st.session_state.conversation:
                try:
                    with st.spinner("Thinking..."):
                        response = st.session_state.conversation.predict(input=prompt)
                    message_placeholder.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response, "provider": model_provider})
                except Exception as e:
                    error_message = f"Error: {str(e)}"
                    message_placeholder.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message, "provider": model_provider})
            else:
                error_message = "Chatbot not initialized. Please check your API key configuration."
                message_placeholder.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message, "provider": model_provider})
    else:
        # Multi-model mode: query all providers and show all responses
        for provider_name, llm in multi_llms:
            avatar = PROVIDER_AVATARS.get(provider_name, "🤖")
            with st.chat_message("assistant", avatar=avatar):
                message_placeholder = st.empty()
                try:
                    with st.spinner(f"{provider_name} thinking..."):
                        # Use a simple ConversationChain for each provider (no memory)
                        response = llm.invoke(prompt) if hasattr(llm, "invoke") else llm.predict(input=prompt)
                        # Extract only the text content for chat models
                        if hasattr(response, "content") and isinstance(response.content, str):
                            response_text = response.content.strip()
                        elif isinstance(response, dict):
                            response_text = response.get("content") or response.get("text") or str(response)
                        else:
                            response_text = str(response)
                        response_text = response_text.strip()
                    answer = f"**{provider_name}:**\n{response_text}"
                    message_placeholder.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer, "provider": provider_name})
                except Exception as e:
                    error_message = f"**{provider_name}:**\nError: {str(e)}"
                    message_placeholder.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message, "provider": provider_name})

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        Built with ❤️ using LangChain and Streamlit and supporting multiple LLMs
    </div>
    """,
    unsafe_allow_html=True
) 
