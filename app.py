import streamlit as st
from groq import Groq

# Seitenkonfiguration
st.set_page_config(
    page_title="Lumina Code KI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ULTRA-MODERNES CSS (Glassmorphism & Neon-Design) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #13182b 50%, #07090e 100%);
        color: #f3f4f6;
    }
    footer {visibility: hidden;}

    .hero-container {
        padding: 2rem 1rem 1rem 1rem;
        text-align: center;
    }
    .main-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #a5b4fc 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -1.5px;
    }
    .sub-title {
        color: #9ca3af;
        font-size: 1.25rem;
        font-weight: 400;
        max-width: 600px;
        margin: 0 auto 2rem auto;
    }

    .glass-card {
        background: rgba(25, 30, 48, 0.6);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        border-radius: 14px;
        padding: 0.85rem 1.5rem;
        border: none;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(168, 85, 247, 0.6);
    }

    .stTextArea textarea, .stSelectbox div[data-baseweb="select"], .stTextInput input {
        background-color: rgba(15, 20, 35, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALISIERUNG DES CHAT-VERLAUFS ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "reflection_done" not in st.session_state:
    st.session_state.reflection_done = False
if "final_feedback" not in st.session_state:
    st.session_state.final_feedback = ""

# --- SEITENLEISTE (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #a5b4fc;'>⚡ Lumina Control</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # API-Key Eingabe
    groq_api_key = st.text_input("🔑 Groq API-Key:", type="password", placeholder="gsk_...")
    
    st.markdown("---")
    selected_model = st.selectbox("🤖 KI-Modell:", ["llama3-70b-8192", "llama3-8b-8192"])
    mode = st.selectbox("🧠 Lernmodus:", ["Pädagogischer Mentor (Tipps)", "Direkter Debugger", "Code Optimizer"])
    level = st.select_slider("📈 Schwierigkeitsgrad:", options=["Anfänger", "Fortgeschritten", "Experte"])
    
    st.markdown("---")
    if st.button("🗑️ Session zurücksetzen"):
        st.session_state.messages = []
        st.session_state.reflection_done = False
        st.session_state.final_feedback = ""
        st.rerun()
        
    st.markdown("### 🚀 Systemstatus")
    if groq_api_key:
        st.success("API-Key erkannt & bereit.")
    else:
        st.warning("Bitte gib deinen Groq API-Key ein.")

# --- HAUPTÜBERSCHRIFT ---
st.markdown("""
    <div class="hero-container">
        <h1 class="main-title">✨ Lumina Code KI</h1>
        <p class="sub-title">Dein intelligenter, KI-gestützter Code-Mentor für tiefe Einblicke und echten Lerneffekt.</p>
    </div>
""", unsafe_allow_html=True)

# --- ZENTRALES LAYOUT IN SPALTEN ---
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 💻 Quellcode & Abfrage Eingabe")
    language = st.selectbox("Programmiersprache / Abfragesprache:", ["Python", "SQL", "C", "C++", "Java", "JavaScript", "TypeScript"])
    user_code = st.text_area("Füge deinen Code oder deine SQL-Abfrage hier ein:", height=300, placeholder="-- Beispiel SQL:\nSELECT name, email FROM users WHERE active = 1;")
    
    analyze_btn = st.button("Code analysieren & verstehen 🚀")
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 KI-Analyse & Interaktiver Chat")
    
    if analyze_btn:
        if not groq_api_key:
            st.error("⚠️ Bitte gib zuerst deinen Groq API-Key in der Seitenleiste ein!")
        elif not user_code.strip():
            st.warning("⚠️ Bitte gib zuerst etwas Code ein!")
        else:
            try:
                client = Groq(api_key=groq_api_key)
                
                with st.spinner("✨ Lumina KI analysiert den Code..."):
                    system_prompt = f"""
                    Du bist 'Lumina Code KI', ein pädagogischer Code-Mentor. 
                    Dein Ziel ist es, dem Schüler ({level}) zu helfen, seinen {language}-Code bzw. seine Abfrage im Modus '{mode}' zu verstehen, 
                    ohne ihm direkt die fertige Lösung auf dem Silbertablett zu servieren. Gib konstruktives Feedback, 
                    erkläre Logikfehler oder Optimierungsmöglichkeiten und stelle Denkanstöße. Antworte strukturiert auf Deutsch.
                    """
                    
                    initial_message = f"Analysiere diesen Code:\n\n{user_code}"
                    
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
                st.error(f"Ein Fehler ist aufgetreten: {e}")

    # Anzeige des Chat-Verlaufs
    if len(st.session_state.messages) > 1:
        for message in st.session_state.messages:
            if message["role"] == "assistant":
                with st.chat_message("assistant", avatar="✨"):
                    st.markdown(message["content"])
            elif message["role"] == "user" and message["content"] != f"Analysiere diesen Code:\n\n{user_code}":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(message["content"])
                    
        # Eingabefeld für Folgefragen
        if groq_api_key and not st.session_state.reflection_done:
            if follow_up := st.chat_input("Stelle eine Frage zum Code oder zur Analyse..."):
                st.session_state.messages.append({"role": "user", "content": follow_up})
                with st.chat_message("user", avatar="👤"):
                    st.markdown(follow_up)
                    
                try:
                    client = Groq(api_key=groq_api_key)
                    with st.spinner("✨ Lumina KI denkt nach..."):
                        chat_completion = client.chat.completions.create(
                            messages=st.session_state.messages,
                            model=selected_model,
                            temperature=0.3,
                        )
                        ai_response = chat_completion.choices[0].message.content
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                        with st.chat_message("assistant", avatar="✨"):
                            st.markdown(ai_response)
                except Exception as e:
                    st.error(f"Ein Fehler ist aufgetreten: {e}")

        # --- LERNREFLEXION & ABSCHLUSS ---
        st.markdown("---")
        st.markdown("### 📝 Lernreflexion & Abschluss")
        user_reflection = st.text_area("Fasse in eigenen Worten zusammen, was du gelernt hast:", placeholder="Heute habe ich gelernt, dass...", key="reflection_input")
        
        if st.button("Reflexion abschicken & Abschlusswort erhalten ✨"):
            if not user_reflection.strip():
                st.warning("⚠️ Bitte schreibe kurz, was du gelernt hast.")
            else:
                try:
                    client = Groq(api_key=groq_api_key)
                    with st.spinner("✨ Lumina formuliert das Abschlusswort..."):
                        reflection_prompt = f"""
                        Der Schüler hat gelernt und folgende Zusammenfassung geschrieben: '{user_reflection}'.
                        Lobe den Schüler, bewerte kurz seine Einsicht und gib ihm ein motivierendes, professionelles Abschlusswort als Code-Mentor auf Deutsch.
                        """
                        response = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": "Du bist ein motivierender, pädagogischer Code-Mentor."},
                                {"role": "user", "content": reflection_prompt}
                            ],
                            model=selected_model,
                            temperature=0.4,
                        )
                        st.session_state.final_feedback = response.choices[0].message.content
                        st.session_state.reflection_done = True
                except Exception as e:
                    st.error(f"Ein Fehler ist aufgetreten: {e}")
                    
        if st.session_state.reflection_done and st.session_state.final_feedback:
            st.success("🎉 Hervorragende Arbeit! Hier ist dein Mentor-Abschlusswort:")
            st.markdown(f"""
                <div style='background: rgba(168, 85, 247, 0.1); border-left: 4px solid #c084fc; padding: 15px; border-radius: 8px; margin-top: 10px;'>
                    {st.session_state.final_feedback}
                </div>
            """, unsafe_allow_html=True)

    else:
        st.info("👈 Trage deinen API-Key ein, füge links deinen Code ein und klicke auf 'Code analysieren & verstehen'.")

    st.markdown('</div>', unsafe_allow_html=True)

# --- FUSSTEXT ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4b5563; font-size: 0.85rem;'>Lumina Code KI Core v1.0 • Sichere & intelligente Umgebung</p>", unsafe_allow_html=True)