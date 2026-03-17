"""
Medical AI Chatbot — Streamlit App
Powered by OpenRouter API (anthropic/claude-sonnet-4-5)
"""

import streamlit as st
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv
from knowledge_base import MEDICAL_KNOWLEDGE, SYMPTOM_CHECKER, EMERGENCY_KEYWORDS

load_dotenv()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MediAssist AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

/* Root variables */
:root {
    --med-blue: #1a6b8a;
    --med-teal: #0d9488;
    --med-light: #f0f9ff;
    --med-border: #bae6fd;
    --emergency: #dc2626;
    --warning: #d97706;
    --success: #059669;
    --text-primary: #0f172a;
    --text-secondary: #475569;
}

/* Global font */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Hide default streamlit header */
#MainMenu, footer, header { visibility: hidden; }

/* App background */
.stApp {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #f0fdf4 100%);
    min-height: 100vh;
}

/* Main chat container */
.main-header {
    background: linear-gradient(135deg, #0f4c75 0%, #1a6b8a 50%, #0d9488 100%);
    padding: 1.5rem 2rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(15, 76, 117, 0.25);
    color: white;
}

.main-header h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    margin: 0;
    letter-spacing: -0.5px;
}

.main-header p {
    margin: 0.3rem 0 0;
    opacity: 0.85;
    font-size: 0.9rem;
    font-weight: 300;
}

/* Chat messages */
.chat-message {
    padding: 1rem 1.25rem;
    border-radius: 14px;
    margin: 0.6rem 0;
    font-size: 0.95rem;
    line-height: 1.65;
    animation: fadeInUp 0.3s ease;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

.user-message {
    background: linear-gradient(135deg, #0f4c75, #1a6b8a);
    color: white;
    margin-left: 10%;
    border-bottom-right-radius: 4px;
    box-shadow: 0 4px 15px rgba(15, 76, 117, 0.2);
}

.assistant-message {
    background: white;
    color: var(--text-primary);
    margin-right: 10%;
    border: 1px solid var(--med-border);
    border-bottom-left-radius: 4px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

.emergency-message {
    background: linear-gradient(135deg, #fff1f2, #ffe4e6);
    border: 2px solid #fecdd3;
    border-left: 5px solid var(--emergency);
    color: #991b1b;
    margin-right: 10%;
    border-bottom-left-radius: 4px;
}

/* Message avatar row */
.message-row {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    margin: 0.5rem 0;
}

.avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
    margin-top: 2px;
}

.avatar-user {
    background: linear-gradient(135deg, #0f4c75, #1a6b8a);
    color: white;
}

.avatar-bot {
    background: linear-gradient(135deg, #0d9488, #059669);
    color: white;
}

/* Disclaimer box */
.disclaimer-box {
    background: linear-gradient(135deg, #fffbeb, #fef3c7);
    border: 1px solid #fcd34d;
    border-left: 4px solid var(--warning);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    font-size: 0.82rem;
    color: #92400e;
    margin: 1rem 0;
    line-height: 1.5;
}

/* Emergency alert */
.emergency-alert {
    background: linear-gradient(135deg, #fff1f2, #ffe4e6);
    border: 2px solid var(--emergency);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    font-size: 0.88rem;
    color: #991b1b;
    margin: 0.5rem 0;
    font-weight: 500;
}

/* Sidebar styling */
.sidebar-section {
    background: white;
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 6px rgba(0,0,0,0.04);
}

.sidebar-title {
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-secondary);
    margin-bottom: 0.7rem;
}

/* Quick question chips */
.chip-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-top: 0.5rem;
}

/* Metric cards */
.metric-card {
    background: white;
    border-radius: 10px;
    padding: 0.8rem;
    text-align: center;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

/* Typing indicator */
.typing-indicator {
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 0.8rem 1rem;
}

.typing-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--med-teal);
    animation: bounce 1.2s infinite;
}

.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}

/* Input area */
.stTextInput > div > div > input {
    border-radius: 12px !important;
    border: 2px solid #bae6fd !important;
    padding: 0.7rem 1rem !important;
    font-size: 0.95rem !important;
    transition: border-color 0.2s !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--med-teal) !important;
    box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.12) !important;
}

/* Buttons */
.stButton > button {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.12) !important;
}

/* Scrollable chat area */
.chat-scroll {
    max-height: 520px;
    overflow-y: auto;
    padding-right: 4px;
    scroll-behavior: smooth;
}

