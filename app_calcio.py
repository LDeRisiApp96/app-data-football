import streamlit as st
import time
import datetime
import pandas as pd

# --- CONFIGURAZIONE MOBILE ---
st.set_page_config(page_title="Scout Mobile", page_icon="⚽", layout="centered")

# --- CSS PER CONTROLLO TOTALE SU UNA RIGA ---
st.markdown("""
    <style>
    .block-container { padding: 0.5rem !important; }
    /* Pulsanti crono in fila */
    div.stButton > button { font-size: 11px !important; height: 35px !important; padding: 0px !important; border-radius: 6px !important; }
    /* Bottoni eventi in colonna */
    .event-btn button { font-size: 13px !important; height: 45px !important; width: 100% !important; margin-bottom: 5px !important; }
    .timer-badge { position: fixed; top: 5px; right: 5px; background: #EF4444; color: white; padding: 2px 8px; border-radius: 8px; font-weight: bold; font-size: 12px; }
    </style>
""", unsafe_allow_html=True)

# [Logica invariata per inizializzazione...]
if "page" not in st.session_state: st.session_state.page = "setup"
if "crono_stato" not in st.session_state: st.session_state.crono_stato = "Fermo"
if "tempo_accumulato" not in st.session_state: st.session_state.tempo_accumulato = 0.0
if "log_strutturato" not in st.session_state: st.session_state.log_strutturato = []

# ==========================================
# DASHBOARD LIVE
# ==========================================
if st.session_state.page == "live":
    # 1. RIGA UNICA CRONOMETRO
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        if st.button("▶️"): st.session_state.crono_stato = "In Corso"; st.session_state.ultimo_avvio = time.time(); st.rerun()
    with c2: 
        if st.button("⏸️"): st.session_state.crono_stato = "Interrotto"; st.session_state.tempo_accumulato += time.time() - st.session_state.ultimo_avvio; st.rerun()
    with c3: 
        if st.button("🔄"): st.session_state.crono_stato = "In Corso"; st.session_state.ultimo_avvio = time.time(); st.rerun()
    with c4: 
        if st.button("⏹️"): st.session_state.page = "report"; st.rerun()

    # 2. SELETTORE GIOCATORE
    giocatore = st.selectbox("Giocatore:", st.session_state.in_campo, label_visibility="collapsed")

    # 3. GRIGLIA EVENTI SU DUE COLONNE
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="event-btn">', unsafe_allow_html=True)
        if st.button("⚽ GOL"): # ... logica evento
            pass
        if st.button("🎯 IN PORTA"):
            pass
        st.markdown('</div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="event-btn">', unsafe_allow_html=True)
        if st.button("❌ FUORI"):
            pass
        if st.button("📉 PALLA PERSA"):
            pass
        st.markdown('</div>', unsafe_allow_html=True)
