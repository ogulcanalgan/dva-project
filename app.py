import streamlit as st
import pandas as pd

# --- CONFIG & THEME ---
st.set_page_config(page_title="DVA Terminal", layout="wide", initial_sidebar_state="collapsed")

# Session State (Patlamayı önleyen güvenli yapı)
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'target' not in st.session_state: st.session_state.target = None
if 'club' not in st.session_state: st.session_state.club = None

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus+Jakarta+Sans', sans-serif; background: #f8fafc; }
    
    /* Kartın her yerini tıklanabilir yapan şeffaf buton stili */
    .stButton > button { 
        width: 100%; border-radius: 20px; border: 1px solid #e2e8f0; 
        background: white; color: #1e293b; text-align: left; padding: 25px;
        transition: all 0.2s ease;
    }
    .stButton > button:hover { border-color: #6366f1; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }

    .stat-card { background: white; padding: 20px; border-radius: 15px; border-bottom: 4px solid #6366f1; text-align: center; }
    .pro-banner { background: #0f172a; color: white; padding: 40px; border-radius: 25px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
def go_to(page, target=None, club=None):
    st.session_state.page = page
    st.session_state.target = target
    st.session_state.club = club
    st.rerun()

# --- TOP LIVE STRIP ---
m_list = [("GS", "2-1", "BJK", "74'"), ("RM", "0-0", "BAR", "18'"), ("MC", "3-2", "LIV", "MS")]
cols = st.columns(len(m_list))
for i, (t1, s, t2, time) in enumerate(m_list):
    if cols[i].button(f"🏟️ {t1} {s} {t2} | {time}", key=f"mstrip_{i}"):
        go_to('live_match', target=f"{t1} v {t2}")

st.divider()

# --- PAGE: MAIN ---
if st.session_state.page == 'main':
    st.title("📡 DVA Trend Radar")
    c1, c2, c3 = st.columns(3)
    players = [
        {"n": "Arda Güler", "v": "€68.4M", "t": "REAL MADRID"},
        {"n": "Semih Kılıçsoy", "v": "€22.1M", "t": "BEŞİKTAŞ"},
        {"n": "Ferdi Kadıoğlu", "v": "€35.0M", "t": "BRIGHTON"}
    ]
    for i, p in enumerate(players):
        with [c1, c2, c3][i]:
            # Kartın her yerine tıklama: Buton metnini kart gibi tasarladık
            if st.button(f"🔥 {p['t']}\n\n{p['n']}\nValue: {p['v']}", key=f"pcard_{i}"):
                go_to('profile', target=p['n'])

# --- PAGE: LIVE MATCH (MAÇKOLİK STYLE) ---
elif st.session_state.page == 'live_match':
    if st.button("← Geri Dön"): go_to('main')
    
    st.header(f"🏟️ {st.session_state.target} | Maç Analitiği")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 İstatistik", "📋 Kadrolar", "📉 Puan Durumu", "📅 Fikstür"])
    
    with tab1:
        sc1, sc2, sc3 = st.columns(3)
        sc1.markdown('<div class="stat-card"><b>xG (Beklenen Gol)</b><h3>1.84 - 0.92</h3></div>', unsafe_allow_html=True)
        sc2.markdown('<div class="stat-card"><b>Topla Oynama</b><h3>%54 - %46</h3></div>', unsafe_allow_html=True)
        sc3.markdown('<div class="stat-card"><b>DVA Rating</b><h3>8.2</h3></div>', unsafe_allow_html=True)

    with tab2:
        k1, k2 = st.columns(2)
        with k1:
            if st.button("🛡️ Galatasaray SK (Kulüp Profili)", use_container_width=True):
                go_to('club_detail', club="Galatasaray SK")
            st.table(pd.DataFrame({"Oyuncu": ["Muslera", "Sanchez", "Torreira"], "DVA": [7.1, 8.4, 7.8]}))
        with k2:
            st.write("**Beşiktaş JK**")
            st.table(pd.DataFrame({"Oyuncu": ["Mert", "Paulista", "Gedson"], "DVA": [6.9, 7.5, 8.1]}))

    with tab3:
        st.table(pd.DataFrame({"#": [1, 2, 3], "Takım": ["Galatasaray", "Fenerbahçe", "Beşiktaş"], "P": [45, 41, 38]}))

# --- PAGE: CLUB DETAIL ---
elif st.session_state.page == 'club_detail':
    if st.button("← Maça Geri Dön"): go_to('live_match', target=st.session_state.target)
    st.title(f"🛡️ {st.session_state.club}")
    
    ct1, ct2 = st.tabs(["Fikstür", "Kadro Değerleri"])
    with ct1:
        st.table(pd.DataFrame({"Tarih": ["22 Jan", "29 Jan"], "Rakip": ["Kasımpaşa", "Antalyaspor"], "Yer": ["D", "E"]}))

# --- PAGE:
