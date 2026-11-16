# .\.venv\Scripts\Activate.ps1
# streamlit run app.py

# Find architecture diagrams.
# Show images related to artificial intelligence.
# What is Artificial Intelligence according to NVIDIA's annual report?
# Summarize NVIDIA's view of AI infrastructure.
# What is the five-layer AI stack mentioned by NVIDIA?
# Show diagrams related to governance.

# ================================================================================
import os
import json
import uuid
import streamlit as st

from agent.agent_loop import run_agent
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")
print("ENV FILE:", BASE_DIR / ".env")
print("KEY FOUND:", os.getenv("GROQ_API_KEY"))
# ================================================================================
# CONFIG
# ================================================================================

st.set_page_config(
    page_title="Agentic Multimodal RAG",
    page_icon="🤖",
    layout="wide"
)

# ================================================================================
# CSS
# ================================================================================

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
}

[data-testid="stImage"] img{
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

# ================================================================================
# CHAT STORAGE
# ================================================================================

CHAT_DIR = "conversations"

os.makedirs(
    CHAT_DIR,
    exist_ok=True
)

# ================================================================================
# STATE
# ================================================================================

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# ================================================================================
# HELPERS
# ================================================================================

def save_chat():
    
    if not st.session_state.current_chat:
        return

    title = "New Chat"

    # First user message becomes title
    for msg in st.session_state.messages:

        if msg["role"] == "user":

            title = msg["content"]

            break

    data = {
        "title": title,
        "messages": st.session_state.messages
    }

    filepath = os.path.join(
        CHAT_DIR,
        st.session_state.current_chat
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )

def load_chat(chat_file):
    
    filepath = os.path.join(
        CHAT_DIR,
        chat_file
    )

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    st.session_state.messages = data["messages"]

    st.session_state.current_chat = chat_file


def new_chat():

    chat_id = f"{uuid.uuid4().hex[:8]}.json"

    st.session_state.current_chat = chat_id

    st.session_state.messages = []

    save_chat()

# ================================================================================
# SIDEBAR
# ================================================================================

with st.sidebar:

    st.title("💬 Conversations")

    if st.button(
        "➕ New Chat",
        use_container_width=True
    ):
        new_chat()
        st.rerun()

    st.divider()

    chat_files = sorted(
        os.listdir(CHAT_DIR),
        reverse=True
    )

    for chat in chat_files:
    
        chat_path = os.path.join(
            CHAT_DIR,
            chat
        )

        try:

            with open(
                chat_path,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            title = data.get(
                "title",
                chat.replace(".json", "")
            )

        except Exception:

            title = chat.replace(
                ".json",
                ""
            )

        # Small title truncation
        if len(title) > 35:

            title = title[:35] + "..."

        col1, col2 = st.columns(
            [5, 1]
        )

        with col1:

            if st.button(
                f"📄 {title}",
                key=f"load_{chat}",
                use_container_width=True
            ):

                load_chat(chat)

                st.rerun()

        with col2:

            if st.button(
                "🗑",
                key=f"delete_{chat}"
            ):

                os.remove(chat_path)

                if (
                    st.session_state.current_chat
                    == chat
                ):

                    st.session_state.current_chat = None

                    st.session_state.messages = []

                st.rerun()
                

    st.divider()

    st.subheader("🤖 Agent Status")

    st.success(
        "Text Vector DB Ready"
    )

    st.success(
        "Image Vector DB Ready"
    )

    st.success(
        "Planner Agent Active"
    )

    st.success(
        "Reflection Agent Active"
    )

    st.divider()

    st.markdown("""
### Models

✅ MiniLM-L6-v2

✅ CLIP ViT-B/32

✅ BLIP

✅ GPT OSS 120B
""")

# ================================================================================
# HEADER
# ================================================================================

st.title(
    "🤖 Agentic Multimodal RAG"
)

st.caption(
    "Planner Agent • Reflection Agent • CLIP Retrieval • BLIP Captioning"
)

# ================================================================================
# LOAD ALL MESSAGES
# ================================================================================

for msg in st.session_state.messages:

    with st.chat_message(
        msg["role"]
    ):

        st.markdown(
            msg["content"]
        )

        if (
            msg["role"] == "assistant"
            and "images" in msg
        ):

            cols = st.columns(2)

            for i, img in enumerate(
                msg["images"]
            ):

                with cols[i % 2]:

                    if os.path.exists(
                        img["path"]
                    ):

                        st.image(
                            img["path"],
                            use_container_width=True
                        )

                        st.caption(
                            img["caption"]
                        )

# ================================================================================
# INPUT
# ================================================================================

query = st.chat_input(
    "Ask a question..."
)

# ================================================================================
# CHAT PROCESSING
# ================================================================================

if query:

    if not st.session_state.current_chat:
        new_chat()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message(
        "user"
    ):
        st.markdown(query)

    with st.spinner(
        "Agent is reasoning..."
    ):

        response = run_agent(
            query,
            os.getenv(
                "GROQ_API_KEY"
            )
        )

    with st.chat_message(
        "assistant"
    ):

        if response["images"]:

            st.markdown(
                "### 🖼 Retrieved Visual Evidence"
            )

            cols = st.columns(2)

            for i, img in enumerate(
                response["images"]
            ):

                with cols[i % 2]:

                    if os.path.exists(
                        img["path"]
                    ):

                        st.image(
                            img["path"],
                            use_container_width=True
                        )

                        st.caption(
                            img["caption"]
                        )

        st.markdown("---")

        st.markdown(
            "### 📖 Analysis"
        )

        st.markdown(
            response["answer"]
        )

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":response["answer"],
            "images":response["images"]
        }
    )

    save_chat()

    st.rerun()