.chat-scroll::-webkit-scrollbar {
    width: 5px;
}
.chat-scroll::-webkit-scrollbar-track {
    background: transparent;
}
.chat-scroll::-webkit-scrollbar-thumb {
    background: #bae6fd;
    border-radius: 4px;
}

/* Status badge */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #dcfce7;
    color: #166534;
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    font-size: 0.78rem;
    font-weight: 500;
}

.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #22c55e;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}
</style>
""", unsafe_allow_html=True)


# ── Session state initialization ───────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "client" not in st.session_state:
    st.session_state.client = None
if "conversation_count" not in st.session_state:
    st.session_state.conversation_count = 0
if "session_start" not in st.session_state:
    st.session_state.session_start = datetime.now()

# ── OpenRouter model config ────────────────────────────────────────────────────
OPENROUTER_MODEL = "anthropic/claude-sonnet-4-5"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


# ── OpenRouter client ──────────────────────────────────────────────────────────
def get_client():
    """Initialize and return the OpenRouter client (OpenAI-compatible)."""
    if st.session_state.client is None:
        try:
            import os
            from dotenv import load_dotenv
            
            # Explicitly load .env from the script's directory
            env_path = os.path.join(os.path.dirname(__file__), ".env")
            load_dotenv(env_path, override=True)
            
            api_key = os.environ.get("OPENROUTER_API_KEY")
            
            if not api_key:
                try:
                    # Streamlit might raise an exception if secrets.toml is missing
                    api_key = st.secrets.get("OPENROUTER_API_KEY", None)
                except Exception:
                    pass
            
            if not api_key:
                st.error("⚠️ OPENROUTER_API_KEY not found. Add it to `.env` or `.streamlit/secrets.toml`.")
                return None
                
            st.session_state.client = OpenAI(
                base_url=OPENROUTER_BASE_URL,
                api_key=api_key.strip(),
            )
        except Exception as e:
            st.error(f"Failed to initialize OpenRouter client: {e}")
            return None
    return st.session_state.client


# ── Emergency keyword detection ────────────────────────────────────────────────
def check_emergency(text: str) -> bool:
    text_lower = text.lower()
    return any(kw in text_lower for kw in EMERGENCY_KEYWORDS)


# ── System prompt ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are MediAssist AI, a compassionate and knowledgeable medical information assistant. 
You provide helpful, accurate medical information while always maintaining appropriate boundaries.

YOUR CORE PRINCIPLES:
1. Always recommend consulting a licensed healthcare professional for diagnosis and treatment
2. Provide evidence-based, clear medical information
3. Never diagnose conditions — only explain symptoms, conditions, and general information
4. Show empathy and compassion in all responses
5. For any emergency symptoms, immediately direct to emergency services (112 in India, 911 in USA)
6. Keep responses well-structured with clear sections when appropriate
7. Use simple language — avoid heavy medical jargon unless explaining technical terms

YOUR CAPABILITIES:
- Explain medical conditions, symptoms, and terminology
- Provide information about medications (general, not dosage advice)
- Describe common treatments and procedures (informational only)
- Offer general wellness, nutrition, and preventive health tips
- Guide users on when to seek medical attention
- Answer questions about lab tests, medical procedures (general info)

RESPONSE FORMAT:
- Use bullet points or numbered lists for symptoms/steps
- Bold key terms for emphasis
- Include a "⚕️ Important Note" section when recommending professional consultation
- Keep responses concise but complete — typically 150-300 words
- Use emojis sparingly but meaningfully (🩺 💊 ❤️ ⚠️)

WHAT YOU NEVER DO:
- Never provide specific dosage recommendations
- Never diagnose a patient
- Never replace emergency medical services
- Never recommend stopping prescribed medications
- Never give advice that contradicts standard medical guidelines

MEDICAL KNOWLEDGE BASE CONTEXT:
{knowledge_context}

Remember: You are a supportive guide, not a replacement for professional medical care."""


def build_system_prompt() -> str:
    knowledge_context = "\n".join([
        f"- {topic}: {info}"
        for topic, info in list(MEDICAL_KNOWLEDGE.items())[:10]
    ])
    return SYSTEM_PROMPT.format(knowledge_context=knowledge_context)


