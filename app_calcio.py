import streamlit as st
import time
import datetime
import pandas as pd

st.set_page_config(page_title="Scout Mobile", layout="centered")

# --- CSS BASE ---
st.markdown("""
    <style>
    .block-container { padding: 0.5rem !important; }
    div.stButton > button { font-size: 13px !important; height: 40px !important; width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

# Inizializzazione base
if "page" not in st.session_state: st.session_state.page = "setup"
if "log_strutturato" not in st.session_state: st.session_state.log_strutturato = []

# --- PAGINE ---
if st.session_state.page == "setup":
    st.write("### ⚽ Setup")
    casa = st.text_input("Squadra Casa", "Team A")
    if st.button("AVVIA"):
        st.session_state.page = "live"
        st.rerun()

elif st.session_state.page == "live":
    st.write("### ⏱️ Live")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("▶️"): st.session_state.crono_stato = "In Corso"
    if c2.button("⏸️"): st.session_state.crono_stato = "Pausa"
    if c3.button("🔄"): pass
    if c4.button("⏹️"): st.session_state.page = "report"; st.rerun()
    
    col_a, col_b = st.columns(2)
    if col_a.button("⚽ GOL"): st.toast("Gol registrato!")
    if col_b.button("❌ FUORI"): st.toast("Tiro fuori")

elif st.session_state.page == "report":
    st.write("### 📊 Report")
    if st.button("Reset"): st.session_state.page = "setup"; st.rerun()
