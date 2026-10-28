# Careline — Conversational Support Copilot

A simple, context-aware support assistant built with LangChain, Gemini, and Streamlit. It remembers the current session's recent messages, lets you tailor its support policy, and exports a Markdown transcript.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Set `GOOGLE_API_KEY` in your shell, then run:

```bash
streamlit run app.py
```

## Design and safety

- Only the latest 12 messages are sent to the selected Gemini model on each turn.
- Chat history is held in Streamlit session state; it is not written to a database by this app.
- The default support policy tells the assistant not to invent account information or approve refunds. No account or ticketing system is connected.
- Treat output as a draft: verify policy-specific or account-specific claims with an authorized system before acting.
- Provider API usage is subject to your Google account's terms and billing.

## Stack

Python · Streamlit · LangChain Core · Google Gemini

## License

MIT. See [LICENSE](LICENSE).
