import os

import streamlit as st

from assistant import get_reply

st.set_page_config(
    page_title="Careline | Support copilot",
    page_icon="◌",
    layout="centered",
)
st.title("◌ Careline")
st.caption("A support copilot that keeps conversation context and makes uncertainty visible.")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("Assistant settings")
    model = st.text_input("Gemini model", value="gemini-2.5-flash").strip()
    instructions = st.text_area(
        "Support policy",
        value=(
            "You are a helpful support assistant. Be clear and kind. Never invent account "
            "details, policy terms, or refund approvals. When a request needs account access "
            "or human judgment, explain the next step and recommend a human agent."
        ),
        height=170,
    ).strip()
    has_api_key = bool(os.getenv("GOOGLE_API_KEY"))
    if has_api_key:
        st.caption("Gemini is configured with GOOGLE_API_KEY.")
    else:
        st.info("Set GOOGLE_API_KEY in the VS Code terminal to enable Gemini replies.")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

query = st.chat_input("How can I help?")
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        if not has_api_key:
            st.warning("Set GOOGLE_API_KEY in the VS Code terminal, then restart Careline.")
        else:
            with st.spinner("Writing a response..."):
                try:
                    answer = get_reply(
                        history=st.session_state.messages,
                        instructions=instructions,
                        model=model,
                        api_key=os.environ["GOOGLE_API_KEY"],
                    )
                except Exception as exc:
                    answer = f"The Gemini request failed: {exc}"
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

if st.session_state.messages:
    transcript = "\n\n".join(
        f"**{message['role'].title()}:** {message['content']}"
        for message in st.session_state.messages
    )
    st.download_button(
        "Export transcript",
        transcript,
        file_name="careline-transcript.md",
        mime="text/markdown",
    )
