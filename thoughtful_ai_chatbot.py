import os
import sys
import gradio as gr
from openai import OpenAI
from typing import List, Dict, Generator

# -------------------------------
# LLM WRAPPER CLASS
# -------------------------------
LLMMessage = Dict[str, str]
class GradioChatbot:
    def __init__(self, openai_client: OpenAI, model: str, system_prompt: str, seed_messages: List[LLMMessage] = []):
        self.openai_client = openai_client
        self.model = model
        self.system_prompt = system_prompt
        self.seed_messages = seed_messages
        
    def chat(self, user_prompt: str, history: List[LLMMessage]) -> Generator[str, None, None]:
        try:
            input_error = self.validate_input(user_prompt)
            if input_error:
                yield input_error
                return
            messages = [{"role": "system", "content": self.system_prompt}] 
            messages += self.seed_messages 
            messages += history 
            messages += [{"role": "user", "content": user_prompt}]
            stream = self.openai_client.chat.completions.create(model=self.model, messages=messages, stream=True)
            response = ""
            for chunk in stream:
                try:
                    response += chunk.choices[0].delta.content or ''
                    yield response
                except Exception as e:
                    yield f"[ERROR] Error while streaming response: {e}"
                    return
        except Exception as e:
            yield f"[ERROR] Failed to get response from OpenAI: {e}"
            return
        
    def validate_input(self, user_prompt: str, max_length: int = 512) -> str:
        if not isinstance(user_prompt, str):
            return "Input must be a string."
        if not user_prompt.strip():
            return "Please enter a valid question."
        if len(user_prompt) > max_length:
            return f"Input is too long (>{max_length} characters). Please shorten your question."
        # Check for mostly non-alphanumeric (gibberish, symbols, emojis)
        alnum_count = sum(c.isalnum() for c in user_prompt)
        if alnum_count < max(3, len(user_prompt) // 8):
            return "Input does not appear to be a valid question."
        return ""
    
    

class ThoughtfulAIChatbot:

    @staticmethod
    def buildChatbot(openai_client: OpenAI) -> GradioChatbot:
        model = "gpt-3.5-turbo"
        knowledge_base = {
            "EVA": {
                "question": "What does the eligibility verification agent (EVA) do?",
                "answer": "EVA automates the process of verifying a patient’s eligibility and benefits information in real-time, eliminating manual data entry errors and reducing claim rejections."
            },
            "CAM": {
                "question": "What does the claims processing agent (CAM) do?",
                "answer": "CAM streamlines the submission and management of claims, improving accuracy, reducing manual intervention, and accelerating reimbursements."
            },
            "PHIL": {
                "question": "How does the payment posting agent (PHIL) work?",
                "answer": "PHIL automates the posting of payments to patient accounts, ensuring fast, accurate reconciliation of payments and reducing administrative burden."
            },
            "agents": {
                "question": "Tell me about Thoughtful AI's Agents.",
                "answer": "Thoughtful AI provides a suite of AI-powered automation agents designed to streamline healthcare processes. These include Eligibility Verification (EVA), Claims Processing (CAM), and Payment Posting (PHIL), among others."
            },
            "benefits": {
                "question": "What are the benefits of using Thoughtful AI's agents?",
                "answer": "Using Thoughtful AI's Agents can significantly reduce administrative costs, improve operational efficiency, and reduce errors in critical processes like claims management and payment posting."
            }
        }
        system_prompt = f"""
            You are a helpful AI assistant for Thoughtful AI, with the following knowledge base (KB): 
            ${knowledge_base}
            
            When I ask you a question, compare it with the KB questions. 
            If one question in the KB matches well with my question, then return the exact answer associated to that question in the KB.
            If the question does not relate to Thoughtful AI, then do not answer the question. Acknowledge the question is outside of your area of expertise and ask how you can help me.
            If none of the KB questions match well, then tell me to visit https://www.thoughtful.ai/ for more information, and say that is what you would do if your creator had time to give you tools.
            If I make a statement rather than a question, and it contradicts any answer in the KB, then provide the answer my statement contradicts.
            If I make a statement rather than a question, and it is about an entry in the KB and aligns, then agree with me and ask how you can assist me.
            If I make a statement rather than a question, and it is not related to Thoughtful AI, then do not agree or disagree. Provide a witty segue into asking how you can help me.
            """
        seed_messages = [
            {"role": "user", "content": "Tell me about your payment agent"},
            {"role": "assistant", "content": knowledge_base["PHIL"]["answer"]},
            {"role": "user", "content": "What are agents?"},
            {"role": "assistant", "content": knowledge_base["agents"]["answer"]},
            {"role": "user", "content": "why would I use Thoughful AI"},
            {"role": "assistant", "content": knowledge_base["benefits"]["answer"]},
            {"role": "user", "content": "why should I care about cheese"},
            {"role": "assistant", "content": "That is not in my area of expertise. How can I assist you with Thoughtful AI?"},
            {"role": "user", "content": "I support bagel taxes on frogs, and you should to."},
            {"role": "assistant", "content": "While I cannot speak on that topic, I can tell you anything you wish to know about Thought AI. How can I assist you"},
        ]
        return GradioChatbot(openai_client, model, system_prompt, seed_messages)


# -------------------------------
# GRADIO APP
# -------------------------------
try:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    open_ai_client = OpenAI(api_key=OPENAI_API_KEY)
    chatbot = ThoughtfulAIChatbot.buildChatbot(open_ai_client)
    gr.ChatInterface(fn=chatbot.chat, type="messages").launch(inbrowser=True)
except Exception as e:
    print(f"[ERROR] Somemething went wrong and no fine-grained error handling was implemented: {e}")
    sys.exit(1)
