import os
import streamlit as st
from assistant import get_reply

st.set_page_config(page_title="Careline | Support copilot",page_icon="◌",layout="centered")
st.title("◌ Careline")
st.caption("A support copilot that keeps conversation context and makes uncertainty visible.")
with st.sidebar:
    st.subheader("Assistant settings")
    model=st.text_input("Gemini model",value="gemini-2.5-flash")
    instructions=st.text_area("Support policy",value="You are a helpful support assistant. Be clear and kind. Never invent account details, policy terms, or refund approvals. When a request needs account access or human judgment, explain the next step and recommend a human agent.",height=170)
    st.caption("Provide GOOGLE_API_KEY in the environment to enable replies.")
    if st.button("Clear conversation"): st.session_state.messages=[]; st.rerun()
if "messages" not in st.session_state: st.session_state.messages=[]
for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.markdown(message["content"])
query=st.chat_input("How can I help?")
if query:
    st.session_state.messages.append({"role":"user","content":query})
    with st.chat_message("user"): st.markdown(query)
    with st.chat_message("assistant"):
        if not os.getenv("GOOGLE_API_KEY"): st.error("Set GOOGLE_API_KEY in your environment to enable the assistant.")
        else:
            with st.spinner("Writing a response..."):
                try: answer=get_reply(st.session_state.messages,instructions,model)
                except Exception as exc: answer=f"The model request failed: {exc}"
            st.markdown(answer)
            st.session_state.messages.append({"role":"assistant","content":answer})
if st.session_state.messages:
    transcript="\n\n".join(f"**{m['role'].title()}:** {m['content']}" for m in st.session_state.messages)
    st.download_button("Export transcript",transcript,file_name="careline-transcript.md",mime="text/markdown")