# ── Chat response via OpenRouter ───────────────────────────────────────────────
def get_medical_response(user_message: str, chat_history: list) -> str:
    client = get_client()
    if not client:
        return "⚠️ Unable to connect to the AI service. Please check your OpenRouter API key."

    # Build message history for the model
    # OpenRouter uses OpenAI-style messages; system prompt goes as first message
    messages = [{"role": "system", "content": build_system_prompt()}]

    for msg in chat_history[-10:]:  # Last 10 messages for context
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model=OPENROUTER_MODEL,
            max_tokens=1000,
            messages=messages,
            extra_headers={
                "HTTP-Referer": "https://mediassist-ai.streamlit.app",  # Optional: your app URL
                "X-Title": "MediAssist AI",                              # Optional: your app name
            }
        )
        return response.choices[0].message.content

    except Exception as e:
        err = str(e).lower()
        if "auth" in err or "401" in err or "api key" in err:
            return "❌ Authentication failed. Please check your OPENROUTER_API_KEY."
        elif "rate" in err or "429" in err:
            return "⏳ Rate limit reached. Please wait a moment and try again."
        elif "model" in err or "404" in err:
            return f"⚠️ Model '{OPENROUTER_MODEL}' not found or unavailable on OpenRouter."
        else:
            return f"⚠️ An error occurred: {str(e)}"


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 0.5rem 0 1rem;'>
        <div style='font-size: 2.5rem;'>🩺</div>
        <div style='font-family: "DM Serif Display", serif; font-size: 1.3rem; 
                    color: #0f4c75; font-weight: 400;'>MediAssist AI</div>
        <div class='status-badge' style='margin: 0.5rem auto; width: fit-content;'>
            <div class='status-dot'></div> Online
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Model info badge
    st.markdown(f"""
    <div style='background:#f0fdf4; border:1px solid #bbf7d0; border-radius:8px;
                padding:0.5rem 0.75rem; font-size:0.75rem; color:#166534;
                text-align:center; margin-bottom:0.75rem;'>
        🤖 Model: <strong>claude-sonnet-4-5</strong><br>
        <span style='opacity:0.7;'>via OpenRouter</span>
    </div>
    """, unsafe_allow_html=True)

    # Session stats
    st.markdown("<div class='sidebar-title'>Session Info</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Messages", st.session_state.conversation_count)
    with col2:
        elapsed = (datetime.now() - st.session_state.session_start).seconds // 60
        st.metric("Minutes", elapsed)

    st.divider()

    # Quick questions
    st.markdown("<div class='sidebar-title'>Quick Questions</div>", unsafe_allow_html=True)
    quick_questions = [
        "💊 Common cold remedies",
        "❤️ Heart disease symptoms",
        "🩸 Diabetes warning signs",
        "🧠 Headache types explained",
        "💉 When to get vaccinated",
        "🌡️ Fever management tips",
        "😴 Improve sleep quality",
        "🥗 Anti-inflammatory foods",
    ]

    for q in quick_questions:
        if st.button(q, key=f"quick_{q}", use_container_width=True):
            st.session_state.pending_question = q.split(" ", 1)[1]

    st.divider()

    # Symptom checker
    st.markdown("<div class='sidebar-title'>Symptom Areas</div>", unsafe_allow_html=True)
    selected_area = st.selectbox(
        "Select body system",
        list(SYMPTOM_CHECKER.keys()),
        label_visibility="collapsed"
    )
    if selected_area and st.button("Check Symptoms", use_container_width=True):
        st.session_state.pending_question = f"What are common symptoms and conditions related to the {selected_area}?"

    st.divider()

    # Emergency info
    st.markdown("""
    <div class='emergency-alert'>
        🚨 <strong>Emergency Numbers</strong><br>
        India: <strong>112</strong> | USA: <strong>911</strong><br>
        UK: <strong>999</strong> | EU: <strong>112</strong><br><br>
        <em>For chest pain, difficulty breathing, or loss of consciousness — call immediately.</em>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Clear chat
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_count = 0
        st.rerun()


# ── Main content ───────────────────────────────────────────────────────────────
# Header
st.markdown("""
<div class='main-header'>
    <h1>🩺 MediAssist AI</h1>
    <p>Your AI-powered medical information companion — always consult a doctor for diagnosis & treatment</p>
</div>
""", unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div class='disclaimer-box'>
    ⚠️ <strong>Medical Disclaimer:</strong> MediAssist AI provides general health information only. 
    It is NOT a substitute for professional medical advice, diagnosis, or treatment. 
    Always seek the advice of your physician or qualified health provider. 
    In case of emergency, call your local emergency services immediately.
</div>
""", unsafe_allow_html=True)

