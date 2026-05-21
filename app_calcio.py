import streamlit as st
import time
import datetime
import pandas as pd
import plotly.express as px

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Scout Pro", page_icon="⚽", layout="wide", initial_sidebar_state="collapsed")

# --- CSS MOBILE RESPONSIVE ---
st.markdown("""
    <style>
    /* Tema scuro */
    .stApp {
        background-color: #0E1117 !important;
        color: #FAFAFA !important;
    }
    
    body, p, div, span, label {
        color: #FAFAFA !important;
    }
    
    div[data-testid="stSelectbox"] div {
        color: #FAFAFA !important;
        background-color: #262730 !important;
    }
    
    textarea {
        background-color: #262730 !important;
        color: #FAFAFA !important;
    }
    
    /* Blocco container mobile ottimizzato */
    .block-container {
        padding: 1rem !important;
        padding-bottom: 120px !important;
        max-width: 100% !important;
    }
    
    /* Riduco margini su mobile */
    @media (max-width: 768px) {
        .block-container {
            padding: 0.5rem !important;
            padding-bottom: 120px !important;
        }
    }
    
    /* Bottoni ottimizzati per mobile */
    div.stButton > button {
        font-size: 14px !important;
        height: 50px !important;
        width: 100% !important;
        border-radius: 8px !important;
        margin-bottom: 0.5rem !important;
        color: white !important;
        font-weight: bold !important;
        touch-action: manipulation !important;
    }
    
    /* Bottoni dentro colonne - ridimensiona per 2 colonne */
    div[data-testid="column"] div.stButton > button {
        width: 100% !important;
        font-size: 13px !important;
        height: 48px !important;
        padding: 0.4rem !important;
    }
    
    @media (max-width: 768px) {
        div.stButton > button {
            font-size: 10px !important;
            height: 36px !important;
            padding: 0.3rem !important;
            margin-bottom: 0.25rem !important;
        }
        
        div[data-testid="column"] div.stButton > button {
            font-size: 9px !important;
            height: 34px !important;
            padding: 0.25rem !important;
        }
    }
    
    /* Colori bottoni */
    div.stButton > button:has(p:contains("GOL")) { background-color: #10B981 !important; border: none !important; }
    div.stButton > button:has(p:contains("Tiro")), div.stButton > button:has(p:contains("Passaggio")) { background-color: #3B82F6 !important; border: none !important; }
    div.stButton > button:has(p:contains("Recuperata")), div.stButton > button:has(p:contains("Subito")) { background-color: #06B6D4 !important; border: none !important; }
    div.stButton > button:has(p:contains("Persa")), div.stButton > button:has(p:contains("Commesso")) { background-color: #4B5563 !important; border: none !important; }
    div.stButton > button:has(p:contains("Ammonito")) { background-color: #EAB308 !important; color: black !important; border: none !important; }
    div.stButton > button:has(p:contains("Espulso")) { background-color: #EF4444 !important; border: none !important; }
    div.stButton > button:has(p:contains("Parata")) { background-color: #8B5CF6 !important; border: none !important; }
    div.stButton > button:has(p:contains("CONFERMA")) { background-color: #F97316 !important; border: none !important; }
    div.stButton > button:has(p:contains("PASSA A")) { background-color: #F97316 !important; border: none !important; }
    
    /* Bottoni cronometro compatti */
    .btn-crono button { 
        background-color: #374151 !important; 
        height: 40px !important; 
        font-size: 12px !important;
        margin-bottom: 0.2rem !important;
    }
    
    @media (max-width: 768px) {
        .btn-crono button {
            height: 32px !important;
            font-size: 9px !important;
            margin-bottom: 0.15rem !important;
        }
    }
    
    /* Titolo responsivo */
    .main-title { 
        font-size: 28px !important;
        font-weight: bold; 
        text-align: center; 
        color: #1E3A8A;
        margin-bottom: 1rem !important;
    }
    
    @media (max-width: 768px) {
        .main-title {
            font-size: 22px !important;
            margin-bottom: 0.75rem !important;
        }
    }
    
    /* Banner info match */
    .match-info-banner { 
        background-color: #e5e7eb !important; 
        padding: 12px; 
        border-radius: 12px; 
        border-left: 4px solid #1E3A8A; 
        margin-bottom: 0.5rem;
        font-size: 14px;
    }
    
    .match-info-banner small { 
        color: #374151 !important; 
        font-size: 12px; 
        display: block;
        margin-bottom: 0.3rem;
    }
    
    .match-info-banner strong { 
        color: #1E3A8A !important; 
        font-size: 16px;
        display: block;
    }
    
    @media (max-width: 768px) {
        .match-info-banner {
            padding: 10px;
            margin-bottom: 0.4rem;
        }
        .match-info-banner small {
            font-size: 11px;
        }
        .match-info-banner strong {
            font-size: 14px;
        }
    }
    
    /* Timer inline sotto il banner */
    .timer-inline {
        background-color: #FF4B4B; 
        color: white;
        padding: 8px 16px; 
        border-radius: 20px;
        font-weight: bold; 
        font-size: 16px;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.3);
    }
    
    @media (max-width: 768px) {
        .timer-inline {
            font-size: 14px;
            padding: 6px 12px;
            margin-bottom: 0.75rem;
        }
    }
    
    /* Input text area mobile */
    textarea {
        font-size: 13px !important;
    }
    
    /* Selectbox mobile */
    div[data-testid="stSelectbox"] {
        margin-bottom: 0.5rem !important;
    }
    
    /* Espander mobile */
    .st-expander {
        border-color: #374151 !important;
    }
    
    /* Colonne responsive - stack su mobile */
    @media (max-width: 768px) {
        div[data-testid="column"] {
            flex-direction: column !important;
            width: 100% !important;
        }
    }
    
    /* Metriche responsive */
    [data-testid="metric-container"] {
        padding: 0.75rem !important;
    }
    
    @media (max-width: 768px) {
        [data-testid="metric-container"] {
            padding: 0.5rem !important;
        }
        .metric-label {
            font-size: 11px !important;
        }
    }
    
    /* Tabelle scrollable */
    [data-testid="dataFrame"] {
        font-size: 12px !important;
    }
    
    @media (max-width: 768px) {
        [data-testid="dataFrame"] {
            font-size: 11px !important;
        }
    }
    
    /* Caption minore per mobile */
    .caption-small {
        font-size: 12px;
        padding: 0.5rem 0;
    }
    
    @media (max-width: 768px) {
        .caption-small {
            font-size: 11px;
        }
    }
    
    /* Alert box */
    .stWarning, .stError, .stSuccess {
        font-size: 13px !important;
        padding: 0.75rem !important;
    }
    
    /* Separatore compatto */
    hr {
        margin: 0.5rem 0 !important;
    }
    
    /* Heading compatti */
    h2, h3, h4, h5 {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Spazio superiore per pagina live */
    .live-page-top-space {
        height: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- INIZIALIZZAZIONE STATO ---
if "page" not in st.session_state: st.session_state.page = "setup"
if "match_data" not in st.session_state: st.session_state.match_data = {}
if "crono_stato" not in st.session_state: st.session_state.crono_stato = "Fermo"
if "tempo_gioco" not in st.session_state: st.session_state.tempo_gioco = "1° Tempo"
if "tempo_accumulato" not in st.session_state: st.session_state.tempo_accumulato = 0.0
if "ultimo_avvio" not in st.session_state: st.session_state.ultimo_avvio = None
if "log_strutturato" not in st.session_state: st.session_state.log_strutturato = []
if "in_campo" not in st.session_state: st.session_state.in_campo = []
if "in_panchina" not in st.session_state: st.session_state.in_panchina = []
if "tutti_giocatori_coinvolti" not in st.session_state: st.session_state.tutti_giocatori_coinvolti = []

# ==========================================
# GESTIONE CRONOMETRO FLUIDO (FRAGMENT)
# ==========================================
@st.fragment(run_every=1.0)
def mostra_orologio():
    if st.session_state.crono_stato == "In Corso":
        passato = st.session_state.tempo_accumulato + (time.time() - st.session_state.ultimo_avvio)
    else:
        passato = st.session_state.tempo_accumulato
    
    minuto_calcistico = int(passato // 60) + 1
    m, s = int(passato // 60), int(passato % 60)
    st.markdown(f"<div class='timer-inline'>⏱️ {m:02d}:{s:02d} ({minuto_calcistico}')</div>", unsafe_allow_html=True)

# ==========================================
# 1. PAGINA INIZIALE (SETUP)
# ==========================================
if st.session_state.page == "setup":
    st.markdown("<p class='main-title'>🆕 Nuovo Match</p>", unsafe_allow_html=True)
    
    data_match = st.date_input("📅 Data della partita", datetime.date.today())
    competizione = st.text_input("🏆 Competizione", placeholder="Es. Serie D, Promozione...")
    
    col_sq1, col_sq2 = st.columns(2)
    with col_sq1: 
        casa = st.text_input("🏠 Casa", placeholder="Casa")
    with col_sq2: 
        trasferta = st.text_input("✈️ Trasferta", placeholder="Trasferta")
    
    st.write("---")
    
    col_dist1, col_dist2 = st.columns(2)
    with col_dist1:
        titolari_input = st.text_area("📋 TITOLARI (uno per riga)", 
                                       value="1.", height=120)
    with col_dist2:
        panchina_input = st.text_area("🪑 PANCHINA (uno per riga)", 
                                       value="12.", height=120)
        
    portieri_input = st.text_input("🧤 Portieri (separati da virgola se più di uno)", 
                                   value="1.")
    
    st.write("---")
    if st.button("🚀 PROCEDI AL MATCH", use_container_width=True):
        if casa and trasferta:
            tits = [g.strip() for g in titolari_input.split("\n") if g.strip()]
            pancs = [g.strip() for g in panchina_input.split("\n") if g.strip()]
            
            st.session_state.match_data = {
                "data": data_match,
                "competizione": competizione,
                "casa": casa,
                "trasferta": trasferta,
                "portieri": [p.strip() for p in portieri_input.split(",") if p.strip()]
            }
            st.session_state.in_campo = tits.copy()
            st.session_state.in_panchina = pancs.copy()
            st.session_state.tutti_giocatori_coinvolti = sorted(list(set(tits + pancs)))
            
            st.session_state.page = "live"
            st.session_state.tempo_gioco = "1° Tempo"
            st.session_state.tempo_accumulato = 0.0
            st.session_state.log_strutturato = [] 
            st.rerun()
        else:
            st.error("❌ Inserisci i nomi delle squadre!")

# ==========================================
# 2. PAGINA LIVE (RACCOLTA DATI)
# ==========================================
elif st.session_state.page == "live":
    # Aggiungi spazio superiore per evitare che il contenuto sia coperto
    st.markdown("<div class='live-page-top-space'></div>", unsafe_allow_html=True)
    
    md = st.session_state.match_data

    st.markdown(f"""
        <div class='match-info-banner'>
            <small>{md['data']} - {md['competizione']} ({st.session_state.tempo_gioco})</small>
            <strong>{md['casa']} vs {md['trasferta']}</strong>
        </div>
    """, unsafe_allow_html=True)

    # Recupero del tempo per calcolo minuto dell'evento
    if st.session_state.crono_stato == "In Corso":
        passato_corrente = st.session_state.tempo_accumulato + (time.time() - st.session_state.ultimo_avvio)
    else:
        passato_corrente = st.session_state.tempo_accumulato
    minuto_calcistico = int(passato_corrente // 60) + 1

    # Avvio del fragment orologio in background (ora inline sotto il banner)
    mostra_orologio()

    # Controlli cronometro - 3 bottoni su una riga
    col_t1, col_t2, col_t3 = st.columns(3)
    
    with col_t1:
        st.markdown('<div class="btn-crono">', unsafe_allow_html=True)
        if st.button("▶️ Inizio", use_container_width=True, disabled=(st.session_state.crono_stato != "Fermo")):
            st.session_state.crono_stato = "In Corso"
            st.session_state.ultimo_avvio = time.time()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_t2:
        st.markdown('<div class="btn-crono">', unsafe_allow_html=True)
        if st.button("🔄 Riprendi", use_container_width=True, disabled=(st.session_state.crono_stato != "Interrotto")):
            st.session_state.crono_stato = "In Corso"
            st.session_state.ultimo_avvio = time.time()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_t3:
        st.markdown('<div class="btn-crono">', unsafe_allow_html=True)
        if st.button("⏹️ Fine", use_container_width=True, disabled=(st.session_state.crono_stato == "Fermo" and st.session_state.tempo_accumulato == 0.0)):
            st.session_state.page = "report" 
            st.session_state.crono_stato = "Fermo"
            st.session_state.ultimo_avvio = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Intervallo - bottone grande
    if st.session_state.tempo_gioco == "1° Tempo":
        if st.button("⏸️ PASSA A INTERVALLO / 2° TEMPO", use_container_width=True):
            if st.session_state.crono_stato == "In Corso":
                st.session_state.tempo_accumulato += time.time() - st.session_state.ultimo_avvio
            st.session_state.tempo_gioco = "2° Tempo"
            st.session_state.crono_stato = "Fermo"
            st.session_state.tempo_accumulato = 45.0 * 60.0
            st.rerun()

    st.write("---")

    # Selezione giocatore - full width su mobile
    if st.session_state.in_campo:
        giocatore_scelto = st.selectbox("👤 Seleziona Giocatore in Campo:", st.session_state.in_campo)
        is_portiere = giocatore_scelto in md['portieri']
    else:
        st.error("🔴 Nessun giocatore rimasto in campo!")
        giocatore_scelto = None
        is_portiere = False

    # Sostituzione in expander
    with st.expander("🔄 Effettua una Sostituzione", expanded=False):
        if st.session_state.in_panchina and giocatore_scelto:
            giocatore_entrante = st.selectbox("🪑 Chi entra dalla panchina?", st.session_state.in_panchina, key="sub")
            if st.button("📥 CONFERMA CAMBIO", use_container_width=True):
                evento_cambio = {
                    "Data": md['data'].strftime('%Y-%m-%d'),
                    "Competizione": md['competizione'],
                    "Partita": f"{md['casa']} - {md['trasferta']}",
                    "Tempo": st.session_state.tempo_gioco,
                    "Minuto": minuto_calcistico,
                    "Giocatore": giocatore_scelto,
                    "Evento": f"🔄 SOSTITUITO (Entra {giocatore_entrante})"
                }
                st.session_state.log_strutturato.insert(0, evento_cambio)
                st.session_state.in_campo.remove(giocatore_scelto)
                st.session_state.in_campo.append(giocatore_entrante)
                st.session_state.in_panchina.remove(giocatore_entrante)
                st.success(f"✅ {giocatore_scelto} → {giocatore_entrante}")
                time.sleep(0.3)
                st.rerun()
        else:
            st.warning("⚠️ Impossibile effettuare sostituzioni.")

    st.markdown("### ⚡ Registra Evento")
    disabilitato = (st.session_state.crono_stato != "In Corso" or giocatore_scelto is None)
    if st.session_state.crono_stato != "In Corso":
        st.warning("⚠️ Avvia il cronometro per registrare gli eventi!")

    evento_registrato = None
    forzare_rimozione_espulso = False

    # Bottoni portiere
    if is_portiere and giocatore_scelto:
        st.markdown("##### 🧤 Ruolo Portiere")
        riga_p1, riga_p2 = st.columns(2)
        with riga_p1:
            if st.button("👐 Parata", use_container_width=True, disabled=disabilitato): 
                evento_registrato = "Parata"
        with riga_p2:
            if st.button("🥅 Gol Subito", use_container_width=True, disabled=disabilitato): 
                evento_registrato = "Gol Subito"
        st.write("---")

    # Bottoni evento - griglia 2 colonne (coppie di bottoni)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⚽ GOL!", use_container_width=True, disabled=disabilitato): 
            evento_registrato = "GOL"
    with c2:
        if st.button("❌ Tiro Fuori", use_container_width=True, disabled=disabilitato): 
            evento_registrato = "Tiro Fuori"

    c3, c4 = st.columns(2)
    with c3:
        if st.button("🎯 Tiro in Porta", use_container_width=True, disabled=disabilitato): 
            evento_registrato = "Tiro in Porta"
    with c4:
        if st.button("👟 Pass Chiave", use_container_width=True, disabled=disabilitato): 
            evento_registrato = "Passaggio Chiave"

    c5, c6 = st.columns(2)
    with c5:
        if st.button("🔄 Palla Rec.", use_container_width=True, disabled=disabilitato): 
            evento_registrato = "Palla Recuperata"
    with c6:
        if st.button("📉 Palla Persa", use_container_width=True, disabled=disabilitato): 
            evento_registrato = "Palla Persa"

    c7, c8 = st.columns(2)
    with c7:
        if st.button("💥 Fallo Subito", use_container_width=True, disabled=disabilitato): 
            evento_registrato = "Fallo Subito"
    with c8:
        if st.button("🛑 Fallo Fatto", use_container_width=True, disabled=disabilitato): 
            evento_registrato = "Fallo Commesso"

    c9, c10 = st.columns(2)
    with c9:
        if st.button("🟨 Ammonito", use_container_width=True, disabled=disabilitato): 
            evento_registrato = "Ammonito"
    with c10:
        if st.button("🟥 Espulso", use_container_width=True, disabled=disabilitato): 
            evento_registrato = "Espulso"
            forzare_rimozione_espulso = True

    # Registra evento
    if evento_registrato and giocatore_scelto:
        dati_evento = {
            "Data": md['data'].strftime('%Y-%m-%d'),
            "Competizione": md['competizione'],
            "Partita": f"{md['casa']} - {md['trasferta']}",
            "Tempo": st.session_state.tempo_gioco,
            "Minuto": minuto_calcistico,
            "Giocatore": giocatore_scelto,
            "Evento": evento_registrato
        }
        st.session_state.log_strutturato.insert(0, dati_evento)
        
        if forzare_rimozione_espulso:
            st.session_state.in_campo.remove(giocatore_scelto)
            st.toast(f"🟥 {giocatore_scelto} ESPULSO!")
        else:
            st.toast(f"✅ {evento_registrato}")
        
        time.sleep(0.2)
        st.rerun()

    # Ultimi eventi
    if st.session_state.log_strutturato:
        st.write("---")
        st.markdown("##### 📝 Ultimi Eventi:")
        for ev in st.session_state.log_strutturato[:5]:
            st.markdown(f"<div class='caption-small'><strong>{ev['Minuto']}'</strong> ({ev['Tempo']}) | {ev['Giocatore']}: **{ev['Evento']}**</div>", unsafe_allow_html=True)

# ==========================================
# 3. PAGINA DI REPORT, GRAFICI E ANALISI
# ==========================================
elif st.session_state.page == "report":
    st.markdown("<p class='main-title'>📊 Analisi Match</p>", unsafe_allow_html=True)
    
    if st.session_state.log_strutturato:
        df_completo = pd.DataFrame(st.session_state.log_strutturato)
        
        st.markdown("### 🔍 Filtra Analisi")
        filtro_tempo = st.radio(
            "Seleziona frazione di gioco:", 
            ["Intera Partita", "Solo 1° Tempo", "Solo 2° Tempo"], 
            horizontal=True
        )
        
        if filtro_tempo == "Solo 1° Tempo":
            df = df_completo[df_completo["Tempo"] == "1° Tempo"]
        elif filtro_tempo == "Solo 2° Tempo":
            df = df_completo[df_completo["Tempo"] == "2° Tempo"]
        else:
            df = df_completo

        tot_gol = len(df[df["Evento"] == "GOL"])
        tot_porta = len(df[df["Evento"] == "Tiro in Porta"])
        tot_fuori = len(df[df["Evento"] == "Tiro Fuori"])
        tot_tiri = tot_gol + tot_porta + tot_fuori
        tot_recuperi = len(df[df["Evento"] == "Palla Recuperata"])
        tot_perse = len(df[df["Evento"] == "Palla Persa"])
        
        st.markdown("### 📈 Numeri di Squadra")
        cm1, cm2, cm3, cm4 = st.columns(4)
        cm1.metric("⚽ Gol", tot_gol)
        cm2.metric("🎯 Tiri", tot_tiri)
        cm3.metric("🔄 Rec.", tot_recuperi)
        cm4.metric("📉 Perse", tot_perse)
        
        st.write("---")
        col_graf1, col_graf2 = st.columns(2)
        
        with col_graf1:
            st.markdown("##### 🎯 Tiri")
            df_tiri = df[df["Evento"].isin(["GOL", "Tiro in Porta", "Tiro Fuori"])]
            if not df_tiri.empty:
                conteggio_tiri = df_tiri["Evento"].value_counts().reset_index()
                conteggio_tiri.columns = ["Tipo Tiro", "Conteggio"]
                colori_mappa = {"GOL": "#10B981", "Tiro in Porta": "#3B82F6", "Tiro Fuori": "#EF4444"}
                fig = px.pie(conteggio_tiri, values="Conteggio", names="Tipo Tiro", color="Tipo Tiro", color_discrete_map=colori_mappa, hole=0.3)
                fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=True, height=300)
                st.plotly_chart(fig, use_container_width=True, config={'responsive': True})
            else:
                st.caption("Nessun tiro registrato.")
                
        with col_graf2:
            st.markdown("##### 🔄 Possesso")
            df_poss_squadra = pd.DataFrame({
                "Fase": ["Rec.", "Perse"],
                "Totale": [tot_recuperi, tot_perse]
            })
            if tot_recuperi > 0 or tot_perse > 0:
                fig_poss = px.bar(df_poss_squadra, x="Fase", y="Totale", color="Fase", color_discrete_map={"Rec.": "#06B6D4", "Perse": "#4B5563"})
                fig_poss.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=False, xaxis_title=None, yaxis_title=None, height=300)
                st.plotly_chart(fig_poss, use_container_width=True, config={'responsive': True})
            else:
                st.caption("Nessun dato di possesso.")

        st.write("---")
        st.markdown("### 👤 KPI Individuali")
        giocatore_kpi = st.selectbox("Scegli Giocatore:", st.session_state.tutti_giocatori_coinvolti)
        df_singolo = df[df["Giocatore"] == giocatore_kpi]
        
        g_gol = len(df_singolo[df_singolo["Evento"] == "GOL"])
        g_in_porta = len(df_singolo[df_singolo["Evento"] == "Tiro in Porta"])
        g_fuori = len(df_singolo[df_singolo["Evento"] == "Tiro Fuori"])
        g_tiri = g_gol + g_in_porta + g_fuori
        g_chiave = len(df_singolo[df_singolo["Evento"] == "Passaggio Chiave"])
        g_recuperate = len(df_singolo[df_singolo["Evento"] == "Palla Recuperata"])
        g_perse = len(df_singolo[df_singolo["Evento"] == "Palla Persa"])
        g_subiti = len(df_singolo[df_singolo["Evento"] == "Fallo Subito"])
        g_commessi = len(df_singolo[df_singolo["Evento"] == "Fallo Commesso"])
        g_ammo = len(df_singolo[df_singolo["Evento"] == "Ammonito"])
        g_espu = len(df_singolo[df_singolo["Evento"] == "Espulso"])
        g_parate = len(df_singolo[df_singolo["Evento"] == "Parata"])
        
        ck1, ck2, ck3, ck4 = st.columns(4)
        ck1.metric("Gol", g_gol)
        ck2.metric("Tiri", f"{g_tiri} ({g_in_porta})")
        ck3.metric("Rec.", g_recuperate)
        ck4.metric("Perse", g_perse)
        
        ck5, ck6, ck7, ck8 = st.columns(4)
        ck5.metric("Pass Ch.", g_chiave)
        ck6.metric("Falli", f"{g_subiti}/{g_commessi}")
        ck7.metric("Cartellini", f"{g_ammo}/{g_espu}")
        if g_parate > 0 or giocatore_kpi in st.session_state.match_data['portieri']:
            ck8.metric("Parate", g_parate)
        else:
            stato = "In Campo" if giocatore_kpi in st.session_state.in_campo else "Panchina"
            ck8.metric("Stato", stato)
            
        if not df_singolo.empty:
            st.markdown("**Cronologia azioni:**")
            eventi_brevi = [f"{row['Minuto']}' - {row['Evento']}" for _, row in df_singolo.iterrows()]
            st.markdown(", ".join(eventi_brevi), unsafe_allow_html=False)

        st.write("---")
        st.markdown("### 📋 Tabella Eventi")
        
        # Tabella con scroll orizzontale su mobile
        df_display = df_completo[["Tempo", "Minuto", "Giocatore", "Evento"]].copy()
        df_display["Minuto"] = df_display["Minuto"].astype(int)
        st.dataframe(df_display, use_container_width=True, height=300)
        
        csv = df_completo.to_csv(index=False).encode('utf-8')
        nome_file = f"scout_{st.session_state.match_data['casa']}_vs_{st.session_state.match_data['trasferta']}.csv"
        st.download_button(
            label="📥 SCARICA CSV", 
            data=csv, 
            file_name=nome_file, 
            mime='text/csv',
            use_container_width=True
        )
        
    st.write("---")
    if st.button("🔄 Nuovo Match", use_container_width=True):
        st.session_state.page = "setup"
        st.session_state.log_strutturato = []
        st.rerun()
