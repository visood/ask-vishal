"""Internationalization strings for le comptoir.

Three languages for the Swiss market: English, French, German.
The portfolio content stays in English — Claude synthesizes answers
in the visitor's selected language.

Strings containing {name} are formatted at runtime with the active candidate's name.
"""

LANGUAGES = {
    "en": "English",
    "fr": "Français",
    "de": "Deutsch",
}

STRINGS = {
    "en": {
        "page_title": "le comptoir",
        "tab_chat": "le comptoir",
        "tab_plan": "Marketing Plan",
        "candidate_label": "Talk to",
        "download_pdf": "Download PDF",
        "header_tagline": "*le comptoir* — ask about {name}'s work",
        "identity_label": "Professional identity",
        "identity_help": "Changes how {name}'s experience is presented to visitors",
        "job_header": "**Match against a job**",
        "job_radio_none": "None",
        "job_radio_paste": "Paste text",
        "job_radio_url": "URL",
        "job_textarea_label": "Job description",
        "job_placeholder": "Paste the job description here...",
        "job_url_placeholder": "https://...",
        "job_fetching": "Fetching...",
        "try_asking": "**Try asking:**",
        "chat_placeholder": "Ask about {name}'s work...",
        "remaining": "{n} free question{s} remaining",
        "exhausted": (
            "You've used all {n} questions in the free tier. "
            "A paid version with extended conversations and deeper analysis "
            "is coming soon."
        ),
        "footer": (
            "*le comptoir* — AI agents who know these professionals' work. "
            "Answers are grounded in actual portfolios."
        ),
        "cost_label": "Est. cost this session: ${cost:.2f}",
        "unlock_heading": "Want deeper answers?",
        "unlock_body": (
            "You've used your {n} free preview questions. "
            "Leave your email to receive a passcode for extended access "
            "with longer, more detailed responses."
        ),
        "email_placeholder": "you@company.com",
        "email_submit": "Request access",
        "email_thanks": "Thank you! We'll send you a passcode shortly.",
        "passcode_label": "Have a passcode?",
        "passcode_placeholder": "Enter passcode",
        "passcode_submit": "Unlock",
        "passcode_invalid": "Invalid passcode. Please check and try again.",
        "passcode_success": "Unlocked! You now have extended access.",
        "example_questions": [
            "What are {name}'s strongest technical skills?",
            "Tell me about {name}'s most impactful project.",
            "How did {name} transition between roles or domains?",
            "What kind of teams has {name} worked with?",
            "What makes {name} stand out as a candidate?",
        ],
        "job_questions": [
            "How does {name} match this role?",
            "What gaps should {name} address for this position?",
            "Write a cover letter for this role.",
        ],
    },
    "fr": {
        "page_title": "le comptoir",
        "tab_chat": "le comptoir",
        "tab_plan": "Plan Marketing",
        "candidate_label": "Parler avec",
        "download_pdf": "Télécharger PDF",
        "header_tagline": "*le comptoir* — renseignez-vous sur le travail de {name}",
        "identity_label": "Identité professionnelle",
        "identity_help": "Change la manière dont l'expérience de {name} est présentée",
        "job_header": "**Comparer à un poste**",
        "job_radio_none": "Aucun",
        "job_radio_paste": "Coller le texte",
        "job_radio_url": "URL",
        "job_textarea_label": "Description du poste",
        "job_placeholder": "Collez la description du poste ici...",
        "job_url_placeholder": "https://...",
        "job_fetching": "Chargement...",
        "try_asking": "**Essayez de demander :**",
        "chat_placeholder": "Posez une question sur le travail de {name}...",
        "remaining": "{n} question{s} gratuite{s} restante{s}",
        "exhausted": (
            "Vous avez utilisé vos {n} questions gratuites. "
            "Une version payante avec des conversations plus approfondies "
            "sera bientôt disponible."
        ),
        "footer": (
            "*le comptoir* — des agents IA qui connaissent le travail de ces professionnels. "
            "Les réponses sont fondées sur leurs portfolios."
        ),
        "cost_label": "Coût estimé de la session : ${cost:.2f}",
        "unlock_heading": "Envie de réponses plus détaillées ?",
        "unlock_body": (
            "Vous avez utilisé vos {n} questions d'aperçu gratuites. "
            "Laissez votre email pour recevoir un code d'accès "
            "avec des réponses plus longues et détaillées."
        ),
        "email_placeholder": "vous@entreprise.com",
        "email_submit": "Demander l'accès",
        "email_thanks": "Merci ! Nous vous enverrons un code d'accès sous peu.",
        "passcode_label": "Vous avez un code ?",
        "passcode_placeholder": "Entrez le code",
        "passcode_submit": "Débloquer",
        "passcode_invalid": "Code invalide. Veuillez vérifier et réessayer.",
        "passcode_success": "Débloqué ! Vous avez maintenant un accès étendu.",
        "example_questions": [
            "Quelles sont les compétences techniques clés de {name} ?",
            "Parlez-moi du projet le plus marquant de {name}.",
            "Comment {name} a évolué entre différents domaines ?",
            "Avec quels types d'équipes {name} a travaillé ?",
            "Qu'est-ce qui distingue {name} comme candidat ?",
        ],
        "job_questions": [
            "En quoi {name} correspond à ce poste ?",
            "Quelles lacunes {name} devrait combler pour ce poste ?",
            "Rédigez une lettre de motivation pour ce poste.",
        ],
    },
    "de": {
        "page_title": "le comptoir",
        "tab_chat": "le comptoir",
        "tab_plan": "Marketingkonzept",
        "candidate_label": "Sprechen mit",
        "download_pdf": "PDF herunterladen",
        "header_tagline": "*le comptoir* — erfahren Sie mehr über {name}s Arbeit",
        "identity_label": "Berufliche Identität",
        "identity_help": "Ändert wie {name}s Erfahrung den Besuchern präsentiert wird",
        "job_header": "**Mit einer Stelle vergleichen**",
        "job_radio_none": "Keine",
        "job_radio_paste": "Text einfügen",
        "job_radio_url": "URL",
        "job_textarea_label": "Stellenbeschreibung",
        "job_placeholder": "Stellenbeschreibung hier einfügen...",
        "job_url_placeholder": "https://...",
        "job_fetching": "Wird geladen...",
        "try_asking": "**Probieren Sie zu fragen:**",
        "chat_placeholder": "Fragen Sie nach {name}s Arbeit...",
        "remaining": "{n} kostenlose Frage{n_de} übrig",
        "exhausted": (
            "Sie haben alle {n} kostenlosen Fragen aufgebraucht. "
            "Eine kostenpflichtige Version mit erweiterten Gesprächen und "
            "tieferer Analyse kommt bald."
        ),
        "footer": (
            "*le comptoir* — KI-Agenten, die die Arbeit dieser Fachleute kennen. "
            "Antworten basieren auf echten Portfolios."
        ),
        "cost_label": "Geschätzte Kosten dieser Sitzung: ${cost:.2f}",
        "unlock_heading": "Möchten Sie ausführlichere Antworten?",
        "unlock_body": (
            "Sie haben Ihre {n} kostenlosen Vorschau-Fragen aufgebraucht. "
            "Hinterlassen Sie Ihre E-Mail, um einen Zugangscode für erweiterten "
            "Zugang mit längeren, detaillierteren Antworten zu erhalten."
        ),
        "email_placeholder": "sie@firma.ch",
        "email_submit": "Zugang anfordern",
        "email_thanks": "Vielen Dank! Wir senden Ihnen in Kürze einen Zugangscode.",
        "passcode_label": "Haben Sie einen Zugangscode?",
        "passcode_placeholder": "Code eingeben",
        "passcode_submit": "Freischalten",
        "passcode_invalid": "Ungültiger Code. Bitte überprüfen und erneut versuchen.",
        "passcode_success": "Freigeschaltet! Sie haben jetzt erweiterten Zugang.",
        "example_questions": [
            "Was sind {name}s wichtigste technische Fähigkeiten?",
            "Erzählen Sie mir vom wirkungsvollsten Projekt von {name}.",
            "Wie hat {name} zwischen verschiedenen Bereichen gewechselt?",
            "Mit welchen Teams hat {name} zusammengearbeitet?",
            "Was zeichnet {name} als Kandidat aus?",
        ],
        "job_questions": [
            "Wie passt {name} zu dieser Stelle?",
            "Welche Lücken sollte {name} für diese Position schliessen?",
            "Schreiben Sie ein Bewerbungsschreiben für diese Stelle.",
        ],
    },
}
