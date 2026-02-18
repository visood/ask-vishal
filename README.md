# le comptoir

**An AI-powered career platform for professionals in transition.**

*le comptoir* gives each job seeker a personal AI agent that knows their work deeply. Instead of sending a flat CV, candidates share a link where recruiters and hiring managers can have a real conversation — asking questions, exploring fit, getting honest, evidence-backed answers.

Built in Switzerland. Trilingual (EN/FR/DE). Designed for ORP/RAV career transition programs.

**Live demo:** [ask-physicist-vishal.streamlit.app](https://ask-physicist-vishal.streamlit.app/)

---

## The problem

Career transition is hard. The tools haven't changed in decades: a CV, a cover letter, a LinkedIn profile. Everyone looks the same on paper — especially professionals switching domains, where their real strengths don't map neatly to keyword filters.

Coaching programs like LHH do excellent work on positioning, storytelling, and strategy. But the *delivery mechanism* is still a static document that gets six seconds of a recruiter's attention.

## The solution

*le comptoir* turns a candidate's entire professional story into a live, conversational experience:

- A recruiter pastes a job description and asks *"how does this person fit?"* — and gets a specific, honest analysis with evidence
- A hiring manager asks *"what did they actually build?"* — and gets project details, not bullet points
- The candidate's positioning adapts in real time to the visitor's interest: the same person is framed differently for a quant role vs. a research role vs. a biotech role

Every answer is grounded in the candidate's actual portfolio. The AI doesn't invent — it synthesizes and narrates from verified content.

### What's included

- **Conversational Q&A** grounded in the candidate's portfolio
- **Professional identity selector** — reframe experience for different role types
- **Job description matching** — paste a posting, get a fit analysis from recruiter and hiring manager perspectives
- **Marketing plan** (plan de recherche d'emploi) — ORP-compliant, viewable online and downloadable as PDF
- **Trilingual** — the agent responds in English, French, or German
- **Tiered access** — free preview questions, then extended access via passcode

---

## For coaches and program managers

### Why this matters for your participants

Every person in a career transition program has a richer story than their CV tells. *le comptoir* lets that story come through in a way that's engaging for recruiters and differentiated from every other applicant.

Participants contribute their content — the same material they develop during coaching (positioning statement, competency domains, target market, action plan). The technology handles the rest.

### Why this matters for LHH

- **Differentiation**: No other outplacement firm offers AI-powered candidate portfolios
- **Scalability**: One deployment serves an entire cohort. Each new participant adds their content — no per-person technical setup
- **Measurability**: Track which candidates get engagement, which questions recruiters ask, what roles generate interest
- **Innovation signal**: Demonstrates that LHH is at the leading edge of career transition methodology
- **Cost**: Effectively zero. Hosting is free (Streamlit Community Cloud). AI costs are ~CHF 0.001 per conversation. A full cohort runs for months on CHF 50 of API credit.

### The collective model

Rather than each person deploying individually, the program runs a single *le comptoir* instance for the cohort:

- **Landing page** with a roster of all participants — recruiters browse and pick who to talk to
- **Each participant** has their own AI agent, trained on their specific portfolio
- **The coach or program manager** maintains the deployment — participants only contribute content
- **Recruiters** get one link to an entire pool of vetted, well-positioned professionals

This flips the dynamic: instead of 15 people sending 15 CVs into the void, you present a curated collective. *"Here are our professionals — talk to any of them."*

### What participants need to provide

The same material they already develop during coaching:

1. **Portfolio content** (a narrative document, 2-5 pages): who they are, what they've built, key projects, expertise areas, career transitions, publications or credentials
2. **Marketing plan** (plan de recherche): positioning statement, competency domains, target market, target companies, action plan
3. **Role variants** (optional): 2-3 ways to frame their experience for different types of roles

No technical skills required. Content can be provided as a Word document, Google Doc, or plain text. One technical person assembles it into the platform.

---

## For individuals (self-service deployment)

If you want to deploy your own *le comptoir* independently, everything happens in your browser. No coding, no terminal.

### You will need

- A GitHub account (free) — [github.com](https://github.com)
- An Anthropic API key (~CHF 5 credit lasts months) — [console.anthropic.com](https://console.anthropic.com)
- A Streamlit Community Cloud account (free) — [share.streamlit.io](https://share.streamlit.io)

### Steps

**1. Get an API key**

Sign up at [console.anthropic.com](https://console.anthropic.com). Go to Settings > API Keys, create a key, copy it. Add CHF 5 of credit under Settings > Billing.

**2. Fork the repository**

Go to [github.com/visood/ask-vishal](https://github.com/visood/ask-vishal) and click **Fork** (top right). This creates your own copy.

**3. Edit your content**

In your forked repo on GitHub, click any file, then the pencil icon to edit:

| File | What to change |
|------|---------------|
| `context.txt` | Replace with your professional portfolio (this is everything the AI knows about you) |
| `marketing_plan.py` | Replace the plan text in the `PLAN` dictionary with your own marketing plan |
| `app.py` | Change `"Vishal Sood"` to your name; edit the `IDENTITIES` dictionary for your role variants |

**4. Deploy**

Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub, click **New app**, select your fork, set `app.py` as the main file. In **Advanced settings**, paste:

```toml
ANTHROPIC_API_KEY = "your-key-here"
PASSCODES = "any-codes,you-want"
```

Click **Deploy**. Live in 2 minutes.

**5. Share your link**

Add it to your LinkedIn, email signature, and application materials. It works 24/7.

---

## How it works

The candidate's professional content is assembled into a single document (`context.txt`). This is injected into the AI's system prompt as grounding context — everything it knows comes from this document. The AI is instructed to be precise, cite specific projects, acknowledge gaps honestly, and adapt its framing to the visitor's interest.

At up to ~80,000 tokens of context, the entire portfolio fits in Claude's context window without needing databases or search infrastructure. The whole system is five Python files and a text file.

### Costs

| Component | Cost |
|-----------|------|
| Streamlit Cloud hosting | Free |
| GitHub repository | Free |
| Anthropic API (Claude Haiku) | ~CHF 0.001 per question |
| Total for a cohort of 15, running 6 months | ~CHF 50 |

---

*le comptoir* — built in Switzerland, for people in transition.
