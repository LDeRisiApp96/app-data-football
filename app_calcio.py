import streamlit as st
import time
import datetime
import pandas as pd
import plotly.express as px

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Scout Pro", page_icon="⚽", layout="centered")

# --- CSS DEFINITIVO PER BOTTONI E LAYOUT ---
# --- CSS OTTIMIZZATO PER MOBILE ---
# --- CSS PER MOBILE E RIGA UNICA ---
st.markdown("""
    <style>
    /* Forza bottoni a pieno schermo e leggibili */
    div.stButton > button {
        width: 100% !important;
        height: 50px !important;
        font-size: 14px !important;
        margin-top: 2px !important;
        margin-bottom: 2px !important;
    }
    /* Contenitore per allineare bottoni orizzontalmente */
    [data-testid="column"] {
        padding: 2px !important;
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
# Questa funzione gira nativamente sul cloud ad altissima velocità
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
# 1. PAGINA INIZIALE (SETUP)
# ==========================================
if st.session_state.page == "setup":
    st.markdown("<p class='main-title'>🆕 Nuovo Match</p>", unsafe_allow_html=True)
    
    data_match = st.date_input("Data della partita", datetime.date.today())
    competizione = st.text_input("Competizione", placeholder="Es. Serie D, Promozione...")
    
    col_sq1, col_sq2 = st.columns(2)
    with col_sq1: casa = st.text_input("Squadra Casa", placeholder="Casa")
    with col_sq2: trasferta = st.text_input("Squadra Trasferta", placeholder="Trasferta")
    
    st.write("---")
    col_dist1, col_dist2 = st.columns(2)
    with col_dist1:
        titolari_input = st.text_area("📋 TITOLARI (uno per riga)", 
                                       value="1. Provedel\n4. Rossi\n8. Ferrari\n9. Bianchi\n10. Verdi", height=150)
    with col_dist2:
        panchina_input = st.text_area("🪑 PANCHINA (uno per riga)", 
                                       value="12. Alisson\n14. Neri\n18. Viola\n20. Gialli", height=150)
        
    portieri_input = st.text_input("Specifica il nome del Portiere (staccati da virgola se più di uno)", 
                                   value="1. Provedel, 12. Alisson")
    
    st.write("---")
    if st.button("🚀 PROCEDI AL MATCH"):
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
            st.error("Inserisci i nomi delle squadre!")

# ==========================================
# 2. PAGINA LIVE (RACCOLTA DATI)
# ==========================================
elif st.session_state.page == "live":
    md = st.session_state.match_data

    st.markdown(f"""
        <div class='match-info-banner'>
            <small>{md['data']} - {md['competizione']} ({st.session_state.tempo_gioco})</small><br>
            <strong>{md['casa']} vs {md['trasferta']}</strong>
        </div>
    """, unsafe_allow_html=True)

    # Recupero del tempo per calcolo minuto dell'evento
    if st.session_state.crono_stato == "In Corso":
        passato_corrente = st.session_state.tempo_accumulato + (time.time() - st.session_state.ultimo_avvio)
    else:
        passato_corrente = st.session_state.tempo_accumulato
    minuto_calcistico = int(passato_corrente // 60) + 1

    # Avvio del fragment orologio in background
    mostra_orologio()

    # Controlli cronometro
    # --- RIGA COMANDI CRONOMETRO 1x4 ---
    # Definiamo le colonne
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    
    # Creiamo un contenitore CSS che forza la riga singola su mobile
    st.markdown("""
        <style>
        /* Forza le colonne a stare vicine e non andare a capo */
        [data-testid="column"] {
            flex: 1 1 25% !important;
            max-width: 25% !important;
        }
        /* Riduci il padding dei bottoni per farli stare meglio */
        div.stButton > button {
            padding: 5px 2px !important;
            font-size: 11px !important; /* Testo più piccolo per non andare a capo */
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Inseriamo i bottoni nelle colonne
    with col_t1:
        if st.button("▶️ Inizio"): 
            st.session_state.crono_stato = "In Corso"; st.session_state.ultimo_avvio = time.time(); st.rerun()
    with col_t2:
        if st.button("⏸️ Sosta"): 
            st.session_state.crono_stato = "Interrotto"; st.session_state.tempo_accumulato += time.time() - st.session_state.ultimo_avvio; st.rerun()
    with col_t3:
        if st.button("🔄 Ripr."): 
            st.session_state.crono_stato = "In Corso"; st.session_state.ultimo_avvio = time.time(); st.rerun()
    with col_t4:
        if st.button("⏹️ Fine"): 
            st.session_state.page = "report"; st.rerun()
    # Intervallo
    if st.session_state.tempo_gioco == "1° Tempo":
        if st.button("⏸️ PASSA A INTERVALLO / 2° TEMPO"):
            if st.session_state.crono_stato == "In Corso":
                st.session_state.tempo_accumulato += time.time() - st.session_state.ultimo_avvio
            st.session_state.tempo_gioco = "2° Tempo"
            st.session_state.crono_stato = "Fermo"
            st.session_state.tempo_accumulato = 45.0 * 60.0
            st.rerun()

    st.write("---")

    if st.session_state.in_campo:
        giocatore_scelto = st.selectbox("👤 Seleziona Giocatore in Campo:", st.session_state.in_campo)
        is_portiere = giocatore_scelto in md['portieri']
    else:
        st.error("🔴 Nessun giocatore rimasto in campo!")
        giocatore_scelto = None
        is_portiere = False

    with st.expander("🔄 Effettua una Sostituzione"):
        if st.session_state.in_panchina and giocatore_scelto:
            giocatore_entrante = st.selectbox("🪑 Chi entra dalla panchina?", st.session_state.in_panchina)
            if st.button("📥 CONFERMA CAMBIO"):
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
                st.success(f"Cambio effettuato! {giocatore_scelto} -> {giocatore_entrante}")
                time.sleep(0.5)
                st.rerun()
        else:
            st.warning("Impossibile effettuare sostituzioni.")

    st.write("### ⚡ Registra Evento")
    disabilitato = (st.session_state.crono_stato != "In Corso" or giocatore_scelto is None)
    if st.session_state.crono_stato != "In Corso":
        st.warning("⚠️ Avvia o Riprendi il cronometro per registrare gli eventi!")

    evento_registrato = None
    forzare_rimozione_espulso = False

    if is_portiere and giocatore_scelto:
        st.markdown("##### 🧤 Ruolo Portiere")
        riga_p1, riga_p2 = st.columns(2)
        with riga_p1:
            if st.button("👐 Parata", disabled=disabilitato): evento_registrato = "Parata"
        with riga_p2:
            if st.button("🥅 Gol Subito", disabled=disabilitato): evento_registrato = "Gol Subito"
        st.write("---")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("⚽ GOL!", disabled=disabilitato): evento_registrato = "GOL"
    with c2:
        if st.button("❌ Tiro Fuori", disabled=disabilitato): evento_registrato = "Tiro Fuori"

    c3, c4 = st.columns(2)
    with c3:
        if st.button("🎯 Tiro in Porta", disabled=disabilitato): evento_registrato = "Tiro in Porta"
    with c4:
        if st.button("👟 Passaggio Chiave", disabled=disabilitato): evento_registrato = "Passaggio Chiave"

    c5, c6 = st.columns(2)
    with c5:
        if st.button("🔄 Palla Recuperata", disabled=disabilitato): evento_registrato = "Palla Recuperata"
    with c6:
        if st.button("📉 Palla Persa", disabled=disabilitato): evento_registrato = "Palla Persa"

    c7, c8 = st.columns(2)
    with c7:
        if st.button("💥 Fallo Subito", disabled=disabilitato): evento_registrato = "Fallo Subito"
    with c8:
        if st.button("🛑 Fallo Commesso", disabled=disabilitato): evento_registrato = "Fallo Commesso"

    c9, c10 = st.columns(2)
    with c9:
        if st.button("🟨 Ammonito", disabled=disabilitato): evento_registrato = "Ammonito"
    with c10:
        if st.button("🟥 Espulso", disabled=disabilitato): 
            evento_registrato = "Espulso"
            forzare_rimozione_espulso = True

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
            st.toast(f"Registrato: {giocatore_scelto} -> {evento_registrato}")
        
        time.sleep(0.3)
        st.rerun()

    if st.session_state.log_strutturato:
        st.write("---")
        st.markdown("##### 📝 Ultimi Eventi:")
        for ev in st.session_state.log_strutturato[:5]:
            st.caption(f"{ev['Minuto']}' ({ev['Tempo']}) | {ev['Giocatore']} : **{ev['Evento']}**")

# ==========================================
# 3. PAGINA DI REPORT, GRAFICI E ANALISI
# ==========================================
elif st.session_state.page == "report":
    st.markdown("<p class='main-title'>📊 Analisi Match</p>", unsafe_allow_html=True)
    
    if st.session_state.log_strutturato:
        df_completo = pd.DataFrame(st.session_state.log_strutturato)
        
        st.markdown("### 🔍 Filtra Analisi")
        filtro_tempo = st.radio("Seleziona frazione di gioco da analizzare:", ["Intera Partita", "Solo 1° Tempo", "Solo 2° Tempo"], horizontal=True)
        
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
        cm1.metric("Gol Fatti", tot_gol)
        cm2.metric("Tiri Totali", tot_tiri)
        cm3.metric("Palle Rec.", tot_recuperi)
        cm4.metric("Palle Perse", tot_perse)
        
        st.write("---")
        col_graf1, col_graf2 = st.columns(2)
        
        with col_graf1:
            st.markdown("##### 🎯 Distribuzione Tiri Squadra")
            df_tiri = df[df["Evento"].isin(["GOL", "Tiro in Porta", "Tiro Fuori"])]
            if not df_tiri.empty:
                conteggio_tiri = df_tiri["Evento"].value_counts().reset_index()
                conteggio_tiri.columns = ["Tipo Tiro", "Conteggio"]
                colori_mappa = {"GOL": "#10B981", "Tiro in Porta": "#3B82F6", "Tiro Fuori": "#EF4444"}
                fig = px.pie(conteggio_tiri, values="Conteggio", names="Tipo Tiro", color="Tipo Tiro", color_discrete_map=colori_mappa, hole=0.3)
                fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.caption("Nessun tiro registrato.")
                
        with col_graf2:
            st.markdown("##### 🔄 Bilancio Possesso Squadra")
            df_poss_squadra = pd.DataFrame({
                "Fase": ["Palle Recuperate", "Palle Perse"],
                "Totale": [tot_recuperi, tot_perse]
            })
            if tot_recuperi > 0 or tot_perse > 0:
                fig_poss = px.bar(df_poss_squadra, x="Fase", y="Totale", color="Fase", color_discrete_map={"Palle Recuperate": "#06B6D4", "Palle Perse": "#4B5563"})
                fig_poss.update_layout(margin=dict(t=10, b=10, l=10, r=10), showlegend=False, xaxis_title=None, yaxis_title=None)
                st.plotly_chart(fig_poss, use_container_width=True)
            else:
                st.caption("Nessun dato di possesso.")

        st.write("---")
        st.markdown("### 👤 KPI e Statistiche Individuali")
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
        ck1.metric("Gol Segnati", g_gol)
        ck2.metric("Tiri Totali (In Porta)", f"{g_tiri} ({g_in_porta})")
        ck3.metric("Palle Recuperate", g_recuperate)
        ck4.metric("Palle Perse", g_perse)
        
        ck5, ck6, ck7, ck8 = st.columns(4)
        ck5.metric("Passaggi Chiave", g_chiave)
        ck6.metric("Falli Subiti / Fatti", f"{g_subiti} / {g_commessi}")
        ck7.metric("Cartellini (G/R)", f"{g_ammo} / {g_espu}")
        if g_parate > 0 or giocatore_kpi in st.session_state.match_data['portieri']:
            ck8.metric("Parate Effettuate", g_parate)
        else:
            ck8.metric("Stato", "In Campo" if giocatore_kpi in st.session_state.in_campo else "Panchina/Sostituito/Espulso")
            
        if not df_singolo.empty:
            st.caption(f"Cronologia azioni di {giocatore_kpi}:")
            eventi_brevi = [f"{row['Minuto']}' ({row['Tempo']}) - {row['Evento']}" for _, row in df_singolo.iterrows()]
            st.write(", ".join(eventi_brevi))

        st.write("---")
        st.markdown("### 📋 Tabella Completa Eventi")
        st.dataframe(df_completo[["Tempo", "Minuto", "Giocatore", "Evento"]], use_container_width=True)
        
        csv = df_completo.to_csv(index=False).encode('utf-8')
        nome_file = f"scout_{st.session_state.match_data['casa']}_vs_{st.session_state.match_data['trasferta']}.csv"
        st.download_button(label="📥 SCARICA DATABASE CSV", data=csv, file_name=nome_file, mime='text/csv')
        
    st.write("---")
    if st.button("🔄 Inizia un nuovo match (Reset)"):
        st.session_state.page = "setup"
        st.session_state.log_strutturato = []
        st.rerun()
