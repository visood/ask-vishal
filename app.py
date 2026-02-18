"""le comptoir — Streamlit chat interface.

An inverse-recruitment agency: a roster of professionals in career transition,
each with their own AI agent that recruiters and hiring managers can talk to.

Features:
  - Candidate roster (select who to talk to)
  - Language selector (English, Francais, Deutsch)
  - Professional identity selector (adapt framing to role type)
  - Job description matching (paste text or URL, get a fit analysis)
  - Conversational Q&A grounded in portfolio content
  - Marketing plan with downloadable PDFs

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
AGENTS_DIR = Path(__file__).parent / "agents"

# --- Agent roster ---
# Each agent: key -> (display_name, tagline, context_file, identities, default_identity)
AGENTS = {
    "vishal": {
        "name": "Vishal Sood",
        "tagline": "Senior Research Engineer | PhD Physics | HPC, Genomics, Scientific Computing",
        "context": AGENTS_DIR / "vishal" / "context.txt",
        "has_plan": True,
        "identities": {
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
        },
        "default_identity": "Research Engineer",
    },
    "marc": {
        "name": "Marc Delarue",
        "tagline": "Senior Risk Manager | 20 years Private Banking | CFA, FRM",
        "context": AGENTS_DIR / "marc" / "context.txt",
        "has_plan": False,
        "identities": {
            "Risk Manager": (
                "Senior Risk Manager",
                "A seasoned private banking professional with over 20 years in risk management, "
                "portfolio oversight, and regulatory compliance across Geneva's leading financial "
                "institutions. Known for building robust risk frameworks that balance client "
                "service excellence with regulatory rigor.",
            ),
            "CRO / Executive": (
                "Chief Risk Officer",
                "An experienced risk executive ready for CRO-level responsibility at boutique "
                "private banks or family offices. Two decades of building and leading risk teams, "
                "presenting to board committees, and navigating FINMA regulatory cycles.",
            ),
            "Risk Consultant": (
                "Risk & Compliance Consultant",
                "A private banking risk specialist available for consulting engagements: "
                "regulatory remediation, risk framework design, FIDLEG implementation, "
                "and interim risk management mandates.",
            ),
        },
        "default_identity": "Risk Manager",
    },
    "sophie": {
        "name": "Sophie Andersen",
        "tagline": "Senior Compliance Officer | 18 years Banking Regulation | MLaw, CAMS",
        "context": AGENTS_DIR / "sophie" / "context.txt",
        "has_plan": False,
        "identities": {
            "Compliance Officer": (
                "Senior Compliance Officer",
                "A compliance and regulatory specialist with 18 years across corporate banking, "
                "trade finance, and asset management. Expert in Swiss and EU financial regulation, "
                "cross-border banking, and sanctions compliance.",
            ),
            "Head of Compliance": (
                "Head of Compliance",
                "Ready for Head of Compliance roles at mid-sized banks or asset managers. "
                "Built compliance programs from scratch at two Swiss banks, led FIDLEG "
                "implementation, and managed regulatory examinations with consistently "
                "positive outcomes.",
            ),
            "Regulatory Consultant": (
                "Regulatory Affairs Consultant",
                "Available for compliance consulting: FIDLEG implementation, regulatory "
                "remediation, AML program design, and fintech regulatory advisory. "
                "Bridges German-speaking and French-speaking Swiss banking cultures.",
            ),
        },
        "default_identity": "Compliance Officer",
    },
    "olena": {
        "name": "Olena Kovalenko",
        "tagline": "Cardiologist (Ukraine) | Clinical Research | CHUV Lausanne",
        "context": AGENTS_DIR / "olena" / "context.txt",
        "has_plan": False,
        "identities": {
            "Clinical Researcher": (
                "Clinical Research Professional",
                "A physician with 12 years of cardiology experience and active clinical "
                "research at CHUV. Experienced in multicenter clinical trials, GCP, "
                "and medical device evaluations. Pursuing Swiss medical equivalence.",
            ),
            "Medical Doctor": (
                "Cardiologist (MEBEKO pathway)",
                "A board-certified cardiologist with 12 years of clinical practice, "
                "3,000+ echocardiograms, and ward chief experience. Completing the "
                "Swiss equivalence pathway while contributing to research at CHUV.",
            ),
            "Medtech / MSL": (
                "Medical Science Liaison / Clinical Affairs",
                "Leveraging deep cardiology expertise for medical device and pharmaceutical "
                "roles: MSL, clinical affairs, medical writing, and regulatory documentation "
                "from the physician's perspective.",
            ),
        },
        "default_identity": "Clinical Researcher",
    },
    "david": {
        "name": "David Chen",
        "tagline": "Technical Writer | 15 years Medtech | EU MDR, Catalogs, CCMS",
        "context": AGENTS_DIR / "david" / "context.txt",
        "has_plan": False,
        "identities": {
            "Technical Writer": (
                "Senior Technical Writer / Documentation Lead",
                "A technical communicator with 15 years creating product catalogs, "
                "regulatory documentation, and surgical technique guides for Swiss "
                "medtech companies. Expert in structured content management and "
                "multilingual publishing.",
            ),
            "Regulatory Documentation": (
                "Regulatory Documentation Specialist",
                "Specialized in EU MDR documentation: IFUs, labeling, technical files, "
                "and CE marking submissions. Led MDR transition projects for 400+ documents "
                "at a major spine surgery company.",
            ),
            "Content Strategy": (
                "Content Strategy & PIM Specialist",
                "Helping medtech companies move from legacy documentation to digital-first "
                "product content. Experienced with CCMS, PIM systems, single-source publishing, "
                "and automated translation workflows.",
            ),
        },
        "default_identity": "Technical Writer",
    },
}


# --- Page config ---
st.set_page_config(
    page_title="le comptoir",
    page_icon="🏪",
    layout="centered",
)


# --- Cached resources ---
@st.cache_resource
def load_context(path: str) -> str:
    """Load a candidate's portfolio content (cached per path)."""
    return Path(path).read_text(encoding="utf-8")


