import os
import hashlib
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import groq as groq_lib
import streamlit as st
from rag import create_retriever, ask, GROQ_MODELS
from usage_tracker import load_daily_tokens, add_tokens
from audio import transcribe, synthesize, STT_MODELS, TTS_VOICES

import transformers
transformers.logging.set_verbosity_error()

st.set_page_config(page_title="YusufBot", page_icon="🤖", layout="centered")

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    model_labels = {v["label"]: k for k, v in GROQ_MODELS.items()}
    selected_label = st.selectbox("LLM Model", list(model_labels.keys()))
    selected_model = model_labels[selected_label]
    daily_limit = GROQ_MODELS[selected_model]["daily_limit"]

    st.divider()

    st.subheader("🎙️ Voice")
    stt_labels = {v: k for k, v in STT_MODELS.items()}
    selected_stt_label = st.selectbox("Speech-to-Text", list(stt_labels.keys()))
    selected_stt = stt_labels[selected_stt_label]
    selected_voice = st.selectbox("TTS Voice", TTS_VOICES)

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
if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None
if "show_mic" not in st.session_state:
    st.session_state.show_mic = False

# ── Chat history ─────────────────────────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            has_tokens = bool(message.get("tokens"))
            has_audio = message.get("audio") is not None
            if has_tokens or has_audio:
                cap_col, play_col = st.columns([5, 2])
                with cap_col:
                    if has_tokens:
                        st.caption(f"🔢 {message['tokens']:,} tokens used for this message")
                with play_col:
                    if has_audio:
                        st.audio(message["audio"], format="audio/wav")

# ── Input area ───────────────────────────────────────────────────────────────
prompt = None

# Small mic toggle — sits just above the sticky chat input bar
mic_col, _ = st.columns([1, 10])
with mic_col:
    mic_label = "🔴" if st.session_state.show_mic else "🎤"
    if st.button(mic_label, help="Toggle voice input", key="mic_toggle"):
        st.session_state.show_mic = not st.session_state.show_mic

if st.session_state.show_mic:
    audio_input = st.audio_input("Record your question", label_visibility="collapsed")
    if audio_input:
        raw = audio_input.read()
        audio_hash = hashlib.md5(raw).hexdigest()
        if audio_hash != st.session_state.last_audio_hash:
            st.session_state.last_audio_hash = audio_hash
            with st.spinner("Transcribing..."):
                try:
                    prompt = transcribe(raw, audio_input.name or "audio.webm", selected_stt)
                    st.info(f"🎤 *Transcribed:* {prompt}")
                except groq_lib.RateLimitError:
                    st.warning("⚠️ Speech-to-text rate limit reached. Please type your question or wait a moment.")
                except Exception:
                    st.error("⚠️ Could not transcribe audio. Please try again.")

text_prompt = st.chat_input("Or type your question...")
if text_prompt:
    prompt = text_prompt

# ── Process prompt ───────────────────────────────────────────────────────────
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    audio_response = None
    tts_warning = None

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

        with st.spinner("Generating audio..."):
            try:
                audio_response = synthesize(response, selected_voice)
            except groq_lib.RateLimitError:
                tts_warning = "⚠️ TTS rate limit reached — no audio for this response"
            except Exception as e:
                tts_warning = f"⚠️ TTS error: {e}"

        cap_col, play_col = st.columns([5, 2])
        with cap_col:
            caption_parts = []
            if tokens:
                caption_parts.append(f"🔢 {tokens:,} tokens used for this message")
            if tts_warning:
                caption_parts.append(tts_warning)
            if caption_parts:
                st.caption(" · ".join(caption_parts))
        with play_col:
            if audio_response:
                st.audio(audio_response, format="audio/wav")

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "tokens": tokens,
        "audio": audio_response,
    })
    st.rerun()
