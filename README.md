# LangChain Chatbot

A simple and interactive chatbot built with LangChain, OpenAI, and Streamlit. This application provides a conversational interface with memory capabilities and easy configuration options.

## Features

- 🤖 Interactive chat interface with Streamlit
- 🧠 Conversation memory using LangChain
- ⚙️ Configurable model selection (GPT-3.5, GPT-4, etc.)
- 🌡️ Adjustable temperature for response creativity
- 💬 Real-time chat with typing indicators
- 🗑️ Clear chat functionality
- 🔧 Easy configuration through sidebar

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd langchain-chatbot
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

4. **Set up your environment variables:**
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key:
   ```bash
   cp .env.example .env
   ```
   - Edit `.env` and replace `your_openai_api_key_here` with your actual OpenAI API key

## Usage

1. **Start the application:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser:**
   - The application will automatically open in your default browser
   - Usually available at `http://localhost:8501`

3. **Configure the chatbot:**
   - Use the sidebar to select your preferred model
   - Adjust the temperature for response creativity
   - Check if your API key is properly configured

4. **Start chatting:**
   - Type your messages in the chat input at the bottom
   - The chatbot will respond with context-aware replies
   - Use the "Clear Chat" button to start a new conversation

## Configuration Options

### Models Available
- **GPT-3.5 Turbo**: Fast and cost-effective (default)
- **GPT-4**: More capable but slower and more expensive
- **GPT-4 Turbo Preview**: Latest features and improvements

### Temperature Settings
- **0.0**: Very focused and deterministic responses
- **0.7**: Balanced creativity and consistency (default)
- **1.0**: Maximum creativity and variety

## Project Structure

```
langchain-chatbot/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── README.md          # This file
└── venv/              # Virtual environment (created during setup)
```

## Key Components

### LangChain Integration
- **ChatOpenAI**: Connects to OpenAI's API
- **ConversationBufferMemory**: Maintains conversation history
- **ConversationChain**: Orchestrates the chat flow

### Streamlit Features
- **Session State**: Persists chat history across interactions
- **Chat Interface**: Modern chat UI with user/assistant messages
- **Sidebar Configuration**: Easy access to settings
- **Error Handling**: Graceful handling of API errors

## Troubleshooting

### Common Issues

1. **"OpenAI API key not found" error:**
   - Ensure you've created a `.env` file with your API key
   - Check that the API key is valid and has sufficient credits

2. **Import errors:**
   - Make sure you've installed all dependencies: `pip install -r requirements.txt`
   - Verify you're using the correct Python version (3.8+)

3. **Streamlit not starting:**
   - Check if port 8501 is available
   - Try running with a different port: `streamlit run app.py --server.port 8502`

### Getting an OpenAI API Key

1. Visit [OpenAI's website](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to the API section
4. Create a new API key
5. Copy the key and add it to your `.env` file

## Customization

### Adding New Models
To add support for additional models, modify the model selection in `app.py`:

```python
model = st.selectbox(
    "Select Model",
    ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview", "your-new-model"],
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