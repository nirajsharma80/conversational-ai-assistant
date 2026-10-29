import os

import streamlit as st
from google.genai import errors

from assistant import get_reply_stream

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
    model = st.selectbox(
        "Gemini model",
        options=("gemini-3.5-flash-lite", "gemini-3.8-flash"),
        key="gemini_model_select_v1",
    )
    st.caption("Flash-Lite is selected by default for faster replies.")
    instructions = st.text_area(
        "Support policy",
        value=(
            "You are a helpful support assistant. Be clear and kind. Never invent account "
            "details, policy terms, or refund approvals. When a request needs account access "
            "or human judgment, explain the next step and recommend a human agent."
        ),
        height=170,
    ).strip()
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
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
        if not api_key:
            st.warning("Set GOOGLE_API_KEY in the VS Code terminal, then restart Careline.")
        else:
            response_status = st.status("Waiting for Gemini...", expanded=False)
            try:
                answer = st.write_stream(
                    get_reply_stream(
                        history=st.session_state.messages,
                        instructions=instructions,
                        model=model,
                        api_key=api_key,
                    )
                )
            except Exception as exc:
                response_status.update(
                    label="Gemini request failed",
                    state="error",
                    expanded=True,
                )
                if isinstance(exc, errors.APIError) and exc.code == 503:
                    answer = (
                        "Gemini is temporarily busy. Please wait a moment and try again."
                    )
                elif isinstance(exc, errors.APIError) and exc.code == 404:
                    answer = (
                        f"Gemini model `{model}` is unavailable for this API key. "
                        "Change the Gemini model setting to `gemini-3.8-flash` and retry."
                    )
                elif "timed out" in str(exc).lower():
                    answer = (
                        "Gemini did not respond before the 120-second timeout. "
                        "Try again shortly or choose Gemini 3.5 Flash-Lite."
                    )
                else:
                    answer = f"The Gemini request failed: {exc}"
                st.error(answer)
            else:
                response_status.update(
                    label="Response received",
                    state="complete",
                    expanded=False,
                )
            if not answer:
                answer = "I couldn’t generate a text response. Please try again."
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
