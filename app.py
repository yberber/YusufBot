import streamlit as st
from rag import create_retriever, ask, GROQ_MODELS

st.set_page_config(page_title="YusufBot", page_icon="🤖", layout="centered")

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    model_labels = {v["label"]: k for k, v in GROQ_MODELS.items()}
    selected_label = st.selectbox("Model", list(model_labels.keys()))
    selected_model = model_labels[selected_label]
    daily_limit = GROQ_MODELS[selected_model]["daily_limit"]

    st.divider()

    st.subheader("📊 Session Token Usage")
    if "session_tokens" not in st.session_state:
        st.session_state.session_tokens = 0
    session_tokens = st.session_state.session_tokens
    st.metric("Tokens used", f"{session_tokens:,}")
    st.caption(f"Daily limit ({selected_label}): {daily_limit:,}")
    st.progress(min(session_tokens / daily_limit, 1.0))

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

if prompt := st.chat_input("Ask me anything about Yusuf..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response, usage = ask(prompt, selected_model, retriever)
                st.session_state.session_tokens += usage["total_tokens"]
            except Exception:
                response = "Sorry, I ran into an issue answering that. Please try again."
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
