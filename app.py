"""The Knowledgeable Colleague — Streamlit chat interface.

A conversational CV where visitors talk to an AI that knows Vishal Sood's work deeply.
Features:
  - Professional identity selector (adapt framing to role type)
  - Job description matching (paste text or URL, get a fit analysis)
  - Conversational Q&A grounded in portfolio content

Usage:
    streamlit run app.py
"""
import streamlit as st
import anthropic
import requests
import re
from pathlib import Path

from prompt import build_system_prompt


# --- Configuration ---
MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 1024
MAX_MESSAGES_PER_SESSION = 5
CONTEXT_FILE = Path(__file__).parent / "context.txt"

# Professional identity variants: (label, title, summary)
IDENTITIES = {
    "Research Engineer": (
        "Senior Research Engineer",
        "A Senior Research Engineer with a PhD in Physics and extensive experience "
        "building robust, scalable computational tools that accelerate scientific "
        "discovery. Proven ability to translate complex research requirements — from "
        "neuroscience to genomics — into production-grade software platforms.",
    ),
    "Software Engineer": (
        "Senior Software Developer",
        "A Systems Architect and Senior Engineer with a proven track record of "
        "designing and building robust, scalable platforms for data-intensive "
        "applications. Combines deep, first-principles expertise in statistical "
        "modeling and algorithms from a PhD in Physics with hands-on experience "
        "engineering high-performance backends (C++, Python) and complex workflow "
        "engines for distributed systems.",
    ),
    "Quant Engineer": (
        "Senior Quantitative Research Engineer",
        "A first-principles thinker with a PhD in Statistical Physics and over a "
        "decade of experience architecting high-performance computational ecosystems. "
        "Proven ability to translate the complex stochastic systems underlying "
        "financial derivatives into robust, low-latency C++ applications and scalable "
        "Python validation pipelines.",
    ),
    "Genomics / Comp Bio": (
        "Senior Research Engineer / Computational Biology Specialist",
        "A Senior Research Engineer with extensive experience developing "
        "high-performance bioinformatics pipelines and clinical-grade software. "
        "Specialized in architecting scalable C++ / Python solutions for processing "
        "complex biological data, from large-scale genomics to multi-terabyte "
        "scientific simulations.",
    ),
    "Research Software Engineer": (
        "Senior Research Software Developer",
        "Senior research software developer (PhD, Statistical Physics) building "
        "Python-first research platforms, complex workflow engines, data pipelines, "
        "and analysis/visualization tooling used by front-office/bench scientists. "
        "Expert in turning large, heterogeneous datasets into fast, reproducible insights.",
    ),
}

DEFAULT_IDENTITY = "Research Engineer"


# --- Page config ---
st.set_page_config(
    page_title="Vishal Sood — The Knowledgeable Colleague",
    page_icon="🔬",
    layout="centered",
)


# --- Cached resources ---
@st.cache_resource
def get_base_content():
    """Load pre-assembled portfolio content (cached — done once)."""
    return CONTEXT_FILE.read_text(encoding="utf-8")


@st.cache_resource
def get_client():
    """Create Anthropic client (cached)."""
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
        return anthropic.Anthropic(api_key=api_key)
    except (FileNotFoundError, KeyError):
        return anthropic.Anthropic()


def get_system_prompt(identity_key: str, job_description: str = "") -> str:
    """Build system prompt with identity framing and optional job context."""
    content = get_base_content()
    title, summary = IDENTITIES[identity_key]

    identity_block = (
        f"\n\n--- Active Professional Identity ---\n\n"
        f"Title: {title}\n"
        f"Summary: {summary}\n\n"
        f"When discussing Vishal's work, lead with this framing. "
        f"Emphasize the aspects of his experience most relevant to a "
        f'"{title}" positioning.\n'
    )

    job_block = ""
    if job_description:
        job_block = (
            f"\n\n--- Job Description Under Evaluation ---\n\n"
            f"{job_description}\n\n"
            f"A recruiter or hiring manager has provided this job description. "
            f"When the visitor asks about fit or match, analyze it using these lenses:\n"
            f"1. The recruiter's filter: Does this candidate survive a 6-second scan "
            f"for this role? What jumps out immediately?\n"
            f"2. The hiring manager's filter: Does the candidate's experience map onto "
            f"problems this role actually faces? Be specific.\n"
            f"3. The honest broker: Where is the alignment strong? Where are gaps? "
            f"Name gaps directly — the candidate can decide how to address them.\n"
            f"4. Domain bridging: Where the candidate's experience is in a different "
            f"domain but structurally similar, make the translation explicit.\n"
        )

    return build_system_prompt(content + identity_block + job_block)


