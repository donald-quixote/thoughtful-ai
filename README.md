# Thoughtful-AI Chatbot

**NOTE**: This is a naive implementation with a single multi-shot prompt.
A more robust implementation would use RAG with a vector database as the knowledge base,
and possibly break the flow into multiple steps to make a more refined conversation flow.

**NOTE**: I wrote the LLM messages, auto-generated this code with co-pilot and revised to wrap in classes and clean up.
I am not a python expert, but chose python for more practice.
I primarily code against the JVM :)

## Steps to Run the Chatbot

1. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

2. **Set your OpenAI API key**:
   - Create a `.env` file or set the environment variable in your shell:
     ```sh
     export OPENAI_API_KEY=sk-...
     ```
   - Or add to `.env`:
     ```
     OPENAI_API_KEY=sk-...
     ```

3. **Run the chatbot**:
   ```sh
   python thoughtful_ai_chatbot.py
   ```
   This will launch a Gradio web interface in your browser.

---

## Notes
- Requires Python 3.8+
- You must have a valid OpenAI API key with access to `gpt-3.5-turbo` or compatible model.
- For troubleshooting, see error messages in the terminal or browser.