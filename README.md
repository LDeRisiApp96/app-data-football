# ⚽ Scout Pro - App Football Data

> ⚠️ **PROGETTO PRIVATO** - Accesso esclusivo solo su autorizzazione

Un'applicazione **Streamlit** moderna e responsive per la raccolta dati in tempo reale durante le partite di calcio. Perfetta per scout, allenatori e analisti che desiderano tracciare dettagliatamente le performance dei giocatori.

## 🔐 Accesso e Licenza

**Tutti i diritti riservati © 2026 LDeRisiApp96**

Questo software è **proprietario e confidenziale**. È **VIETATO**:
- ❌ Copiare, clonare o forkare il codice
- ❌ Usarlo in produzione senza licenza esplicita
- ❌ Distribuirlo a terzi
- ❌ Modificarlo senza autorizzazione
- ❌ Pubblicare il codice altrove
- ❌ Creare versioni derivate

**Per accesso, utilizzo commerciale o collaborazioni:** 
📧 Contatta l'autore per una licenza autorizzata

---

## 🎯 Caratteristiche Principali

### 📊 Raccolta Dati Live
- **Cronometro fluido** con tracking del tempo effettivo di gioco
- **Registrazione eventi in tempo reale**: gol, tiri, passaggi, recuperi, falli, cartellini
- **Gestione giocatori**: titolari, panchina, sostituzioni automatiche
- **Suddivisione per tempo**: 1° e 2° tempo

### 📈 Analisi Avanzate
- **Statistiche di squadra**: totali gol, tiri, recuperi, palle perse
- **Grafici interattivi** (Plotly): distribuzione tiri, possesso palla
- **KPI individuali**: statistiche dettagliate per ogni giocatore
- **Tabella eventi completa** con export CSV

### 📱 Design Responsive
- **Mobile-first**: completamente ottimizzato per smartphone e tablet
- **Tema scuro** confortevole per l'uso in campo
- **Interfaccia intuitiva** con bottoni a griglia 2 colonne
- **Gestione touch** ottimizzata

### 🎨 Esperienza Utente
- Toast notifications per le azioni confermate
- Layout adattivo con media queries CSS
- Schermo di caricamento e transition fluide
- Colori codificati per gli eventi (gol verde, tiri blu, falli grigi, cartellini giallo/rosso)

## 📦 Requisiti

```txt
streamlit>=1.33.0
pandas
plotly
```

## 🚀 Installazione e Avvio

### 1. Clona il repository
```bash
git clone https://github.com/LDeRisiApp96/app-data-football.git
cd app-data-football
```

### 2. Installa le dipendenze
```bash
pip install -r requirements.txt
```

### 3. Avvia l'app
```bash
streamlit run app_calcio.py
```

L'app si aprirà automaticamente nel browser all'indirizzo `http://localhost:8501`

## 📋 Come Usarla

### Fase 1: Setup Partita
1. Inserisci la **data** della partita
2. Compila i dati delle **squadre** (casa/trasferta) e **competizione**
3. Elenca i **giocatori titolari** (uno per riga)
4. Elenca i **giocatori in panchina** (uno per riga)
5. Specifica i **numeri dei portieri**
6. Clicca **"🚀 PROCEDI AL MATCH"**

### Fase 2: Live Tracking
1. **Avvia il cronometro** con il bottone "▶️ Inizio"
2. **Seleziona un giocatore** dalla lista
3. **Registra gli eventi** cliccando i bottoni corrispondenti:
   - ⚽ **GOL**: gol realizzato
   - 🎯 **Tiro in Porta**: tiro nello specchio
   - ❌ **Tiro Fuori**: tiro fuori dalla porta
   - 👟 **Pass Chiave**: passaggio decisivo
   - 🔄 **Palla Rec.**: palla recuperata
   - 📉 **Palla Persa**: palla persa
   - 💥 **Fallo Subito**: fallo subito dal giocatore
   - 🛑 **Fallo Fatto**: fallo commesso dal giocatore
   - 🟨 **Ammonito**: cartellino giallo
   - 🟥 **Espulso**: cartellino rosso
   - 👐 **Parata** (solo portieri): parata effettuata
   - 🥅 **Gol Subito** (solo portieri): gol subito

4. **Effettua sostituzioni** tramite l'expander "🔄 Effettua una Sostituzione"
5. **Passa al 2° tempo** con il bottone "⏸️ PASSA A INTERVALLO / 2° TEMPO"
6. **Termina la partita** con il bottone "⏹️ Fine"

### Fase 3: Analisi e Report
1. **Filtra per tempo**: intera partita, solo 1° o solo 2° tempo
2. **Visualizza statistiche di squadra**: gol, tiri, recuperi, palle perse
3. **Analizza KPI individuali**: seleziona un giocatore per vedere i suoi dettagli
4. **Visualizza grafici**: distribuzione tiri e possesso palla
5. **Scarica i dati** in formato CSV

## 🎨 Eventi Supportati

| Evento | Colore | Descrizione |
|--------|--------|-------------|
| GOL | 🟢 Verde | Gol realizzato |
| Tiro in Porta | 🔵 Blu | Tiro nello specchio |
| Tiro Fuori | 🔴 Rosso | Tiro fuori dalla porta |
| Pass Chiave | 🔵 Blu | Passaggio decisivo |
| Palla Recuperata | 🔵 Ciano | Palla recuperata |
| Palla Persa | ⚫ Grigio | Palla persa |
| Fallo Subito | 🔵 Ciano | Fallo subito |
| Fallo Commesso | ⚫ Grigio | Fallo commesso |
| Ammonito | 🟨 Giallo | Cartellino giallo |
| Espulso | 🔴 Rosso | Cartellino rosso |
| Parata | 🟣 Viola | Parata (portiere) |
| Gol Subito | 🟣 Viola | Gol subito (portiere) |

## 🗂️ Struttura del Progetto

```
app-data-football/
├── app_calcio.py          # Applicazione principale Streamlit
├── requirements.txt       # Dipendenze Python
├── README.md              # Documentazione
└── .devcontainer/         # Configurazione Dev Container (opzionale)
```

## 📊 Dati Raccolti

Ogni evento registrato include:
- **Data**: Data della partita
- **Competizione**: Tipo di competizione
- **Partita**: Squadre coinvolte
- **Tempo**: 1° o 2° tempo
- **Minuto**: Minuto calcistico dell'evento
- **Giocatore**: Nome del giocatore
- **Evento**: Tipo di evento

## 💾 Export

I dati possono essere scaricati in formato **CSV** direttamente dall'app con il bottone "📥 SCARICA CSV". Il file avrà il nome: `scout_[squadra_casa]_vs_[squadra_trasferta].csv`

## 🛠️ Stack Tecnologico

- **Frontend**: [Streamlit](https://streamlit.io/) - Framework web Python
- **Dati**: [Pandas](https://pandas.pydata.org/) - Data manipulation
- **Visualizzazione**: [Plotly](https://plotly.com/) - Grafici interattivi
- **Linguaggio**: Python 3.8+

## 📱 Browser Supportati

- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Dispositivi mobili (iOS/Android)

## ⚙️ Configurazione Avanzata

### Personalizzare i Colori
Modifica la sezione CSS nel file `app_calcio.py` (righe 10-284) per personalizzare il tema dell'applicazione.

### Aggiungere Nuovi Eventi
1. Aggiungi il bottone nella sezione "⚡ Registra Evento" (riga 464+)
2. Aggiorna il sistema di colori CSS
3. Aggiungi la logica di registrazione nell'evento

---

**Creato con ❤️ da LDeRisiApp96**

*Ultimo aggiornamento: Maggio 2026*