def fetch_url_text(url: str) -> str:
    """Fetch a URL and extract readable text."""
    try:
        resp = requests.get(url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (compatible; KnowledgeableColleague/1.0)"
        })
        resp.raise_for_status()
        # Strip HTML tags for a rough text extraction
        text = re.sub(r'<script[^>]*>.*?</script>', '', resp.text, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:10000]  # cap at ~10K chars to stay within budget
    except Exception as e:
        return f"[Could not fetch URL: {e}]"


# --- Sidebar ---
with st.sidebar:
    st.title("Vishal Sood")

    # Identity selector
    identity = st.selectbox(
        "Professional identity",
        options=list(IDENTITIES.keys()),
        index=list(IDENTITIES.keys()).index(DEFAULT_IDENTITY),
        help="Changes how the Colleague frames Vishal's experience",
    )
    title, summary = IDENTITIES[identity]
    st.caption(title)

    st.divider()

    # Job description input
    st.markdown("**Match against a job**")
    job_input_method = st.radio(
        "Provide job description via:",
        ["None", "Paste text", "URL"],
        index=0,
        label_visibility="collapsed",
    )

    job_description = ""
    if job_input_method == "Paste text":
        job_description = st.text_area(
            "Job description",
            height=150,
            placeholder="Paste the job description here...",
        )
    elif job_input_method == "URL":
        job_url = st.text_input("Job posting URL", placeholder="https://...")
        if job_url:
            with st.spinner("Fetching..."):
                job_description = fetch_url_text(job_url)
            if job_description.startswith("[Could not"):
                st.warning(job_description)
                job_description = ""
            else:
                st.success(f"Fetched {len(job_description):,} chars")

    st.divider()

    # Example questions — job-matching questions appear when a job is loaded
    st.markdown("**Try asking:**")
    example_questions = []
    if job_description:
        example_questions = [
            "How does Vishal match this role?",
            "What gaps should he address for this position?",
            "Write a cover letter for this role.",
        ]
    example_questions += [
        "What did Vishal build at the Blue Brain Project?",
        "How does his physics background apply to quantitative finance?",
        "Tell me about his publications on complex networks.",
        "What experience does he have with HPC and parallel computing?",
        "How did he transition between scientific domains?",
    ]

    for q in example_questions:
        if st.button(q, use_container_width=True):
            st.session_state.pending_question = q
            st.rerun()

    st.divider()
    st.caption(
        "This is an AI colleague who knows Vishal's work. "
        "Answers are grounded in his actual portfolio."
    )
    st.caption(f"Model: `{MODEL}`")
    used = st.session_state.get("message_count", 0)
    # Haiku: $0.80/M input, $4/M output. ~80K input tokens per turn, ~500 output tokens.
    input_cost = used * 80_000 * 0.80 / 1_000_000
    output_cost = used * 500 * 4.00 / 1_000_000
    st.caption(f"Est. cost this session: ${input_cost + output_cost:.2f}")


# --- Initialize state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "message_count" not in st.session_state:
    st.session_state.message_count = 0

# --- Load resources ---
system_prompt = get_system_prompt(identity, job_description)
client = get_client()

# --- Header ---
st.title("The Knowledgeable Colleague")
remaining = MAX_MESSAGES_PER_SESSION - st.session_state.message_count
st.caption(f"*{title}* — Ask me about Vishal Sood's work, expertise, and experience. "
           f"({remaining} free question{'s' if remaining != 1 else ''} remaining)")

# --- Display conversation history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Handle pending question from sidebar buttons ---
prompt = None
if "pending_question" in st.session_state:
    prompt = st.session_state.pending_question
    del st.session_state.pending_question

# --- Chat input ---
if st.session_state.message_count >= MAX_MESSAGES_PER_SESSION:
    st.info(
        f"You've used all {MAX_MESSAGES_PER_SESSION} questions in the free tier. "
        "A paid version with extended conversations and deeper analysis is coming soon.\n\n"
        "In the meantime, reach Vishal directly at "
        "**vishal.chandra.sood@protonmail.com**"
    )
elif prompt or (prompt := st.chat_input("Ask about Vishal's work...")):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.message_count += 1

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with client.messages.stream(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        ) as stream:
            full_response = st.write_stream(stream.text_stream)

    if full_response:
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
