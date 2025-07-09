# Multi Model Chatbot using LangChain and Streamlit

A simple and interactive chatbot built with LangChain, supporting OpenAI (GPT-3.5 Turbo), Google Gemini, Anthropic Claude (claude-3-7-sonnet-20250219), Google Vertex AI (gemini-2.5-flash), and Ollama (Llama3) models. This application provides a conversational interface with memory capabilities, multi-modal support (text and images, where supported by the model), and easy configuration options.

- 🤖 **Multi-provider:** Use OpenAI, Google Gemini, Anthropic Claude, Google Vertex AI, or Ollama (Llama3) models
- 🖼️ **Multi-modal:** Supports text and (where available) image input/output with Gemini, Vertex AI, and future OpenAI models
- 🧠 **Conversation memory:** Remembers chat history for context-aware responses
- ⚙️ **Configurable:** Easily switch models and API keys in the sidebar
- 💬 **Modern UI:** Real-time chat with typing indicators and clear chat functionality
- 🔄 **Multi-model mode:** Query all available models simultaneously and compare responses

## Features

- 🤖 Interactive chat interface with Streamlit
- 🧠 Conversation memory using LangChain
- ⚙️ Configurable model selection (OpenAI, Gemini, Claude, Vertex AI, Ollama)
- 🌡️ Adjustable temperature for response creativity
- 💬 Real-time chat with typing indicators
- 🗑️ Clear chat functionality
- 🔧 Easy configuration through sidebar
- 🔄 Single model vs multi-model chat modes
- 🎨 Provider-specific colored avatars for easy identification

## Supported Models

- **OpenAI (GPT-3.5 Turbo)**
- **Google Gemini**
- **Anthropic Claude (claude-3-sonnet)**
- **Google Vertex AI (gemini-2.5-flash)**
- **Ollama (Llama3)**

## Prerequisites

