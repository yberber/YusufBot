import streamlit as st
from rag import create_chain, ask

st.set_page_config(page_title="YusufBot", page_icon="🤖")
st.title("YusufBot — Ask me anything about Yusuf")
st.caption("Yusuf is applying for Trainee Data Science in Big Data & Advanced Analytics at Commerzbank")


@st.cache_resource
def load_chain():
    return create_chain()


chain = load_chain()

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
            response = ask(prompt, chain)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
