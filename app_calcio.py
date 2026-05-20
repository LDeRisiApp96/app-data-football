import streamlit as st
import time
import datetime
import pandas as pd
import plotly.express as px

# --- CONFIGURAZIONE PAGINA MOBILE-FIRST ---
st.set_page_config(page_title="Scout Pro", page_icon="⚽", layout="centered")

# --- CSS ULTRA-COMPATTO PER SMARTPHONE ---
st.markdown("""
    <style>
    /* Riduciamo i margini generali per guadagnare spazio sullo schermo */
    .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; padding-left: 0.5rem !important; padding-right: 0.5rem !important; }
    
    /* Bottoni Evento: compatti, quadrati e perfetti per il pollice */
    div.stButton > button {
        font-size: 14px !important;
        height: 48px !important;
        width: 100% !important;
        border-radius: 8px !important;
        margin-bottom: -5px !important;
        color: white !important;
        font-weight: bold !important;
        padding: 2px 2px !important;
    }
    
    /* Colori dei bottoni basati sul testo contenuto */
    div.stButton > button:has(p:contains("⚽")) { background-color: #10B981 !important; border: none !important; }
    div.stButton > button:has(p:contains("🎯")), div.stButton > button:has(p:contains("👟")) { background-color: #3B82F6 !important; border: none !important; }
    div.stButton > button:has(p:contains("🔄")), div.stButton > button:has(p:contains("💥")) { background-color: #06B6D4 !important; border: none !important; }
    div.stButton > button:has(p:contains("❌")), div.stButton > button:has(p:contains("📉")), div.stButton > button:has(p:contains("🛑")) { background-color: #4B5563 !important; border: none !important; }
    div.stButton > button:has(p:contains("🟨")) { background-color: #EAB308 !important; color: black !important; border: none !important; }
    div.stButton > button:has(p:contains("🟥")) { background-color: #EF4444 !important; border: none !important; }
    div.stButton > button:has(p:contains("👐")), div.stButton > button:has(p:contains("🥅")) { background-color: #8B5CF6 !important; border: none !important; }
    
    /* Bottoni di controllo cronometro più piccoli */
    .btn-crono button { background-color: #374151 !important; height: 35px !important; font-size: 12px !important; }
    
    /* Banner info ridotto al minimo */
    .match-info-mini { 
        background-color: #f3f4f6 !important; 
        padding: 8px; 
        border-radius: 8px; 
        text-align: center;
        margin-bottom: 10px;
        font-size: 14px;
        font-weight: bold;
        color: #1E3A8A;
    }
    
    /* Timer fisso in alto a destra molto discreto */
    .timer-top-right {
        position: fixed; top: 10px; right: 10px;
        background-color: #FF4B4B; color: white;
        padding: 3px 10px; border-radius: 12px;
        font-weight: bold; font-size: 13px;
        z-index: 9999; box-shadow: 0px 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Riduzione spazi dei selettori */
    div[data-testid="stSelectbox"] { margin-bottom: -10px !important; }
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

# --- TIMER AD ALTA VELOCITÀ ---
@st.fragment(run_every=1.0)
def mostra_orologio():
    if st.session_state.crono_stato == "In Corso":
        passato = st.session_state.tempo_accumulato + (time.time() - st.session_state.ultimo_avvio)
    else:
        passato = st.session_state.tempo_accumulato
    minuto_calcistico = int(passato // 60) + 1
    m, s = int(passato // 60), int(passato % 60)
    st.markdown(f"<div class='timer-top-right'>⏱️ {m:02d}:{s:02d} ({minuto_calcistico}')</div>", unsafe_allow_html=True)

# ==========================================
# 1. SETUP MATCH (OTTIMIZZATO)
# ==========================================
if st.session_state.page == "setup":
    st.markdown("### ⚽ Configura Match")
    data_match = st.date_input("Data", datetime.date.today())
    competizione = st.text_input("Competizione", value="Campionato")
    
    c_c1, c_c2 = st.columns(2)
    with c_c1: casa = st.text_input("Casa", value="Team A")
    with c_c2: trasferta = st.text_input("Trasf.", value="Team B")
    
    titolari_input = st.text_area("📋 Titolari (uno per riga)", value="1. Provedel\n4. Rossi\n8. Ferrari\n9. Bianchi\n10. Verdi", height=100)
    panchina_input = st.text_area("🪑 Panchina (uno per riga)", value="12. Alisson\n14. Neri\n18. Viola", height=100)
    portieri_input = st.text_input("Portieri (separati da virgola)", value="1. Provedel, 12. Alisson")
    
    if st.button("🚀 AVVIA DASHBOARD LIVE"):
        if casa and trasferta:
            tits = [g.strip() for g in titolari_input.split("\n") if g.strip()]
            pancs = [g.strip() for g in panchina_input.split("\n") if g.strip()]
            st.session_state.match_data = {
                "data": data_match, "competizione": competizione, "casa": casa, "trasferta": trasferta,
                "portieri": [p.strip() for p in portieri_input.split(",") if p.strip()]
            }
            st.session_state.in_campo = tits.copy()
            st.session_state.in_panchina = pancs.copy()
            st.session_state.tutti_giocatori_coinvolti = sorted(list(set(tits + pancs)))
            st.session_state.page = "live"
            st.rerun()

# ==========================================
# 2. INTERFACCIA LIVE MOBILE-FIRST
# ==========================================
elif st.session_state.page == "live":
    md = st.session_state.match_data
    mostra_orologio()
    
    # Intestazione ultra-compatta
    st.markdown(f"<div class='match-info-mini'>{md['casa']} - {md['trasferta']} ({st.session_state.tempo_gioco})</div>", unsafe_allow_html=True)

    # Calcolo minuto corrente per il log interno
    if st.session_state.crono_stato == "In Corso":
        passato_corrente = st.session_state.tempo_accumulato + (time.time() - st.session_state.ultimo_avvio)
    else:
        passato_corrente = st.session_state.tempo_accumulato
    minuto_calcistico = int(passato_corrente // 60) + 1

    # Cronometro Micro
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    with col_t1:
        st.markdown('<div class="btn-crono">', unsafe_allow_html=True)
        if st.button("▶️ Start", disabled=(st.session_state.crono_stato != "Fermo")):
            st.session_state.crono_stato = "In Corso"; st.session_state.ultimo_avvio = time.time(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_t2:
        st.markdown('<div class="btn-crono">', unsafe_allow_html=True)
        if st.button("⏸️ Pausa", disabled=(st.session_state.crono_stato != "In Corso")):
            st.session_state.crono_stato = "Interrotto"; st.session_state.tempo_accumulato += time.time() - st.session_state.ultimo_avvio; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_t3:
        st.markdown('<div class="btn-crono">', unsafe_allow_html=True)
        if st.button("🔄 Ripr.", disabled=(st.session_state.crono_stato != "Interrotto")):
            st.session_state.crono_stato = "In Corso"; st.session_state.ultimo_avvio = time.time(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_t4:
        st.markdown('<div class="btn-crono">', unsafe_allow_html=True)
        if st.button("⏹️ Fine", disabled=(st.session_state.crono_stato == "Fermo" and st.session_state.tempo_accumulato == 0.0)):
            st.session_state.page = "report"; st.session_state.crono_stato = "Fermo"; st.session_state.ultimo_avvio = None; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Selezione Giocatore (Spazio Ottimizzato)
    if st.session_state.in_campo:
        giocatore_scelto = st.selectbox("👤 In Campo:", st.session_state.in_campo, label_visibility="collapsed")
        is_portiere = giocatore_scelto in md['portieri']
    else:
        st.error("Nessun giocatore in campo")
        giocatore_scelto = None
        is_portiere = False

    # GRIGLIA EVENTI COMPATTA A DUE COLONNE
    st.write("")
    disabilitato = (st.session_state.crono_stato != "In Corso" or giocatore_scelto is None)
    
    evento_registrato = None
    forzare_rimozione_espulso = False

    # Sezione Portiere Condizionale e super stretta
    if is_portiere and giocatore_scelto:
        p1, p2 = st.columns(2)
        with p1:
            if st.button("👐 Parata", disabled=disabilitato): evento_registrato = "Parata"
        with p2:
            if st.button("🥅 Gol Subito", disabled=disabilitato): evento_registrato = "Gol Subito"

    c1, c2 = st.columns(2)
    with c1:
        if st.button("⚽ GOL!", disabled=disabilitato): evento_registrato = "GOL"
    with c2:
        if st.button("❌ Tiro Fuori", disabled=disabilitato): evento_registrato = "Tiro Fuori"

    c3, c4 = st.columns(2)
    with c3:
        if st.button("🎯 In Porta", disabled=disabilitato): evento_registrato = "Tiro in Porta"
    with c4:
        if st.button("👟 Pass. Chiave", disabled=disabilitato): evento_registrato = "Passaggio Chiave"

    c5, c6 = st.columns(2)
    with c5:
        if st.button("🔄 Palla Rec.", disabled=disabilitato): evento_registrato = "Palla Recuperata"
    with c6:
        if st.button("📉 Palla Persa", disabled=disabilitato): evento_registrato = "Palla Persa"

    c7, c8 = st.columns(2)
    with c7:
        if st.button("💥 Fallo Sub.", disabled=disabilitato): evento_registrato = "Fallo Subito"
    with c8:
        if st.button("🛑 Fallo Comm.", disabled=disabilitato): evento_registrato = "Fallo Commesso"

    c9, c10 = st.columns(2)
    with c9:
        if st.button("🟨 Ammonito", disabled=disabilitato): evento_registrato = "Ammonito"
    with c10:
        if st.button("🟥 Espulso", disabled=disabilitato): 
            evento_registrato = "Espulso"
            forzare_rimozione_espulso = True

    # Logica di salvataggio istantanea
    if evento_registrato and giocatore_scelto:
        st.session_state.log_strutturato.insert(0, {
            "Data": md['data'].strftime('%Y-%m-%d'), "Competizione": md['competizione'], "Partita": f"{md['casa']}-{md['trasferta']}",
            "Tempo": st.session_state.tempo_gioco, "Minuto": minuto_calcistico, "Giocatore": giocatore_scelto, "Evento": evento_registrato
        })
        if forzare_rimozione_espulso:
            st.session_state.in_campo.remove(giocatore_scelto)
            st.toast(f"🟥 {giocatore_scelto} Rimosso!")
        else:
            st.toast(f"OK: {giocatore_scelto} -> {evento_registrato}")
        time.sleep(0.1)
        st.rerun()

    # Opzioni secondarie nascoste in expander per liberare lo schermo
    st.write("---")
    with st.expander("🔄 Effettua Sostituzione"):
        if st.session_state.in_panchina and giocatore_scelto:
            giocatore_entrante = st.selectbox("🪑 Panchina:", st.session_state.in_panchina)
            if st.button("📥 CONFERMA CAMBIO"):
                st.session_state.log_strutturato.insert(0, {
                    "Data": md['data'].strftime('%Y-%m-%d'), "Competizione": md['competizione'], "Partita": f"{md['casa']}-{md['trasferta']}",
                    "Tempo": st.session_state.tempo_gioco, "Minuto": minuto_calcistico, "Giocatore": giocatore_scelto, "Evento": f"🔄 CAMBIO (Entra {giocatore_entrante})"
                })
                st.session_state.in_campo.remove(giocatore_scelto)
                st.session_state.in_campo.append(giocatore_entrante)
                st.session_state.in_panchina.remove(giocatore_entrante)
                st.rerun()

    with st.expander("⏱️ Gestione Tempi"):
        if st.session_state.tempo_gioco == "1° Tempo":
            if st.button("⏸️ PASSA A INTERVALLO / 2° TEMPO"):
                if st.session_state.crono_stato == "In Corso":
                    st.session_state.tempo_accumulato += time.time() - st.session_state.ultimo_avvio
                st.session_state.tempo_gioco = "2° Tempo"; st.session_state.crono_stato = "Fermo"; st.session_state.tempo_accumulato = 45.0 * 60.0
                st.rerun()

    if st.session_state.log_strutturato:
        with st.expander("📝 Ultimi Eventi (Registro)"):
            for ev in st.session_state.log_strutturato[:4]:
                st.caption(f"{ev['Minuto']}' | {ev['Giocatore']}: {ev['Evento']}")

# ==========================================
# 3. REPORT FINALE (GRAFICI RESPONSIVE)
# ==========================================
elif st.session_state.page == "report":
    st.markdown("### 📊 Analisi Match")
    if st.session_state.log_strutturato:
        df = pd.DataFrame(st.session_state.log_strutturato)
        
        st.metric("Gol Fatti", len(df[df["Evento"] == "GOL"]))
        st.metric("Tiri Totali", len(df[df["Evento"].isin(["GOL", "Tiro in Porta", "Tiro Fuori"])]))
        
        st.write("---")
        st.markdown("##### 👤 Statistiche Giocatore")
        giocatore_kpi = st.selectbox("Scegli:", st.session_state.tutti_giocatori_coinvolti)
        df_g = df[df["Giocatore"] == giocatore_kpi]
        st.dataframe(df_g[["Minuto", "Evento"]], use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 SCARICA CSV", data=csv, file_name="scout.csv", mime='text/csv')
    
    if st.button("🔄 Reset Nuovo Match"):
        st.session_state.page = "setup"; st.session_state.log_strutturato = []; st.rerun()