@st.cache_resource
def get_client():
    """Create Anthropic client (cached)."""
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
        return anthropic.Anthropic(api_key=api_key)
    except (FileNotFoundError, KeyError):
        return anthropic.Anthropic()


def get_system_prompt(agent: dict, identity_key: str, job_description: str = "",
                      language: str = "en", concise: bool = False) -> str:
    """Build system prompt with identity framing and optional job context."""
    content = load_context(str(agent["context"]))
    name = agent["name"]
    title, summary = agent["identities"][identity_key]

    identity_block = (
        f"\n\n--- Active Professional Identity ---\n\n"
        f"Title: {title}\n"
        f"Summary: {summary}\n\n"
        f"When discussing {name}'s work, lead with this framing. "
        f"Emphasize the aspects of their experience most relevant to a "
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
    st.title("le comptoir")
    st.caption("*an agency of professionals in transition*")

    st.divider()

    # Language selector
    lang_options = list(LANGUAGES.keys())
    lang = st.selectbox(
        "Language",
        options=lang_options,
        format_func=lambda code: LANGUAGES[code],
        index=0,
    )
    t = STRINGS[lang]

    st.divider()

    # Candidate selector
    agent_keys = list(AGENTS.keys())
    if "current_agent" not in st.session_state:
        st.session_state.current_agent = agent_keys[0]

    def _on_agent_change():
        st.session_state.current_agent = st.session_state._agent_select
        st.session_state.messages = []
        st.session_state.message_count = 0

    st.selectbox(
        t["candidate_label"],
        options=agent_keys,
        format_func=lambda k: f"{AGENTS[k]['name']} — {AGENTS[k]['tagline']}",
        index=agent_keys.index(st.session_state.current_agent),
        key="_agent_select",
        on_change=_on_agent_change,
    )

    current_agent = AGENTS[st.session_state.current_agent]
    agent_name = current_agent["name"].split()[0]  # first name for UI strings

    st.divider()

    # Identity selector
    identities = current_agent["identities"]
    default_id = current_agent["default_identity"]
    identity = st.selectbox(
        t["identity_label"],
        options=list(identities.keys()),
        index=list(identities.keys()).index(default_id),
        help=t["identity_help"].format(name=agent_name),
    )
    title, summary = identities[identity]
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
        example_questions = [q.format(name=agent_name) for q in t["job_questions"]]
    example_questions += [q.format(name=agent_name) for q in t["example_questions"]]

    for i, q in enumerate(example_questions):
        if st.button(q, key=f"eq_{st.session_state.current_agent}_{i}", use_container_width=True):
            st.session_state.pending_question = q
            st.rerun()

    st.divider()

    # Passcode entry
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
system_prompt = get_system_prompt(current_agent, identity, job_description,
                                  language=lang, concise=is_concise)
client = get_client()

# --- Header ---
st.title(current_agent["name"])
st.caption(f"*{title}*")

# --- Tabs ---
tabs = [t["tab_chat"]]
if current_agent["has_plan"]:
    tabs.append(t["tab_plan"])
active_tabs = st.tabs(tabs)

# ===================== TAB 1: CHAT =====================
with active_tabs[0]:
    st.markdown(t["header_tagline"].format(name=agent_name))
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

    # Suggestion buttons when conversation is empty
    if not st.session_state.messages and st.session_state.message_count < max_questions:
        suggestions = [q.format(name=agent_name) for q in t["example_questions"][:3]]
        if job_description:
            suggestions = [q.format(name=agent_name) for q in t["job_questions"][:2]] + suggestions[:1]
        cols = st.columns(len(suggestions))
        for i, (col, q) in enumerate(zip(cols, suggestions)):
            with col:
                if st.button(q, key=f"suggest_{st.session_state.current_agent}_{i}",
                             use_container_width=True):
                    st.session_state.pending_question = q
                    st.rerun()

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

    elif prompt or (prompt := st.chat_input(t["chat_placeholder"].format(name=agent_name))):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.message_count += 1

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
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
            except anthropic.AuthenticationError:
                st.error("API configuration error. Please try again later.")
                full_response = None
            except anthropic.APIError:
                st.error("Something went wrong. Please try again.")
                full_response = None

        if full_response:
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

# ===================== TAB 2: MARKETING PLAN (if available) =====================
if current_agent["has_plan"] and len(active_tabs) > 1:
    with active_tabs[1]:
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