# Chat area
chat_container = st.container()

with chat_container:
    if not st.session_state.messages:
        # Welcome message
        st.markdown("""
        <div class='chat-message assistant-message' style='margin-right:10%'>
            <strong>👋 Welcome to MediAssist AI!</strong><br><br>
            I'm here to help you with medical information and health questions. Here's what I can help with:<br><br>
            🔍 <strong>Symptom information</strong> — understand what symptoms may indicate<br>
            💊 <strong>Medication info</strong> — general information about medicines<br>
            🏥 <strong>Medical conditions</strong> — explanations in plain language<br>
            🥗 <strong>Wellness tips</strong> — nutrition, exercise, preventive care<br>
            📋 <strong>Lab & test info</strong> — what medical tests measure<br><br>
            <em>Remember: I provide information, not diagnosis. Always consult a healthcare professional.</em><br><br>
            <strong>How can I help you today?</strong>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            role = msg["role"]
            content = msg["content"]
            is_emergency = msg.get("emergency", False)

            if role == "user":
                st.markdown(f"""
                <div style='display:flex; justify-content:flex-end; align-items:flex-start; gap:0.6rem; margin:0.5rem 0;'>
                    <div class='chat-message user-message'>{content}</div>
                    <div class='avatar avatar-user'>👤</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                msg_class = "emergency-message" if is_emergency else "assistant-message"
                st.markdown(f"""
                <div style='display:flex; align-items:flex-start; gap:0.6rem; margin:0.5rem 0;'>
                    <div class='avatar avatar-bot'>🩺</div>
                    <div class='chat-message {msg_class}'>{content}</div>
                </div>
                """, unsafe_allow_html=True)

# ── Input area ─────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

col_input, col_btn = st.columns([5, 1])

with col_input:
    user_input = st.text_input(
        "Ask your medical question...",
        key="user_input",
        placeholder="e.g. What are symptoms of high blood pressure?",
        label_visibility="collapsed"
    )

with col_btn:
    send_pressed = st.button("Send 📤", use_container_width=True, type="primary")

# Handle pending question from sidebar quick buttons
if "pending_question" in st.session_state:
    user_input = st.session_state.pending_question
    del st.session_state.pending_question
    send_pressed = True

# ── Process message ────────────────────────────────────────────────────────────
if send_pressed and user_input and user_input.strip():
    question = user_input.strip()
    is_emergency = check_emergency(question)

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })
    st.session_state.conversation_count += 1

    # Show emergency alert immediately if detected
    if is_emergency:
        emergency_prefix = """🚨 **EMERGENCY ALERT** 🚨

Based on your message, this may be a medical emergency. 

**CALL EMERGENCY SERVICES IMMEDIATELY:**
- 🇮🇳 India: **112**
- 🇺🇸 USA/Canada: **911**  
- 🇬🇧 UK: **999**
- 🌍 Europe: **112**

Do NOT wait — time is critical. Here is some general information:

---

"""
        response = emergency_prefix + get_medical_response(question, st.session_state.messages[:-1])
    else:
        with st.spinner("MediAssist is thinking..."):
            response = get_medical_response(question, st.session_state.messages[:-1])

    # Add assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "emergency": is_emergency
    })

    st.rerun()

# ── Feature cards at bottom ────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<p style='text-align:center; color:#64748b; font-size:0.82rem; font-weight:500;'>CAPABILITIES</p>", unsafe_allow_html=True)

feat_cols = st.columns(4)
features = [
    ("🔬", "Symptom Info", "Understand what symptoms may indicate"),
    ("💊", "Medication Guide", "General drug information & interactions"),
    ("🏃", "Wellness Tips", "Lifestyle, diet & preventive health"),
    ("📊", "Health Metrics", "Understand lab results & vitals"),
]
for col, (icon, title, desc) in zip(feat_cols, features):
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size:1.6rem'>{icon}</div>
            <div style='font-weight:600; font-size:0.85rem; color:#0f172a; margin:0.3rem 0'>{title}</div>
            <div style='font-size:0.75rem; color:#64748b'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)