import streamlit as st
import pandas as pd

# --- ELITE UI CONFIG ---
st.set_page_config(page_title="DVA Elite Performance", layout="wide")

# Özel CSS: Kartlar, Butonlar ve Tipografi
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus+Jakarta+Sans', sans-serif; background-color: #f8f9fa; }
    
    /* Lig Seçim Butonları */
    .stRadio [role="radiogroup"] { gap: 10px; padding: 10px 0; }
    
    /* Modern Kart Yapısı */
    .elite-card {
        background: white;
        padding: 24px;
        border-radius: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        transition: transform 0.2s;
    }
    .elite-score {
        color: #00d084;
        font-size: 32px;
        font-weight: 800;
        margin: 10px 0;
    }
    .team-tag {
        font-size: 12px;
        color: #6c757d;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GENİŞ VERİ SETİ ---
if 'players_df' not in st.session_state:
    st.session_state.players_df = pd.DataFrame([
        {"Name": "E. Haaland", "Team": "Man City", "League": "Premier League", "Pos": "FW", "Perf": 88, "Gls": 1.12, "Ast": 0.15, "xG": 0.95, "Pass": 78},
        {"Name": "K. De Bruyne", "Team": "Man City", "League": "Premier League", "Pos": "MF", "Perf": 91, "Gls": 0.25, "Ast": 0.88, "xG": 0.22, "Pass": 84},
        {"Name": "Vinícius Jr.", "Team": "Real Madrid", "League": "La Liga", "Pos": "FW", "Perf": 94, "Gls": 0.65, "Ast": 0.40, "xG": 0.55, "Pass": 82},
        {"Name": "Lamine Yamal", "Team": "Barcelona", "League": "La Liga", "Pos": "FW", "Perf": 85, "Gls": 0.35, "Ast": 0.50, "xG": 0.42, "Pass": 79},
        {"Name": "Harry Kane", "Team": "FC Bayern", "League": "Bundesliga", "Pos": "FW", "Perf": 92, "Gls": 1.05, "Ast": 0.22, "xG": 0.88, "Pass": 81}
    ])

# --- SAYFA NAVİGASYONU ---
menu = st.sidebar.radio("NAVIGASYON", ["🏠 Keşfet", "⚔️ Arena (Kıyasla)", "🏟️ Canlı Skor", "⚙️ Admin"])

if menu == "🏠 Keşfet":
    st.title("Elite Performers")
    
    # Lig Filtreleri (Dribbble Stil)
    leagues = ["Premier League", "La Liga", "Bundesliga", "Serie A"]
    sel_league = st.radio("LİG SEÇİMİ", leagues, horizontal=True, label_visibility="collapsed")
    
    # Global Arama
    search = st.text_input("🔍 Oyuncu, takım veya lig ara...", placeholder="Örn: Haaland")
    
    st.divider()
    
    # Filtrelenmiş Veri
    f_df = st.session_state.players_df[st.session_state.players_df['League'] == sel_league]
    if search:
        f_df = st.session_state.players_df[st.session_state.players_df['Name'].str.contains(search, case=False)]

    # Kart Görünümü
    cols = st.columns(3)
    for i, (_, p) in enumerate(f_df.iterrows()):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="elite-card">
                    <span class="team-tag">{p['Team']}</span>
                    <h3 style="margin: 5px 0 0 0;">{p['Name']}</h3>
                    <div class="elite-score">{p['Perf']}</div>
                    <p style="font-size: 13px; color: #888;">Haftalık Performans Endeksi</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Profil: {p['Name']}", key=p['Name']):
                st.session_state.selected_p = p['Name']
                st.rerun()

    # OYUNCU PROFİL DETAYI (Seçilince Açılır)
    if 'selected_p' in st.session_state:
        st.divider()
        player = st.session_state.players_df[st.session_state.players_df['Name'] == st.session_state.selected_p].iloc[0]
        st.subheader(f"Detailed Analytics: {player['Name']}")
        
        c1, c2 = st.columns([1, 2])
        with c1:
            st.info(f"**Mevki:** {player['Pos']}\n\n**Pas İsabeti:** %{player['Pass']}")
            if st.button("⚔️ Bu Oyuncuyu Kıyaslamaya Gönder"):
                st.toast("Arena'ya eklendi!")
        with c2:
            st.write("**Son Maçlar**")
            st.table(pd.DataFrame({"Maç": ["v Liverpool", "v Arsenal"], "Skor": ["1G", "1A"], "Puan": [8.2, 7.5]}))

elif menu == "⚔️ Arena (Kıyasla)":
    st.title("Comparison Arena")
    # Sportbase tarzı yan yana karşılaştırma (V8'deki modern satır yapısı)
    names = st.session_state.players_df['Name'].tolist()
    p1 = st.selectbox("Oyuncu 1", names, index=0)
    p2 = st.selectbox("Oyuncu 2", names, index=1)
    
    d1 = st.session_state.players_df[st.session_state.players_df['Name'] == p1].iloc[0]
    d2 = st.session_state.players_df[st.session_state.players_df['Name'] == p2].iloc[0]
    
    metrics = [("Goals/90", "Gls"), ("Assists/90", "Ast"), ("xG", "xG"), ("Pass Acc", "Pass")]
    for label, key in metrics:
        col1, col2, col3 = st.columns([1, 2, 1])
        col1.markdown(f"<h4 style='text-align:left;'>{d1[key]}</h4>", unsafe_allow_html=True)
        col2.markdown(f"<p style='text-align:center; color:gray; margin-top:10px;'>{label}</p>", unsafe_allow_html=True)
        col3.markdown(f"<h4 style='text-align:right;'>{d2[key]}</h4>", unsafe_allow_html=True)
        st.divider()

elif menu == "🏟️ Canlı Skor":
    st.title("Match Day")
    st.markdown("<div style='background:white; padding:40px; border-radius:30px; text-align:center;'>Man City <b>2 - 1</b> Arsenal<br><small>LIVE 72'</small></div>", unsafe_allow_html=True)
