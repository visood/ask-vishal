# Ask Vishal

A conversational CV powered by Claude. Instead of reading a static resume, visitors talk to an AI colleague who knows Vishal Sood's work deeply — his projects, publications, career transitions, and technical expertise.

## Features

- **Professional identity selector** — frame the conversation for Research Engineer, Software Engineer, Quant Engineer, Genomics/Comp Bio, or Research Software Engineer roles
- **Job description matching** — paste a job description or provide a URL, then ask how Vishal fits the role
- **Grounded answers** — every claim is backed by actual portfolio content (projects, publications, code)
- **Free tier** — 5 questions per session, powered by Claude Haiku

## Run locally

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"
streamlit run app.py
```

Or put your key in `.streamlit/secrets.toml`:

```toml
ANTHROPIC_API_KEY = "your-key-here"
```

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect the repo, set `app.py` as the main file
4. Add `ANTHROPIC_API_KEY` in the Secrets section
5. Deploy

## How it works

The app loads `context.txt` — a pre-assembled document containing Vishal's full professional portfolio (identity, expertise, experience, publications, project deep-dives). This content is injected into the system prompt as grounding context. At ~80K tokens, the entire corpus fits in Claude's context window without needing RAG.

The system prompt establishes the "Knowledgeable Colleague" stance: an AI that speaks from thorough knowledge of Vishal's work, maintains thesis-proof structure (claim + evidence), and adapts emphasis to the visitor's interest.