- Python 3.8 or higher
- API keys for your chosen provider(s):
  - OpenAI API key (for GPT-3.5 Turbo)
  - Google Gemini API key (for gemini-2.0-flash)
  - Anthropic API key (for Claude)
  - Google Cloud service account key + project ID (for Vertex AI)
  - [Ollama](https://ollama.com/) installed and running locally (for Llama3)

## Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd multimodel-chatbot
   ```
2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Install Ollama (for Llama3 support):**
   - [Download and install Ollama](https://ollama.com/download) for your OS (macOS, Linux, Windows WSL)
   - Start Ollama (it runs as a background service):
     ```bash
     ollama serve
     ```
   - Pull the Llama3 model:
     ```bash
     ollama pull llama3
     ```

### Environment Variables
Copy `.env.example` to `.env` and fill in the required keys:

- [Get your OpenAI API key here](https://platform.openai.com/api-keys)
- [Get your Gemini API key here](https://aistudio.google.com/app/apikey)
- [Get your Anthropic API key here](https://console.anthropic.com/)

```
OPENAI_API_KEY=your-openai-api-key
GEMINI_API_KEY=your-gemini-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
VERTEXAI_PROJECT_ID=your-gcp-project-id
VERTEXAI_REGION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-file.json
```

- For Vertex AI, you must also set up a Google Cloud service account and download the JSON key (see Vertex AI Setup above).

### .gitignore
- The `.gitignore` file ensures that `venv/`, `.env`, `.env.example`, and Google Cloud service account keys are not committed to the repository.

## Usage

1. **Start the application:**
   ```bash
   streamlit run app.py
   ```
2. **Open your browser:**
   - The application will automatically open in your default browser
   - Usually available at `http://localhost:8501`
3. **Configure the chatbot:**
   - Use the sidebar to select your preferred chat mode:
     - **Single Model:** Chat with one selected provider
     - **Multi-Model:** Query all available models simultaneously
   - Select your preferred model provider (OpenAI, Gemini, Claude, Vertex AI, or Ollama)
   - Enter the appropriate API key for the selected model (not needed for Ollama)
   - For Ollama, set the model name (default: `llama3`) and temperature
   - Adjust the temperature for response creativity
   - Check if your API key or model is properly configured (status is shown for all providers)
4. **Start chatting:**
   - Type your messages in the chat input at the bottom
   - The chatbot will respond with context-aware replies
   - Each response is color-coded with the provider's avatar for easy identification
   - Use the "Clear Chat" button to start a new conversation

## Notes
- You can use OpenAI (GPT-3.5 Turbo), Google Gemini (gemini-2.0-flash), Anthropic Claude (claude-3-sonnet), Google Vertex AI (chat-bison), or Ollama (Llama3) models by selecting them in the sidebar.
- Choose between **Single Model** mode (one provider) or **Multi-Model** mode (all providers simultaneously).
- Each provider has a unique colored avatar: 🔵 OpenAI, 🟣 Google Gemini, 🟡 Anthropic Claude, 🟢 Google Vertex AI, 🟠 Ollama (Llama3).
- The sidebar will show the status of all API keys and allow you to enter or update them at any time. For Ollama, it will show the model name.
- Debug information is shown in the sidebar and above each assistant response to help you verify which model and key are being used.

## Troubleshooting
- If you see a 401 error, double-check that the correct API key is entered for the selected model.
- For Gemini, your key should **not** start with `sk-` (that's an OpenAI key).
- For OpenAI, your key should start with `sk-`.
- For Anthropic, your key should start with `sk-ant-`.

## Configuration Options

### Chat Modes
- **Single Model:** Chat with one selected provider (traditional mode)
- **Multi-Model:** Query all available models simultaneously and compare responses

### Models Available
- **GPT-3.5 Turbo**: Fast and cost-effective (default)
- **Gemini 2.0 Flash**: Google's latest model with multi-modal support
- **Claude 3 Sonnet**: Anthropic's balanced model for general use
- **Vertex AI Chat Bison**: Google's enterprise model via Vertex AI
- **Ollama (Llama3)**: Open-source LLM running locally via Ollama

### Provider Avatars
Each provider has a unique colored avatar for easy identification:
- 🔵 **OpenAI** - Blue circle
- 🟣 **Google Gemini** - Purple circle  
- 🟡 **Anthropic Claude** - Yellow circle
- 🟢 **Google Vertex AI** - Green circle
- 🟠 **Ollama (Llama3)** - Orange circle

### Temperature Settings
- **0.0**: Very focused and deterministic responses
- **0.7**: Balanced creativity and consistency (default)
- **1.0**: Maximum creativity and variety

## Project Structure

```
multimodel-chatbot/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── README.md          # This file
└── venv/              # Virtual environment (created during setup)
```

## Key Components

### LangChain Integration
- **ChatOpenAI**: Connects to OpenAI's API
- **ChatGoogleGenerativeAI**: Connects to Google's Gemini API
- **ChatAnthropic**: Connects to Anthropic's Claude API
- **ChatVertexAI**: Connects to Google's Vertex AI
- **ChatOllama**: Connects to local Ollama models
- **ConversationBufferMemory**: Maintains conversation history
- **ConversationChain**: Orchestrates the chat flow

### Streamlit Features
- **Session State**: Persists chat history across interactions
- **Chat Interface**: Modern chat UI with user/assistant messages
- **Sidebar Configuration**: Easy access to settings
- **Error Handling**: Graceful handling of API errors

## Customization

### Adding New Models
To add support for additional models, modify the model selection in `app.py`:

```python
model_provider = st.selectbox(
    "Select Model Provider",
    ["OpenAI", "Google Gemini", "Anthropic Claude", "Google Vertex AI", "Ollama (Llama3)", "your-new-provider"],
    index=0
)
```

### Custom Prompts
You can customize the system prompt by modifying the ConversationChain initialization in `app.py`.

### Styling
The application uses Streamlit's default styling, but you can customize it by adding custom CSS in the `st.markdown()` sections.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this chatbot!

## License

This project is open source and available under the MIT License.

## How to Get Anthropic Claude API Key

To get an Anthropic Claude API key, follow these steps:

### Step-by-Step Guide

1. **Create an Anthropic Account**
   - Go to [https://console.anthropic.com/](https://console.anthropic.com/)
   - Click "Sign Up" or "Get Started"
   - Create an account using your email address

2. **Verify Your Account**
   - Check your email for a verification link
   - Click the link to verify your account
   - Complete any additional verification steps if required

3. **Access the API Console**
   - Log in to your Anthropic console
   - Navigate to the "API Keys" section (usually in the left sidebar)

4. **Create a New API Key**
   - Click "Create Key" or "Generate API Key"
   - Give your key a descriptive name (e.g., "Multi Model Chatbot")
   - Copy the generated API key immediately (it starts with `sk-ant-`)

5. **Set Up Your Environment**
   - Add the key to your `.env` file:
     ```
     ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
     ```
   - Or enter it directly in the app's sidebar when using Claude

### Important Notes:

- **Key Format**: Anthropic API keys start with `sk-ant-` (not `sk-` like OpenAI)
- **Security**: Keep your API key secure and never commit it to version control
- **Billing**: Anthropic may require you to add billing information before using the API
- **Rate Limits**: Check Anthropic's documentation for current rate limits and pricing

### Troubleshooting:
- If you see a 401 error, make sure your key starts with `sk-ant-`
- If you get a billing error, you may need to add payment information to your Anthropic account
- The key should be about 50+ characters long

Once you have your API key, you can select "Anthropic Claude" in the app's sidebar and start chatting with Claude!

## How to Find Your Google Cloud Project ID

Your **Google Cloud Project ID** is a unique identifier for your project in Google Cloud. Here’s how you can find it:

### Method 1: Google Cloud Console (Web UI)
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. At the top left, click the project dropdown (it may show your current project name).
3. In the list, you’ll see all your projects.  
   - The **Project ID** is shown in the “ID” column (not the “Name” column).
   - It usually looks like: `my-sample-project-123456`

### Method 2: Command Line (gcloud CLI)
If you have the Google Cloud SDK installed, run:
```sh
gcloud projects list
```
This will show a table with your project names, IDs, and numbers.

### Method 3: Billing or API Dashboard
- When you enable billing or APIs, the project ID is often shown in the dashboard or URL.

**Note:**
- The Project ID is globally unique and is used in API calls and configuration.
- Do not confuse it with the Project Name (which is just a label and can be changed). 

## How to Get Google Vertex AI Credentials

To use Vertex AI, you need a Google Cloud service account key (JSON file) with the right permissions. Here’s how to get it:

1. **Create a Google Cloud Project**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Click the project dropdown at the top and select “New Project”.

2. **Enable Vertex AI API**
   - In your project, go to “APIs & Services” > “Enable APIs and Services”.
   - Search for “Vertex AI API” and enable it.

3. **Create a Service Account**
   - Go to “IAM & Admin” > “Service Accounts”.
   - Click “Create Service Account”.
   - Give it a name (e.g., `vertex-ai-sa`).
   - Click “Create and Continue”.

4. **Grant Vertex AI Permissions**
   - Assign the role: `Vertex AI User` (or `Vertex AI Admin` for full access).
   - Click “Continue” and then “Done”.

5. **Create and Download a Service Account Key**
   - Click on your new service account in the list.
   - Go to the “Keys” tab.
   - Click “Add Key” > “Create new key”.
   - Choose “JSON” and click “Create”.
   - Download the JSON file and keep it safe (this is your “API key” for Vertex AI).

6. **Set the Environment Variable**
   - Set the environment variable in your shell or `.env` file:
     ```
     GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-file.json
     ```
     Replace `/path/to/your/service-account-file.json` with the actual path to your downloaded JSON key.

7. **Set Project and Region**
   - In your `.env` or via the app sidebar, set:
     ```
     VERTEXAI_PROJECT_ID=your-gcp-project-id
     VERTEXAI_REGION=us-central1
     ```

**References:**
- [Google Cloud: Creating and managing service account keys](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)
- [Vertex AI Python Client Authentication](https://cloud.google.com/vertex-ai/docs/start/client-auth) 

### Ollama (Llama3) Setup

1. **Install Ollama:**
   - Download from [ollama.com/download](https://ollama.com/download) and follow the installation instructions for your OS.
2. **[macOS] If you installed via the .app and get 'command not found', create a symlink:**
   - This lets you run `ollama` from any terminal window:
     ```sh
     sudo ln -s /Applications/Ollama.app/Contents/Resources/ollama /usr/local/bin/ollama
     ```
   - Then test with:
     ```sh
     ollama --version
     ```
3. **Start Ollama:**
   - Run `ollama serve` in your terminal (Ollama may start automatically on some systems).
4. **Pull the Llama3 model:**
   - Run `ollama pull llama3` to download the model.
5. **Test a One-off Prompt**
   - You can also run a single prompt and get a response:
      ```sh
      echo "Tell me a joke." | ollama run llama3
      ```
   - You should see a joke as output.
5. **Select Ollama (Llama3) in the sidebar:**
   - No API key is required. Set the model name (default: `llama3`) and temperature as desired.
6. **Chat!**

For more details, see the [Ollama documentation](https://ollama.com/). 

