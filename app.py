import streamlit as st
import pandas as pd
import plotly.express as px

# --- MODERN UI CONFIG (DRIBBBLE INSPIRED) ---
st.set_page_config(page_title="DVA: Elite Analytics", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; background-color: #fcfcfd; }
    
    /* Lig Butonları */
    .stRadio [role="radiogroup"] {
        background: #f1f3f5;
        padding: 10px;
        border-radius: 15px;
        border: none;
    }
    
    /* Modern Kart Tasarımı */
    .player-card {
        background: white;
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #f0f0f0;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.03);
        text-align: center;
        margin-bottom: 15px;
    }
    .player-score {
        background: #101828;
        color: #00d084;
        font-size: 24px;
        font-weight: 800;
        padding: 5px 15px;
        border-radius: 12px;
        display: inline-block;
    }
    
    /* Karşılaştırma Tablosu */
    .comparison-row {
        display: flex;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid #f0f0f0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETİ ---
if 'players_df' not in st.session_state:
    data = [
        {"Name": "E. Haaland", "Team": "Man City", "League": "Premier League", "Pos": "FW", "Price": 180, "Perf": 88, "Gls": 1.12, "Ast": 0.15, "xG": 0.95, "SHT": 3.8, "Pass": 78},
        {"Name": "K. De Bruyne", "Team": "Man City", "League": "Premier League", "Pos": "MF", "Price": 90, "Perf": 91, "Gls": 0.25, "Ast": 0.88, "xG": 0.22, "SHT": 2.1, "Pass": 84},
        {"Name": "Vinícius Jr.", "Team": "Real Madrid", "League": "La Liga", "Pos": "FW", "Price": 150, "Perf": 94, "Gls": 0.65, "Ast": 0.40, "xG": 0.55, "SHT": 3.2, "Pass": 82},
        {"Name": "J. Bellingham", "Team": "Real Madrid", "League": "La Liga", "Pos": "MF", "Price": 120, "Perf": 89, "Gls": 0.45, "Ast": 0.30, "xG": 0.35, "SHT": 1.8, "Pass": 88}
    ]
    st.session_state.players_df = pd.DataFrame(data)

# --- SIDEBAR & NAV ---
page = st.sidebar.radio("Navigation", ["🏠 Home", "🏟️ Live Center", "⚔️ Comparison", "🔐 Admin"])

# --- 1. HOME (DRIBBBLE LEAGUE TABS) ---
if page == "🏠 Home":
    st.title("Elite Performers")
    
    # Lig Seçimi (Tabs gibi duran radio)
    leagues = ["Premier League", "La Liga", "Bundesliga", "Serie A"]
    selected_league = st.radio("Choose League", leagues, horizontal=True, label_visibility="collapsed")
    
    st.divider()
    
    # Oyuncu Kartları
    f_df = st.session_state.players_df[st.session_state.players_df['League'] == selected_league]
    
    if not f_df.empty:
        cols = st.columns(3)
        for idx, (_, row) in enumerate(f_df.iterrows()):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="player-card">
                        <p style="color:gray; font-size:12px; margin:0;">{row['Team']}</p>
                        <h3 style="margin:5px 0;">{row['Name']}</h3>
                        <div class="player-score">{row['Perf']}</div>
                        <p style="font-size:12px; margin-top:5px; color:#666;">Opta Rating</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"Analyze {row['Name']}", key=row['Name']):
                    st.toast(f"Detail view for {row['Name']}")
    else:
        st.info("No data available for this league yet.")

# --- 2. LIVE CENTER ---
elif page == "🏟️ Live Center":
    st.title("Live Match Day")
    # Modern Maç Kartı
    st.markdown("""
        <div style="background:white; padding:30px; border-radius:25px; text-align:center; border: 1px solid #f0f0f0;">
            <div style="display:flex; justify-content:space-around; align-items:center;">
                <div><h2 style="margin:0;">MC</h2><p>Man City</p></div>
                <div><h1 style="margin:0; font-size:48px;">2 - 1</h1><span style="color:red; font-weight:bold;">LIVE 78'</span></div>
                <div><h2 style="margin:0;">ARS</h2><p>Arsenal</p></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 3. COMPARISON (CLEAN DATA VIEW) ---
elif page == "⚔️ Comparison":
    st.title("Head to Head")
    names = st.session_state.players_df['Name'].tolist()
    c1, c2 = st.columns(2)
    p1 = c1.selectbox("First Player", names, index=0)
    p2 = c2.selectbox("Second Player", names, index=1)
    
    d1 = st.session_state.players_df[st.session_state.players_df['Name'] == p1].iloc[0]
    d2 = st.session_state.players_df[st.session_state.players_df['Name'] == p2].iloc[0]
    
    st.divider()
    
    # Modern Satır Bazlı Karşılaştırma
    metrics = [("Goals/90", "Gls"), ("Assists/90", "Ast"), ("Expected Goals", "xG"), ("Shots/90", "SHT"), ("Pass Accuracy", "Pass")]
    
    for label, key in metrics:
        st.markdown(f"""
            <div class="comparison-row">
                <div style="font-weight:bold; color:#007bff; width:20%;">{d1[key]}</div>
                <div style="color:gray; text-align:center; width:60%;">{label}</div>
                <div style="font-weight:bold; color:#00d084; width:20%; text-align:right;">{d2[key]}</div>
            </div>
        """, unsafe_allow_html=True)

# --- 4. ADMIN ---
elif page == "🔐 Admin":
    st.title("Data Management")
    target = st.selectbox("Player", st.session_state.players_df['Name'])
    score = st.slider("Update Performance", 0, 100, 90)
    if st.button("Commit Change"):
        st.session_state.players_df.loc[st.session_state.players_df['Name'] == target, 'Perf'] = score
        st.success("Database Updated")
