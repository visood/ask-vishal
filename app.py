"""le comptoir — Streamlit chat interface.

A conversational CV where visitors talk to an AI that knows Vishal Sood's work deeply.
Features:
  - Language selector (English, Français, Deutsch)
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
from i18n import LANGUAGES, STRINGS
from marketing_plan import get_plan
from generate_pdf import generate_marketing_plan_pdf


# --- Configuration ---
MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS_FREE = 256
MAX_TOKENS_UNLOCKED = 1024
FREE_QUESTIONS = 5
UNLOCKED_QUESTIONS = 30
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
    page_title="Vishal Sood — le comptoir",
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


def get_system_prompt(identity_key: str, job_description: str = "",
                      language: str = "en", concise: bool = False) -> str:
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

    return build_system_prompt(content + identity_block + job_block,
                               language=language, concise=concise)


def fetch_url_text(url: str) -> str:
    """Fetch a URL and extract readable text."""
    try:
        resp = requests.get(url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (compatible; LeComptoir/1.0)"
        })
        resp.raise_for_status()
        text = re.sub(r'<script[^>]*>.*?</script>', '', resp.text, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:10000]
    except Exception as e:
        return f"[Could not fetch URL: {e}]"


# --- Sidebar ---
with st.sidebar:
    st.title("Vishal Sood")

    # Language selector
    lang_options = list(LANGUAGES.keys())
    lang_labels = list(LANGUAGES.values())
    lang = st.selectbox(
        "Language",
        options=lang_options,
        format_func=lambda code: LANGUAGES[code],
        index=0,
    )
    t = STRINGS[lang]

    st.divider()

    # Identity selector
    identity = st.selectbox(
        t["identity_label"],
        options=list(IDENTITIES.keys()),
        index=list(IDENTITIES.keys()).index(DEFAULT_IDENTITY),
        help=t["identity_help"],
    )
    title, summary = IDENTITIES[identity]
    st.caption(title)

    st.divider()

    # Job description input
    st.markdown(t["job_header"])
    job_radio_options = [t["job_radio_none"], t["job_radio_paste"], t["job_radio_url"]]
    job_input_method = st.radio(
        "job_method",
        job_radio_options,
        index=0,
        label_visibility="collapsed",
    )

    job_description = ""
    if job_input_method == t["job_radio_paste"]:
        job_description = st.text_area(
            t["job_textarea_label"],
            height=150,
            placeholder=t["job_placeholder"],
        )
    elif job_input_method == t["job_radio_url"]:
        job_url = st.text_input("URL", placeholder=t["job_url_placeholder"])
        if job_url:
            with st.spinner(t["job_fetching"]):
                job_description = fetch_url_text(job_url)
            if job_description.startswith("[Could not"):
                st.warning(job_description)
                job_description = ""
            else:
                st.success(f"Fetched {len(job_description):,} chars")

    st.divider()

    # Example questions
    st.markdown(t["try_asking"])
    example_questions = []
    if job_description:
        example_questions = list(t["job_questions"])
    example_questions += list(t["example_questions"])

    for q in example_questions:
        if st.button(q, use_container_width=True):
            st.session_state.pending_question = q
            st.rerun()

    st.divider()

    # Passcode entry in sidebar
    st.markdown(t["passcode_label"])
    passcode_input = st.text_input(
        "passcode",
        placeholder=t["passcode_placeholder"],
        label_visibility="collapsed",
    )
    if st.button(t["passcode_submit"], use_container_width=True):
        valid_codes = set()
        try:
            raw = st.secrets.get("PASSCODES", "")
            valid_codes = {c.strip() for c in raw.split(",") if c.strip()}
        except (FileNotFoundError, KeyError):
            pass
        if passcode_input.strip() in valid_codes:
            st.session_state.unlocked = True
            st.success(t["passcode_success"])
            st.rerun()
        elif passcode_input.strip():
            st.error(t["passcode_invalid"])

    st.divider()
    st.caption(t["footer"])
    st.caption(f"Model: `{MODEL}`")
    used = st.session_state.get("message_count", 0)
    input_cost = used * 80_000 * 0.80 / 1_000_000
    output_cost = used * 500 * 4.00 / 1_000_000
    st.caption(t["cost_label"].format(cost=input_cost + output_cost))


# --- Initialize state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "message_count" not in st.session_state:
    st.session_state.message_count = 0
if "unlocked" not in st.session_state:
    st.session_state.unlocked = False
if "email_submitted" not in st.session_state:
    st.session_state.email_submitted = False

# --- Determine tier ---
unlocked = st.session_state.unlocked
max_questions = UNLOCKED_QUESTIONS if unlocked else FREE_QUESTIONS
max_tokens = MAX_TOKENS_UNLOCKED if unlocked else MAX_TOKENS_FREE
is_concise = not unlocked

# --- Load resources ---
system_prompt = get_system_prompt(identity, job_description, language=lang,
                                  concise=is_concise)
client = get_client()

# --- Header ---
st.title("Vishal Sood")
st.caption(f"*{title}*")

# --- Tabs ---
tab_chat, tab_plan = st.tabs([t["tab_chat"], t["tab_plan"]])

# ===================== TAB 1: CHAT =====================
with tab_chat:
    st.markdown(t["header_tagline"])
    remaining = max_questions - st.session_state.message_count
    remaining = max(remaining, 0)
    if lang == "de":
        plural = "n" if remaining != 1 else ""
        st.caption(t["remaining"].format(n=remaining, n_de=plural))
    else:
        plural = "s" if remaining != 1 else ""
        st.caption(t["remaining"].format(n=remaining, s=plural))

    # Display conversation history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle pending question from sidebar buttons
    prompt = None
    if "pending_question" in st.session_state:
        prompt = st.session_state.pending_question
        del st.session_state.pending_question

    # Chat input
    if st.session_state.message_count >= max_questions:
        st.markdown(f"### {t['unlock_heading']}")
        st.markdown(t["unlock_body"].format(n=max_questions))

        if st.session_state.email_submitted:
            st.success(t["email_thanks"])
        else:
            email = st.text_input("email", placeholder=t["email_placeholder"],
                                  label_visibility="collapsed")
            if st.button(t["email_submit"]):
                if email and "@" in email:
                    st.session_state.email_submitted = True
                    print(f"ACCESS_REQUEST: {email}")
                    st.rerun()

    elif prompt or (prompt := st.chat_input(t["chat_placeholder"])):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.message_count += 1

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with client.messages.stream(
                model=MODEL,
                max_tokens=max_tokens,
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

# ===================== TAB 2: MARKETING PLAN =====================
with tab_plan:
    plan = get_plan(lang)

    # Download button
    pdf_bytes = generate_marketing_plan_pdf(lang)
    st.download_button(
        label=f"{t['download_pdf']} ({LANGUAGES[lang]})",
        data=pdf_bytes,
        file_name=f"marketing-plan-{lang}.pdf",
        mime="application/pdf",
    )

    st.divider()

    # Render plan sections
    for section in plan["sections"]:
        st.markdown(f"### {section['heading']}")
        st.markdown(section["body"])
        st.markdown("---")
