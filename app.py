import streamlit as st
from groq import Groq

# Seitenkonfiguration festlegen
st.set_page_config(
    page_title="Lumina Code KI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INITIALISIERUNG VON SESSION & VERLAUF ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "reflection_done" not in st.session_state:
    st.session_state.reflection_done = False
if "final_feedback" not in st.session_state:
    st.session_state.final_feedback = ""
if "user_code" not in st.session_state:
    st.session_state.user_code = ""
if "saved_sessions" not in st.session_state:
    st.session_state.saved_sessions = []

# --- ERWEITERTES SPRACHWÖRTERBUCH ---
texts = {
    "Français": {
        "api_label": "Clé API Groq :", "model_label": "Modèle IA :", "mode_label": "Mode d'apprentissage :",
        "modes": ["Mentor Pédagogique (Conseils)", "Debogueur Direct", "Optimiseur de Code"],
        "level_label": "Niveau de difficulté :", "levels": ["Débutant", "Intermédiaire", "Expert"],
        "new_chat_btn": "Nouvelle discussion", "reset_btn": "Réinitialiser la session",
        "history_title": "Historique des discussions", "delete_chat": "Supprimer",
        "status_title": "Statut du système", "status_ok": "Clé API détectée & prête.", "status_warn": "Veuillez entrer votre clé API Groq.",
        "hero_title": "Lumina Code KI", "hero_sub": "Votre mentor de code intelligent propulsé par l'IA pour un apprentissage approfondi.",
        "card_code_title": "Code Source & Requête", "lang_label": "Langage de programmation / de requête :",
        "analyze_btn": "Analyser et comprendre le code", "card_chat_title": "Analyse IA & Chat Interactif",
        "err_no_key": "Veuillez d'abord entrer votre clé API Groq dans la barre latérale !",
        "err_no_code": "Veuillez d'abord entrer du code !", "spinner_analyze": "Lumina analyse le code...",
        "chat_input_ph": "Posez une question sur le code ou l'analyse...", "spinner_think": "Lumina réfléchit...",
        "reflection_title": "Réflexion & Conclusion", "reflection_ph": "Aujourd'hui, j'ai appris que...",
        "reflection_btn": "Envoyer la réflexion & obtenir le mot de la fin", "reflection_warn": "Veuillez écrire brièvement ce que vous avez appris.",
        "spinner_feedback": "Lumina formule le mot de la fin...",
        "success_feedback": "Excellent travail ! Voici le mot de la fin de votre mentor :",
        "info_init": "Entrez votre clé API, collez votre code à gauche et cliquez sur 'Analyser et comprendre le code'.",
        "footer": "Lumina Code KI Core v1.0 • Environnement sécurisé & intelligent"
    },
    "Deutsch": {
        "api_label": "Groq API-Key:", "model_label": "KI-Modell:", "mode_label": "Lernmodus:",
        "modes": ["Pädagogischer Mentor (Tipps)", "Direkter Debugger", "Code Optimizer"],
        "level_label": "Schwierigkeitsgrad:", "levels": ["Anfänger", "Fortgeschritten", "Experte"],
        "new_chat_btn": "Neue Diskussion", "reset_btn": "Session zurücksetzen",
        "history_title": "Diskussionsverlauf", "delete_chat": "Löschen",
        "status_title": "Systemstatus", "status_ok": "API-Key erkannt & bereit.", "status_warn": "Bitte gib deinen Groq API-Key ein.",
        "hero_title": "Lumina Code KI", "hero_sub": "Dein intelligenter, KI-gestützter Code-Mentor für tiefe Einblicke und echten Lerneffekt.",
        "card_code_title": "Quellcode & Abfrage Eingabe", "lang_label": "Programmiersprache / Abfragesprache:",
        "analyze_btn": "Code analysieren & verstehen", "card_chat_title": "KI-Analyse & Interaktiver Chat",
        "err_no_key": "Bitte gib zuerst deinen Groq API-Key in der Seitenleiste ein!",
        "err_no_code": "Bitte gib zuerst etwas Code ein!", "spinner_analyze": "Lumina KI analysiert den Code...",
        "chat_input_ph": "Stelle eine Frage zum Code oder zur Analyse...", "spinner_think": "Lumina KI denkt nach...",
        "reflection_title": "Lernreflexion & Abschluss", "reflection_ph": "Heute habe ich gelernt, dass...",
        "reflection_btn": "Reflexion abschicken & Abschlusswort erhalten", "reflection_warn": "Bitte schreibe kurz, was du gelernt hast.",
        "spinner_feedback": "Lumina formuliert das Abschlusswort...",
        "success_feedback": "Hervorragende Arbeit! Hier ist dein Mentor-Abschlusswort:",
        "info_init": "Trage deinen API-Key ein, füge links deinen Code ein und klicke auf 'Code analysieren & verstehen'.",
        "footer": "Lumina Code KI Core v1.0 • Sichere & intelligente Umgebung"
    },
    "English": {
        "api_label": "Groq API Key:", "model_label": "AI Model:", "mode_label": "Learning Mode:",
        "modes": ["Pedagogical Mentor (Tips)", "Direct Debugger", "Code Optimizer"],
        "level_label": "Difficulty Level:", "levels": ["Beginner", "Intermediate", "Expert"],
        "new_chat_btn": "New Chat", "reset_btn": "Reset Session",
        "history_title": "Chat History", "delete_chat": "Delete",
        "status_title": "System Status",
        "status_ok": "API Key detected & ready.", "status_warn": "Please enter your Groq API Key.",
        "hero_title": "Lumina Code KI", "hero_sub": "Your intelligent, AI-powered code mentor for deep insights and real learning.",
        "card_code_title": "Source Code & Query Input", "lang_label": "Programming / Query Language:",
        "analyze_btn": "Analyze & Understand Code", "card_chat_title": "AI Analysis & Interactive Chat",
        "err_no_key": "Please enter your Groq API Key in the sidebar first!",
        "err_no_code": "Please enter some code first!", "spinner_analyze": "Lumina AI is analyzing the code...",
        "chat_input_ph": "Ask a question about the code or analysis...", "spinner_think": "Lumina AI is thinking...",
        "reflection_title": "Reflection & Conclusion", "reflection_ph": "Today I learned that...",
        "reflection_btn": "Submit Reflection & Get Closing Word", "reflection_warn": "Please write briefly what you have learned.",
        "spinner_feedback": "Lumina is formulating the closing statement...",
        "success_feedback": "Great job! Here is your mentor's closing statement:",
        "info_init": "Enter your API Key, paste your code on the left and click 'Analyze & Understand Code'.",
        "footer": "Lumina Code KI Core v1.0 • Secure & Intelligent Environment"
    },
    "Italiano": {
        "api_label": "Chiave API Groq:", "model_label": "Modello IA:", "mode_label": "Modalità di apprendimento:",
        "modes": ["Mentore Pedagogico (Consigli)", "Debugger Diretto", "Ottimizzatore di Codice"],
        "level_label": "Livello di difficoltà:", "levels": ["Principiante", "Intermedio", "Esperto"],
        "new_chat_btn": "Nuova discussione", "reset_btn": "Ripristina sessione",
        "history_title": "Cronologia chat", "delete_chat": "Elimina",
        "status_title": "Stato del sistema", "status_ok": "Chiave API rilevata e pronta.", "status_warn": "Inserisci la tua chiave API Groq.",
        "hero_title": "Lumina Code KI", "hero_sub": "Il tuo mentore di codice intelligente basato su IA per approfondimenti e apprendimento reale.",
        "card_code_title": "Codice Sorgente e Query", "lang_label": "Linguaggio di programmazione / query:",
        "analyze_btn": "Analizza e comprendi il codice", "card_chat_title": "Analisi IA e Chat Interattiva",
        "err_no_key": "Inserisci prima la tua chiave API Groq nella barra laterale!",
        "err_no_code": "Inserisci prima del codice!", "spinner_analyze": "Lumina sta analizzando il codice...",
        "chat_input_ph": "Fai una domanda sul codice o sull'analisi...", "spinner_think": "Lumina sta pensando...",
        "reflection_title": "Riflessione e Conclusione", "reflection_ph": "Oggi ho imparato che...",
        "reflection_btn": "Invia riflessione e ottieni la conclusione", "reflection_warn": "Scrivi brevemente cosa hai imparato.",
        "spinner_feedback": "Lumina sta formulando la dichiarazione finale...",
        "success_feedback": "Ottimo lavoro! Ecco la dichiarazione finale del tuo mentore:",
        "info_init": "Inserisci la chiave API, incolla il codice a sinistra e clicca 'Analizza e comprendi il codice'.",
        "footer": "Lumina Code KI Core v1.0 • Ambiente sicuro e intelligente"
    },
    "中文": {
        "api_label": "Groq API 密钥:", "model_label": "AI 模型:", "mode_label": "学习模式:",
        "modes": ["教学导师 (提示)", "直接调试器", "代码优化器"],
        "level_label": "难度级别:", "levels": ["初级", "中级", "专家"],
        "new_chat_btn": "新建对话", "reset_btn": "重置会话",
        "history_title": "历史对话记录", "delete_chat": "删除",
        "status_title": "系统状态", "status_ok": "API 密钥已就绪。", "status_warn": "请输入您的 Groq API 密钥。",
        "hero_title": "Lumina Code KI", "hero_sub": "您的智能 AI 代码导师，助您深入理解并实现高效学习。",
        "card_code_title": "源代码与查询输入", "lang_label": "编程/查询语言:",
        "analyze_btn": "分析并理解代码", "card_chat_title": "AI 分析与互动聊天",
        "err_no_key": "请先在侧边栏输入您的 Groq API 密钥！",
        "err_no_code": "请先输入一些代码！", "spinner_analyze": "Lumina 正在分析代码...",
        "chat_input_ph": "提出关于代码或分析的问题...", "spinner_think": "Lumina 正在思考...",
        "reflection_title": "学习反思与总结", "reflection_ph": "今天我学到了...",
        "reflection_btn": "提交反思并获取导师寄语", "reflection_warn": "请简要写下你学到的内容。",
        "spinner_feedback": "Lumina 正在生成总结寄语...",
        "success_feedback": "做得好！这是导师给你的寄语：",
        "info_init": "输入API密钥，在左侧粘贴代码并点击“分析并理解代码”。",
        "footer": "Lumina Code KI Core v1.0 • 安全智能环境"
    },
    "Español": {
        "api_label": "Clave API Groq:", "model_label": "Modelo de IA:", "mode_label": "Modo de aprendizaje:",
        "modes": ["Mentor pedagógico (Consejos)", "Depurador directo", "Optimizador de código"],
        "level_label": "Nivel de dificultad:", "levels": ["Principiante", "Intermedio", "Experto"],
        "new_chat_btn": "Nueva discusión", "reset_btn": "Restablecer sesión",
        "history_title": "Historial de chats", "delete_chat": "Elimina",
        "status_title": "Estado del sistema", "status_ok": "Clave API detectada y lista.", "status_warn": "Por favor introduce tu clave API Groq.",
        "hero_title": "Lumina Code KI", "hero_sub": "Tu mentor de código inteligente impulsado por IA para un aprendizaje profundo.",
        "card_code_title": "Código fuente y consulta", "lang_label": "Lenguaje de programación / consulta:",
        "analyze_btn": "Analizar y comprender el código", "card_chat_title": "Análisis IA y Chat Interactivo",
        "err_no_key": "¡Introduce primero tu clave API Groq en la barra lateral!",
        "err_no_code": "¡Introduce algo de código primero!", "spinner_analyze": "Lumina está analizando el código...",
        "chat_input_ph": "Haz una pregunta sobre el código o el análisis...", "spinner_think": "Lumina está pensando...",
        "reflection_title": "Reflexión y conclusión", "reflection_ph": "Hoy he aprendido que...",
        "reflection_btn": "Enviar reflexión et obtener palabra de cierre", "reflection_warn": "Por favor escribe brevemente lo que has aprendido.",
        "spinner_feedback": "Lumina está formulando la declaración final...",
        "success_feedback": "¡Buen trabajo! Aquí tienes la palabra de cierre de tu mentor:",
        "info_init": "Introduce tu clave API, pega tu código a la izquierda y haz clic en 'Analizar y comprender el código'.",
        "footer": "Lumina Code KI Core v1.0 • Entorno seguro e inteligente"
    }
}

# --- SIDEBAR FÜR EINSTELLUNGEN UND VERLAUF ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #6366f1;'>Lumina Control</h2>", unsafe_allow_html=True)
    st.markdown("---")

    theme_choice = st.selectbox("Thème / Theme:", ["Nuit (Dark)", "Jour (Light)"])
    is_dark = "Nuit" in theme_choice

    lang_choice = st.selectbox("Langue / Language:", ["Français", "Deutsch", "English", "Italiano", "中文", "Español"])

t = texts[lang_choice]

with st.sidebar:
    st.markdown("---")
    groq_api_key = st.text_input(t["api_label"], type="password", placeholder="gsk_...")

    st.markdown("---")
    selected_model = st.selectbox(t["model_label"], ["qwen/qwen3.8-27b"])
    mode = st.selectbox(t["mode_label"], t["modes"])
    level = st.select_slider(t["level_label"], options=t["levels"])

    st.markdown("---")
    if st.button(t["reset_btn"]):
        st.session_state.messages = []
        st.session_state.reflection_done = False
        st.session_state.final_feedback = ""
        st.session_state.user_code = ""
        st.rerun()

    st.markdown(f"### {t['history_title']}")
    if st.session_state.saved_sessions:
        for idx, chat_item in enumerate(st.session_state.saved_sessions):
            col_h1, col_h2 = st.columns([3, 1])
            with col_h1:
                if st.button(chat_item["title"], key=f"load_chat_{idx}"):
                    st.session_state.messages = chat_item["messages"]
                    st.session_state.user_code = chat_item["code"]
                    st.session_state.reflection_done = chat_item.get("reflection_done", False)
                    st.session_state.final_feedback = chat_item.get("final_feedback", "")
                    st.rerun()
            with col_h2:
                if st.button("X", key=f"del_chat_{idx}"):
                    st.session_state.saved_sessions.pop(idx)
                    st.rerun()
    else:
        st.caption("Aucune discussion sauvegardée." if lang_choice=="Français" else "Keine gespeicherten Chats." if lang_choice=="Deutsch" else "No saved chats." if lang_choice=="English" else "Nessuna chat salvata." if lang_choice=="Italiano" else "暂无保存的对话。" if lang_choice=="中文" else "No hay chats guardados.")

    st.markdown("---")
    st.markdown(f"### {t['status_title']}")
    if groq_api_key:
        st.success(t["status_ok"])
    else:
        st.warning(t["status_warn"])

# --- FARBKONFIGURATION (SIDEBAR IMMER HELL, BEREICH IM DUNKELMODUS DUNKEL) ---
if is_dark:
    bg_gradient = "linear-gradient(135deg, #050811 0%, #0f172a 50%, #020617 100%)"
    text_color = "#ffffff"
    sub_color = "#94a3b8"
    card_bg = "#0f172a"
    card_border = "1px solid #334155"
    code_bg = "#334155"
    code_text = "#38bdf8"
    input_bg = "#1e293b"
    input_border = "#475569"

    sidebar_bg = "#ffffff"
    sidebar_text = "#1e293b"
else:
    bg_gradient = "linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f1f5f9 100%)"
    text_color = "#1e293b"
    sub_color = "#64748b"
    card_bg = "#ffffff"
    card_border = "1px solid #cbd5e1"
    code_bg = "#e2e8f0"
    code_text = "#0284c7"
    input_bg = "#ffffff"
    input_border = "#cbd5e1"

    sidebar_bg = "#f1f5f9"
    sidebar_text = "#1e293b"

st.markdown(f"""
    <style>
    .stApp {{
        background: {bg_gradient};
    }}

    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
    }}

    footer {{visibility: hidden;}}

    .hero-container {{
        padding: 1rem 1rem 0.5rem 1rem;
        text-align: center;
    }}
    .main-title {{
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }}
    .sub-title {{
        color: {sub_color};
        font-size: 1.05rem;
        max-width: 600px;
        margin: 0 auto 1rem auto;
    }}

    .glass-card {{
        background: {card_bg};
        border: {card_border};
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
        margin-bottom: 20px;
    }}

    .glass-card *, .stApp p:not([data-testid="stSidebar"] p), .stApp span:not([data-testid="stSidebar"] span), .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    div[data-testid="stMarkdownContainer"] *,
    .stChatMessage * {{
        color: {text_color} !important;
    }}

    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] div, [data-testid="stSidebar"] input {{
        color: {sidebar_text} !important;
    }}

    textarea, input:not([data-testid="stSidebar"] input) {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border-color: {input_border} !important;
    }}

    .stChatMessage code {{
        background-color: {code_bg} !important;
        color: {code_text} !important;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.9em;
    }}

    div[data-testid="stAlert"] * {{
        color: #0f172a !important;
    }}

    .stButton>button {{
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white !important;
        font-weight: 700;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        border: none;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(168, 85, 247, 0.6);
    }}
    </style>
""", unsafe_allow_html=True)

# --- KOPFBEREICH ---
st.markdown(f"""
    <div class="hero-container">
        <h1 class="main-title">{t["hero_title"]}</h1>
        <p class="sub-title">{t["hero_sub"]}</p>
    </div>
""", unsafe_allow_html=True)

# --- HAUPTBEREICH IN SPALTEN ---
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f"### {t['card_code_title']}")
    language = st.selectbox(t["lang_label"], ["SQL", "Python", "C", "C++", "Java", "JavaScript", "TypeScript"])
    st.session_state.user_code = st.text_area("Code input:", height=250, value=st.session_state.user_code, label_visibility="collapsed")

    analyze_btn = st.button(t["analyze_btn"])
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    col_chat_head1, col_chat_head2 = st.columns([2, 1])
    with col_chat_head1:
        st.markdown(f"### {t['card_chat_title']}")
    with col_chat_head2:
        if st.button(t["new_chat_btn"], key="new_chat_top"):
            if len(st.session_state.messages) > 1:
                chat_title = st.session_state.user_code[:20].replace("\n", " ") + "..." if st.session_state.user_code else "Discussion"
                st.session_state.saved_sessions.append({
                    "title": chat_title,
                    "messages": list(st.session_state.messages),
                    "code": st.session_state.user_code,
                    "reflection_done": st.session_state.reflection_done,
                    "final_feedback": st.session_state.final_feedback
                })
            st.session_state.messages = []
            st.session_state.reflection_done = False
            st.session_state.final_feedback = ""
            st.session_state.user_code = ""
            st.rerun()

    st.markdown("---")

    if analyze_btn:
        if not groq_api_key:
            st.error(t["err_no_key"])
        elif not st.session_state.user_code.strip():
            st.warning(t["err_no_code"])
        else:
            try:
                client = Groq(api_key=groq_api_key)

                with st.spinner(t["spinner_analyze"]):
                    system_prompt = f"""
                    You are 'Lumina Code KI', an educational code mentor.
                    Your goal is to help the student ({level}) understand their {language} code/query in mode '{mode}',
                    without giving away the direct solution on a silver platter. Give constructive feedback,
                    explain logic errors or optimization possibilities and offer prompts for thought. Respond in {lang_choice}.
                    """

                    initial_message = f"Analyze this code:\n\n{st.session_state.user_code}"

                    st.session_state.messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": initial_message}
                    ]
                    st.session_state.reflection_done = False
                    st.session_state.final_feedback = ""

                    chat_completion = client.chat.completions.create(
                        messages=st.session_state.messages,
                        model=selected_model,
                        temperature=0.3,
                    )

                    ai_response = chat_completion.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})

            except Exception as e:
                st.error(f"Error: {e}")

    # Chatverlauf anzeigen
    if len(st.session_state.messages) > 1:
        for message in st.session_state.messages:
            if message["role"] == "assistant":
                with st.chat_message("assistant"):
                    st.markdown(message["content"])
            elif message["role"] == "user" and message["content"] != f"Analyze this code:\n\n{st.session_state.user_code}":
                with st.chat_message("user"):
                    st.markdown(message["content"])

        # --- NACHFRAGEFELD FÜR WEITERE FRAGEN ---
        if groq_api_key and not st.session_state.reflection_done:
            if follow_up := st.chat_input(t["chat_input_ph"]):
                st.session_state.messages.append({"role": "user", "content": follow_up})
                with st.chat_message("user"):
                    st.markdown(follow_up)

                try:
                    client = Groq(api_key=groq_api_key)
                    with st.spinner(t["spinner_think"]):
                        chat_completion = client.chat.completions.create(
                            messages=st.session_state.messages,
                            model=selected_model,
                        )
                        ai_response = chat_completion.choices[0].message.content
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                        with st.chat_message("assistant"):
                            st.markdown(ai_response)
                except Exception as e:
                    st.error(f"Error: {e}")

        # --- LERNREFLEXION ---
        st.markdown("---")
        st.markdown(f"### {t['reflection_title']}")
        user_reflection = st.text_area("Reflection input:", placeholder=t["reflection_ph"], key="reflection_input", label_visibility="collapsed")

        if st.button(t["reflection_btn"]):
            if not user_reflection.strip():
                st.warning(t["reflection_warn"])
            else:
                try:
                    client = Groq(api_key=groq_api_key)
                    with st.spinner(t["spinner_feedback"]):
                        reflection_prompt = f"""
                        The student learned and wrote this summary: '{user_reflection}'.
                        Praise the student, briefly evaluate their insight, and give them a motivating closing mentor word in {lang_choice}.
                        """
                        response = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": "You are a motivating, educational code mentor."},
                                {"role": "user", "content": reflection_prompt}
                            ],
                            model=selected_model,
                            temperature=0.4,
                        )
                        st.session_state.final_feedback = response.choices[0].message.content
                        st.session_state.reflection_done = True
                except Exception as e:
                    st.error(f"Error: {e}")

        if st.session_state.reflection_done and st.session_state.final_feedback:
            st.success(t["success_feedback"])
            st.info(st.session_state.final_feedback)

    else:
        st.info(t["info_init"])

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: {sub_color}; font-size: 0.85rem;'>{t['footer']}</p>", unsafe_allow_html=True)