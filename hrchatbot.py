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

def detect_intent(user_message):
    keywords = {
        "absence": ["leave", "absence", "vacation", "sick", "maternity", "paternity"],
        "talent": ["performance", "goal", "appraisal", "succession", "training"],
        "payroll": ["salary", "payroll", "bonus", "increment", "compensation"],
        "recruitment": ["hire", "recruit", "interview", "onboard", "joining"],
        "core_hr": ["employee", "position", "department", "org", "transfer"]
    }
    
    message_lower = user_message.lower()
    
    for intent, words in keywords.items():
        if any(word in message_lower for word in words):
            return intent
    
    return "general"

def load_chat_history():
    try:
        with open(CHAT_HISTORY_FILE,"r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_chat_history(history):
    with open(CHAT_HISTORY_FILE,"w") as file:
        json.dump(history, file, indent=4)

def ask_hr_bot(user_message, conversation, intent):
    # Dynamic system prompt based on detected intent
    dynamic_rule = ""
    if intent == "absence":
        dynamic_rule = "CRITICAL FOCUS: Oracle Absence Management, Accrual Plans, and Leave Entitlements."
    elif intent == "core_hr":
        dynamic_rule = "CRITICAL FOCUS: Oracle Core HR, Security Profiles, Descriptive Flexfields (DFFs), and Worker Assignments."
    elif intent == "talent":
        dynamic_rule = "CRITICAL FOCUS: Talent Management, Performance Goals, and Succession."
    elif intent == "payroll":
        dynamic_rule = "CRITICAL FOCUS: Payroll calculation, Salary structures, and Compensation."
    elif intent == "recruitment":
        dynamic_rule = "CRITICAL FOCUS: Oracle Recruiting Cloud (ORC), Job Requisitions, Candidate Sourcing, and Onboarding."
    else:
        dynamic_rule = "CRITICAL FOCUS: General HR and Oracle HCM guidance."

    system_prompt = f"""You are a senior HR consultant and Oracle HCM Cloud specialist.
    Context: Indian IT company
    Tone: Professional

    {dynamic_rule}

    How you respond:
    - Always give clear, structured, professional answers
    - Use bullet points for complex topics
    - If a question is outside HR scope, politely redirect
    - Keep answers concise but complete

    Think step by step before answering complex HR policy questions.

    Examples:
    Q: What is an Annual Leave policy?
    A: Annual Leave Policy:
       - Employees are entitled to X days per year
       - Must be approved by line manager
       - Cannot be carried forward beyond March 31
       - Encashment allowed up to 50% of balance
    """

    # Add the raw user question to memory
    conversation.append({
        "role": "user",
        "content": user_message
    })

    # Sliding window: only send last 6 messages (3 Q&A turns) to avoid clutter
    recent_history = conversation[-6:]

    try:
        response = client.chat.completions.create(
            temperature=0.3,
            max_tokens=1024,
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt}
            ] + recent_history
        )
        ai_reply = response.choices[0].message.content
    except Exception as e:
        ai_reply = f"⚠️ Sorry, I couldn't process your request. Error: {str(e)}"

    conversation.append({
        "role": "assistant",
        "content": ai_reply
    })

    return ai_reply, conversation

def format_response(ai_reply, intent, user_input):
    return {
        "question": user_input,
        "topic": intent,
        "answer": ai_reply,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model": "llama-3.3-70b-versatile"
    }

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

        intent = detect_intent(user_input)
        print(f"\n📌 Topic detected: {intent.upper()}")
        print("\n🤖 Bot: thinking...")

        ai_reply, conversation = ask_hr_bot(user_input, conversation, intent)
        structured_response = format_response(ai_reply, intent, user_input)
        print(f"\n📌 Topic: {structured_response['topic'].upper()}")
        print(f"\n🤖 Bot: {structured_response['answer']}")

        chat_history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": user_input,
            "bot": ai_reply,
            "topic": intent
        })

        save_chat_history(chat_history)

# ── Run ───
run_chatbot()