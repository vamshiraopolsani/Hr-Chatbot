import streamlit as st
import json
from groq import Groq
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
CHAT_HISTORY_FILE = "chat_history.json"

# ── Intent Detection ───

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

# ── Dynamic System Prompt ───

def get_system_prompt(intent):
    dynamic_rules = {
        "absence": "CRITICAL FOCUS: Oracle Absence Management, Accrual Plans, and Leave Entitlements.",
        "core_hr": "CRITICAL FOCUS: Oracle Core HR, Security Profiles, Descriptive Flexfields (DFFs), and Worker Assignments.",
        "talent": "CRITICAL FOCUS: Talent Management, Performance Goals, and Succession.",
        "payroll": "CRITICAL FOCUS: Payroll calculation, Salary structures, and Compensation.",
        "recruitment": "CRITICAL FOCUS: Oracle Recruiting Cloud (ORC), Job Requisitions, Candidate Sourcing, and Onboarding.",
        "general": "CRITICAL FOCUS: General HR and Oracle HCM guidance."
    }
    dynamic_rule = dynamic_rules.get(intent, dynamic_rules["general"])

    return f"""You are a senior HR consultant and Oracle HCM Cloud specialist.
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

# ── Chat History ───

def load_chat_history():
    try:
        with open(CHAT_HISTORY_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_chat_history(history):
    with open(CHAT_HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

# ── Ask Bot ───

def ask_hr_bot(user_message, conversation, intent):
    conversation.append({"role": "user", "content": user_message})

    # Sliding window: only send last 6 messages
    recent_history = conversation[-6:]
    system_prompt = get_system_prompt(intent)

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

    conversation.append({"role": "assistant", "content": ai_reply})
    return ai_reply, conversation

# ── Intent Colors ───

INTENT_COLORS = {
    "absence": "🟠",
    "talent": "🟣",
    "payroll": "🟢",
    "recruitment": "🔵",
    "core_hr": "🔴",
    "general": "⚪"
}

# ── Streamlit UI ───

st.set_page_config(
    page_title="HR Expert Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for premium look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        text-align: center;
        padding: 1.5rem 0 1rem 0;
    }

    .main-header h1 {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }

    .main-header p {
        color: #888;
        font-size: 0.95rem;
    }

    .intent-badge {
        display: inline-block;
        padding: 0.2rem 0.7rem;
        border-radius: 1rem;
        font-size: 0.75rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea22, #764ba222);
        color: #667eea;
        border: 1px solid #667eea33;
        margin-bottom: 0.5rem;
    }

    .sidebar-info {
        padding: 1rem;
        border-radius: 0.75rem;
        background: linear-gradient(135deg, #667eea11, #764ba211);
        border: 1px solid #667eea22;
        margin-bottom: 1rem;
    }

    div[data-testid="stChatMessage"] {
        border-radius: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 HR Expert Chatbot</h1>
    <p>Powered by LLaMA 3.3 · Oracle HCM Cloud Specialist</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 💡 About")
    st.markdown("""
    <div class="sidebar-info">
        <strong>HR Expert Chatbot</strong> answers questions about Oracle HCM Cloud modules:
        <br><br>
        🔴 Core HR &nbsp; 🟠 Absence<br>
        🟣 Talent &nbsp; 🟢 Payroll<br>
        🔵 Recruitment &nbsp; ⚪ General
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚙️ Model")
    st.code("LLaMA 3.3 70B via Groq", language=None)

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; color:#888; font-size:0.8rem;'>Built by Vamshi<br>Oracle HCM + AI</p>",
        unsafe_allow_html=True
    )

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and "intent" in msg:
            emoji = INTENT_COLORS.get(msg["intent"], "⚪")
            st.markdown(
                f'<span class="intent-badge">{emoji} {msg["intent"].upper()}</span>',
                unsafe_allow_html=True
            )
        st.markdown(msg["content"])

# Chat input
if user_input := st.chat_input("Ask an HR question..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Detect intent
    intent = detect_intent(user_input)

    # Get bot response
    with st.chat_message("assistant"):
        emoji = INTENT_COLORS.get(intent, "⚪")
        st.markdown(
            f'<span class="intent-badge">{emoji} {intent.upper()}</span>',
            unsafe_allow_html=True
        )
        with st.spinner("Thinking..."):
            ai_reply, st.session_state.conversation = ask_hr_bot(
                user_input, st.session_state.conversation, intent
            )
        st.markdown(ai_reply)

    # Save to session state
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply,
        "intent": intent
    })

    # Save to JSON file
    file_history = load_chat_history()
    file_history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user_input,
        "bot": ai_reply,
        "topic": intent
    })
    save_chat_history(file_history)
