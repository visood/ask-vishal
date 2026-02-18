"""Internationalization strings for le comptoir.

Three languages for the Swiss market: English, French, German.
The portfolio content stays in English — Claude synthesizes answers
in the visitor's selected language.
"""

LANGUAGES = {
    "en": "English",
    "fr": "Français",
    "de": "Deutsch",
}

STRINGS = {
    "en": {
        "page_title": "Vishal Sood — le comptoir",
        "tab_chat": "le comptoir",
        "tab_plan": "Marketing Plan",
        "download_pdf": "Download PDF",
        "header_tagline": "*le comptoir* — ask about his work",
        "identity_label": "Professional identity",
        "identity_help": "Changes how the agent frames Vishal's experience",
        "job_header": "**Match against a job**",
        "job_radio_none": "None",
        "job_radio_paste": "Paste text",
        "job_radio_url": "URL",
        "job_textarea_label": "Job description",
        "job_placeholder": "Paste the job description here...",
        "job_url_placeholder": "https://...",
        "job_fetching": "Fetching...",
        "try_asking": "**Try asking:**",
        "chat_placeholder": "Ask about Vishal's work...",
        "remaining": "{n} free question{s} remaining",
        "exhausted": (
            "You've used all {n} questions in the free tier. "
            "A paid version with extended conversations and deeper analysis "
            "is coming soon.\n\n"
            "In the meantime, reach Vishal directly at "
            "**vishal.chandra.sood@protonmail.com**"
        ),
        "footer": (
            "*le comptoir* — an AI agent who knows Vishal's work. "
            "Answers are grounded in his actual portfolio."
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
        "email_thanks": "Thank you! Vishal will send you a passcode shortly.",
        "passcode_label": "Have a passcode?",
        "passcode_placeholder": "Enter passcode",
        "passcode_submit": "Unlock",
        "passcode_invalid": "Invalid passcode. Please check and try again.",
        "passcode_success": "Unlocked! You now have extended access.",
        "example_questions": [
            "What did Vishal build at the Blue Brain Project?",
            "How does his physics background apply to quantitative finance?",
            "Tell me about his publications on complex networks.",
            "What experience does he have with HPC and parallel computing?",
            "How did he transition between scientific domains?",
        ],
        "job_questions": [
            "How does Vishal match this role?",
            "What gaps should he address for this position?",
            "Write a cover letter for this role.",
        ],
    },
    "fr": {
        "page_title": "Vishal Sood — le comptoir",
        "tab_chat": "le comptoir",
        "tab_plan": "Plan Marketing",
        "download_pdf": "Télécharger PDF",
        "header_tagline": "*le comptoir* — renseignez-vous sur son travail",
        "identity_label": "Identité professionnelle",
        "identity_help": "Change la manière dont l'agent présente l'expérience de Vishal",
        "job_header": "**Comparer à un poste**",
        "job_radio_none": "Aucun",
        "job_radio_paste": "Coller le texte",
        "job_radio_url": "URL",
        "job_textarea_label": "Description du poste",
        "job_placeholder": "Collez la description du poste ici...",
        "job_url_placeholder": "https://...",
        "job_fetching": "Chargement...",
        "try_asking": "**Essayez de demander :**",
        "chat_placeholder": "Posez une question sur le travail de Vishal...",
        "remaining": "{n} question{s} gratuite{s} restante{s}",
        "exhausted": (
            "Vous avez utilisé vos {n} questions gratuites. "
            "Une version payante avec des conversations plus approfondies "
            "sera bientôt disponible.\n\n"
            "En attendant, contactez Vishal directement à "
            "**vishal.chandra.sood@protonmail.com**"
        ),
        "footer": (
            "*le comptoir* — un agent IA qui connaît le travail de Vishal. "
            "Les réponses sont fondées sur son portfolio."
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
        "email_thanks": "Merci ! Vishal vous enverra un code d'accès sous peu.",
        "passcode_label": "Vous avez un code ?",
        "passcode_placeholder": "Entrez le code",
        "passcode_submit": "Débloquer",
        "passcode_invalid": "Code invalide. Veuillez vérifier et réessayer.",
        "passcode_success": "Débloqué ! Vous avez maintenant un accès étendu.",
        "example_questions": [
            "Qu'a construit Vishal au Blue Brain Project ?",
            "Comment sa formation en physique s'applique-t-elle à la finance quantitative ?",
            "Parlez-moi de ses publications sur les réseaux complexes.",
            "Quelle expérience a-t-il en HPC et calcul parallèle ?",
            "Comment a-t-il évolué entre les domaines scientifiques ?",
        ],
        "job_questions": [
            "En quoi Vishal correspond-il à ce poste ?",
            "Quelles lacunes devrait-il combler pour ce poste ?",
            "Rédigez une lettre de motivation pour ce poste.",
        ],
    },
    "de": {
        "page_title": "Vishal Sood — le comptoir",
        "tab_chat": "le comptoir",
        "tab_plan": "Marketingkonzept",
        "download_pdf": "PDF herunterladen",
        "header_tagline": "*le comptoir* — erfahren Sie mehr über seine Arbeit",
        "identity_label": "Berufliche Identität",
        "identity_help": "Ändert wie der Agent Vishals Erfahrung präsentiert",
        "job_header": "**Mit einer Stelle vergleichen**",
        "job_radio_none": "Keine",
        "job_radio_paste": "Text einfügen",
        "job_radio_url": "URL",
        "job_textarea_label": "Stellenbeschreibung",
        "job_placeholder": "Stellenbeschreibung hier einfügen...",
        "job_url_placeholder": "https://...",
        "job_fetching": "Wird geladen...",
        "try_asking": "**Probieren Sie zu fragen:**",
        "chat_placeholder": "Fragen Sie nach Vishals Arbeit...",
        "remaining": "{n} kostenlose Frage{n_de} übrig",
        "exhausted": (
            "Sie haben alle {n} kostenlosen Fragen aufgebraucht. "
            "Eine kostenpflichtige Version mit erweiterten Gesprächen und "
            "tieferer Analyse kommt bald.\n\n"
            "In der Zwischenzeit erreichen Sie Vishal direkt unter "
            "**vishal.chandra.sood@protonmail.com**"
        ),
        "footer": (
            "*le comptoir* — ein KI-Agent, der Vishals Arbeit kennt. "
            "Antworten basieren auf seinem Portfolio."
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
        "email_thanks": "Vielen Dank! Vishal wird Ihnen in Kürze einen Zugangscode senden.",
        "passcode_label": "Haben Sie einen Zugangscode?",
        "passcode_placeholder": "Code eingeben",
        "passcode_submit": "Freischalten",
        "passcode_invalid": "Ungültiger Code. Bitte überprüfen und erneut versuchen.",
        "passcode_success": "Freigeschaltet! Sie haben jetzt erweiterten Zugang.",
        "example_questions": [
            "Was hat Vishal beim Blue Brain Project entwickelt?",
            "Wie lässt sich sein Physik-Hintergrund auf quantitative Finanzen anwenden?",
            "Erzählen Sie mir von seinen Publikationen zu komplexen Netzwerken.",
            "Welche Erfahrung hat er mit HPC und parallelem Rechnen?",
            "Wie hat er den Wechsel zwischen wissenschaftlichen Bereichen vollzogen?",
        ],
        "job_questions": [
            "Wie passt Vishal zu dieser Stelle?",
            "Welche Lücken sollte er für diese Position schliessen?",
            "Schreiben Sie ein Bewerbungsschreiben für diese Stelle.",
        ],
    },
}
