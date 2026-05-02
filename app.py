import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import streamlit as st
from rag import create_retriever, ask, GROQ_MODELS
from usage_tracker import load_daily_tokens, add_tokens

st.set_page_config(page_title="YusufBot", page_icon="🤖", layout="centered")

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    model_labels = {v["label"]: k for k, v in GROQ_MODELS.items()}
    selected_label = st.selectbox("Model", list(model_labels.keys()))
    selected_model = model_labels[selected_label]
    daily_limit = GROQ_MODELS[selected_model]["daily_limit"]

    st.divider()

    st.subheader("📊 Daily Token Usage")
    daily_tokens = load_daily_tokens()
    st.metric("Tokens used today", f"{daily_tokens:,}")
    st.caption(f"Daily limit ({selected_label}): {daily_limit:,} · resets at midnight UTC")
    st.progress(min(daily_tokens / daily_limit, 1.0))

    st.divider()

    st.markdown(
        "[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)]"
        "(https://www.linkedin.com/in/yusuf-sancar-berber-66b7a7353/)  "
        "[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)]"
        "(https://github.com/yberber)"
    )

# ── Main ─────────────────────────────────────────────────────────────────────
st.title("YusufBot — Ask me anything about Yusuf")
st.caption("Yusuf is applying for Trainee Data Science in Big Data & Advanced Analytics at Commerzbank")


@st.cache_resource
def load_retriever():
    return create_retriever()


retriever = load_retriever()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and message.get("tokens"):
            st.caption(f"🔢 {message['tokens']:,} tokens used for this message")

if prompt := st.chat_input("Ask me anything about Yusuf..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response, usage = ask(prompt, selected_model, retriever)
                tokens = usage["total_tokens"]
                add_tokens(tokens)
            except Exception:
                response = "Sorry, I ran into an issue answering that. Please try again."
                tokens = 0
        st.markdown(response)
        if tokens:
            st.caption(f"🔢 {tokens:,} tokens used for this message")

    st.session_state.messages.append({"role": "assistant", "content": response, "tokens": tokens})
    st.rerun()
