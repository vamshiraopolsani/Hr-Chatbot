import json
from groq import Groq
from datetime import datetime

#---setup---

from dotenv import load_dotenv
import os
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
CHAT_HISTORY_FILE = "chat_history.json"

#---functions---

def load_chat_history():
    try:
        with open(CHAT_HISTORY_FILE,"r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_chat_history(history):
    with open(CHAT_HISTORY_FILE,"w") as file:
        json.dump(history, file, indent=4)

def ask_hr_bot(user_message, conversation):
    conversation.append({
        "role": "user",
        "content": user_message
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert HR consultant with deep knowledge of Oracle HCM Cloud, HR policies, talent management, and absence management. Give clear, professional answers."}
        ] + conversation
    )

    ai_reply = response.choices[0].message.content

    conversation.append({
        "role": "assistant",
        "content": ai_reply
    })

    return ai_reply, conversation

def run_chatbot():
    print("=" * 50)
    print("   🤖 HR Expert Chatbot powered by LLaMA")
    print("=" * 50)
    print("Type your HR question below.")
    print("Type 'history' to see past chats.")
    print("Type 'exit' to quit.")
    print("=" * 50)

    chat_history = load_chat_history()
    conversation = []

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            print("\n👋 Goodbye! Chat saved to chat_history.json")
            break

        elif user_input.lower() == "history":
            if not chat_history:
                print("No history yet!")
            else:
                for entry in chat_history:
                    print(f"\n[{entry['timestamp']}]")
                    print(f"You: {entry['user']}")
                    print(f"Bot: {entry['bot']}")
            continue

        elif user_input == "":
            print("Please type a question!")
            continue

        print("\n🤖 Bot: thinking...")
        ai_reply, conversation = ask_hr_bot(user_input, conversation)
        print(f"\n🤖 Bot: {ai_reply}")

        chat_history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": user_input,
            "bot": ai_reply
        })

        save_chat_history(chat_history)

# ── Run ───
run_chatbot()