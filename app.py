import streamlit as st

from src.chatbot import get_ai_response


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS — DEEP VIOLET / INDIGO THEME
# (Colors here match .streamlit/config.toml exactly, so the
# native Streamlit chrome — top bar, chat input — blends in
# instead of showing white/black.)
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       GLOBAL
    -------------------------------------------------------- */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(167, 139, 250, 0.16),
                transparent 32%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(244, 114, 182, 0.14),
                transparent 30%
            ),
            #1e1b4b;
    }

    .main .block-container {
        max-width: 950px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* --------------------------------------------------------
       HERO
    -------------------------------------------------------- */

    .hero {
        padding: 1.5rem 2rem;
        border-radius: 24px;
        margin-bottom: 1.4rem;

        background:
            linear-gradient(
                135deg,
                #4f46e5,
                #9333ea,
                #db2777
            );

        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 20px 55px rgba(30, 27, 75, 0.55);
    }

    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        color: #ffffff;
    }

    .hero-subtitle {
        margin-top: 0.5rem;
        font-size: 1rem;
        color: #ede9fe;
    }

    /* --------------------------------------------------------
       CHAT BUBBLES
    -------------------------------------------------------- */

    div[data-testid="stChatMessage"] {
        background: #2a2464;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 18px;
        box-shadow: 0 10px 28px rgba(30, 27, 75, 0.35);
        padding: 0.6rem 0.4rem;
        margin-bottom: 0.7rem;
    }

    div[data-testid="stChatMessage"] p {
        color: #f5f3ff;
    }

    /* --------------------------------------------------------
       BUTTONS
    -------------------------------------------------------- */

    .stButton > button {
        width: 100%;
        border-radius: 14px;
        border: none;
        padding: 0.7rem 1rem;
        font-weight: 700;

        background:
            linear-gradient(
                90deg,
                #6366f1,
                #a855f7,
                #ec4899
            );

        color: white;
        transition: all 0.2s ease;
        box-shadow: 0 8px 22px rgba(147, 51, 234, 0.35);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(147, 51, 234, 0.45);
    }

    /* --------------------------------------------------------
       CHAT INPUT
    -------------------------------------------------------- */

    .stChatInput, .stChatInput textarea, .stChatInput input {
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.14) !important;
        background: #2a2464 !important;
        color: #f5f3ff !important;
    }

    [data-testid="stBottom"] {
        background: #1e1b4b !important;
    }

    /* --------------------------------------------------------
       SIDEBAR
    -------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #211d54, #1e1b4b);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    .sidebar-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .sidebar-card p {
        color: #cbd0e8;
        font-size: 0.88rem;
        margin: 0;
    }

    /* --------------------------------------------------------
       TOP TOOLBAR
    -------------------------------------------------------- */

    header[data-testid="stHeader"] {
        background: #1e1b4b;
    }

    /* --------------------------------------------------------
       FOOTER
    -------------------------------------------------------- */

    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255,255,255,0.08);
        color: #a5aad0;
        font-size: 0.85rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

AVATARS = {
    "user": "🧑‍💻",
    "assistant": "🤖",
}


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 💬 AI Chatbot")

    st.markdown(
        '<div class="sidebar-card">'
        '<p>A conversational AI assistant that remembers '
        'everything said earlier in the chat, so you can ask '
        'natural follow-up questions.</p>'
        '</div>',
        unsafe_allow_html=True
    )

    new_chat_button = st.button(
        "🧹 Start a New Conversation",
        use_container_width=True
    )

    if new_chat_button:
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown(
        f'<div class="sidebar-card">'
        f'<p>💬 <strong>{len(st.session_state.messages)}</strong> '
        f'messages in this conversation</p>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.caption("⚡ Powered by Groq — fast, free-tier LLM inference.")


# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="hero">'
    '<div class="hero-title">💬 AI Chatbot</div>'
    '<div class="hero-subtitle">Your intelligent assistant — ask questions, brainstorm ideas, or just chat. I keep track of our conversation as we go.</div>'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar=AVATARS.get(message["role"])
    ):
        st.markdown(message["content"])


# ============================================================
# EMPTY STATE
# ============================================================

if not st.session_state.messages:

    st.markdown(
        '<div class="sidebar-card" style="text-align:center; padding: 2rem;">'
        '<p style="font-size: 1.05rem;">👋 <strong>Say hello to get started!</strong><br>'
        'I\'ll remember everything we discuss, so feel free to '
        'ask follow-up questions.</p>'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input("Type your message here...")

if user_input:

    # ------------------------------------------------------------
    # Show and store the user's message
    # ------------------------------------------------------------

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user", avatar=AVATARS["user"]):
        st.markdown(user_input)

    # ------------------------------------------------------------
    # Get and show the AI's response
    # ------------------------------------------------------------

    with st.chat_message("assistant", avatar=AVATARS["assistant"]):

        with st.spinner("Thinking..."):

            try:

                reply = get_ai_response(
                    st.session_state.messages
                )

                st.markdown(reply)

                st.session_state.messages.append(
                    {"role": "assistant", "content": reply}
                )

            except Exception as error:

                error_message = (
                    "⚠️ Sorry, something went wrong while "
                    f"contacting the AI: {error}"
                )

                st.error(error_message)

                # Remove the user's last message so the failed
                # exchange doesn't stay stuck in the conversation.
                st.session_state.messages.pop()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        💬 AI Chatbot
        <br>
        Built with Streamlit and the Groq API
    </div>
    """,
    unsafe_allow_html=True
)