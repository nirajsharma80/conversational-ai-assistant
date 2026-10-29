# Careline — Conversational Support Copilot

A context-aware support assistant built with Streamlit and Google's Gemini SDK. It keeps the current conversation in Streamlit session state and exports a Markdown transcript.

## Requirements

- Python 3.11–3.15
- A Google AI Studio API key to generate Gemini replies

## Run in VS Code

1. Open this repository in VS Code and select the project interpreter. The checked-in workspace settings point to `.venv-vscode` on Windows.
2. In a new PowerShell terminal, create the environment and install dependencies:

   ```powershell
   python -m venv .venv-vscode
   .\.venv-vscode\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. Set the API key for this terminal session and launch the app:

   ```powershell
   $env:GOOGLE_API_KEY = "your-key"
   .\.venv-vscode\Scripts\python.exe -m streamlit run app.py
   ```

The app opens without an API key so you can inspect the interface. Gemini replies require a valid `GOOGLE_API_KEY`; never commit real credentials.

## Design and safety

- Only the latest 12 messages are sent to Gemini for each reply.
- Chat history stays in Streamlit session state and is not written to a database.
- The default support policy tells the assistant not to invent account details or approve refunds. No account or ticketing system is connected.
- Treat output as a draft. Verify policy-specific or account-specific claims in an authorized system before acting.
- Provider API usage is subject to your Google account's terms and billing.

## Stack

Python · Streamlit · Google Gen AI SDK · Gemini

## License

MIT. See [LICENSE](LICENSE).
