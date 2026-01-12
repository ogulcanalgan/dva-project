import streamlit as st
import pandas as pd
import random

# --- UI & UX ARCHITECTURE ---
st.set_page_config(page_title="DVA Pulse Terminal", layout="wide", initial_sidebar_state="collapsed")

# Session State (Sayfa ve Seçim Yönetimi)
states = {'page': 'main', 'target': None, 'sub_page': 'summary', 'club': None}
for key, val in states.items():
    if key not in st.session_state: st.session_state[key] = val

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus+Jakarta+Sans', sans-serif; background: #f8fafc; }

    /* Kartın Her Yerini Tıklanabilir Yapan CSS */
    .card-container { position: relative; cursor: pointer; }
    .stButton > button { 
        width: 100%; height: 220px; background: transparent !important; color: transparent !important;
        border: none !important; position: absolute; top: 0; left: 0; z-index: 100;
    }
    
    /* Maçkolik Tarzı Puan Durumu ve Fikstür */
    .data-table { width: 100%; background: white; border-radius: 15px; overflow: hidden; border: 1px solid #e2e8f0; }
    .data-header { background: #0f172a; color: white; padding: 10px; font-weight: bold; }
    
    /* Tasarım Kartları (image_f2b9cb) */
    .heat-card-ui { 
        background: white; border-radius: 24px; padding: 25px; border: 1px solid #f1f5f9; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.03); position: relative;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. GLOBAL MATCH CENTER (LIVE HUB) ---
matches = [("GS", "2-1", "BJK", "72'"), ("RM", "0-0", "BAR", "15'"), ("MC", "3-2", "LIV", "FT")]
m_cols = st.columns(len(matches) + 1)
for i, (t1, s, t2, time) in enumerate(matches):
    with m_cols[i]:
        if st.button(f"{t1} {s} {t2}", key=f"m_{i}"):
            st.session_state.target = f"{t1} v {t2}"
            st.session_state.page = 'live_match'
            st.rerun()
        st.markdown(f'<p style="text-align:center; color:red; font-size:11px; margin-top:-35px;">{time}</p>', unsafe_allow_html=True)

# --- 2. DİNAMİK SAYFA MOTORU ---

if st.session_state.page == 'main':
    # ANA SAYFA: MARKET HEAT & TRENDLER
    st.subheader("🔥 Market Heat (Analitik Değerler)")
    h_cols = st.columns(3)
    players = [{"n": "Arda Güler", "v": "€68.4M", "c": "REAL MADRID"}, {"n": "Semih Kılıçsoy", "v": "€22.1M", "c": "BEŞİKTAŞ"}, {"n": "Ferdi Kadıoğlu", "v": "€35.0M", "c": "BRIGHTON"}]
    
    for i, p in enumerate(players):
        with h_cols[i]:
            st.markdown(f'<div class="heat-card-ui"><small style="color:#6366f1;">{p["c"]}</small><h2>{p["n"]}</h2><p style="color:#00d084; font-size:24px; font-weight:800;">{p["v"]}</p></div>', unsafe_allow_html=True)
            if st.button("", key=f"pbtn_{i}"): # Gizli buton tüm kartı kapsar
                st.session_state.target = p['n']
                st.session_state.page = 'profile'
                st.rerun()

elif st.session_state.page == 'live_match':
    # MAÇKOLİK TARZI MAÇ DETAYI (image_f2c0f0)
    if st.button("← Geri"): st.session_state.page = 'main'; st.rerun()
    
    st.title(f"🏟️ {st.session_state.target}")
    tab1, tab2, tab3, tab4 = st.tabs(["Özet", "İstatistik", "Kadrolar", "Puan Durumu"])
    
    with tab1: # Özet & Canlı Skor
        st.markdown('<div style="background:white; padding:20px; border-radius:15px; border:1px solid #6366f1;"><h4>Canlı DVA Rating: 8.2</h4><p>72\' Gol: Osimhen (GS)</p></div>', unsafe_allow_html=True)
    
    with tab2: # Detaylı İstatistik (image_f2c0f0)
        c1, c2, c3 = st.columns(3)
        c1.metric("xG (Beklenen Gol)", "1.84 - 0.92")
        c2.metric("Topla Oynama", "%54 - %46")
        c3.metric("DVA Moment", "Yüksek Baskı", delta="12%")

    with tab3: # Kadrolar & Kulübe Tıklama
        st.subheader("İlk 11'ler")
        k_col1, k_col2 = st.columns(2)
        with k_col1:
            st.write("**Galatasaray**")
            if st.button("Galatasaray SK (Kulübe Git)", use_container_width=True):
                st.session_state.club = "Galatasaray"
                st.session_state.page = 'club_detail'
                st.rerun()
            st.table(pd.DataFrame({"No": [1, 5, 34], "Oyuncu": ["Muslera", "Sanchez", "Torreira"], "DVA": [7.4, 8.1, 7.9]}))

    with tab4: # Puan Durumu
        st.table(pd.DataFrame({"Sıra": [1, 2, 3], "Takım": ["Galatasaray", "Fenerbahçe", "Beşiktaş"], "P": [42, 38, 35]}))

elif st.session_state.page == 'club_detail':
    # KULÜP DETAY & FİKSTÜR
    if st.button("← Maça Dön"): st.session_state.page = 'live_match'; st.rerun()
    st.title(f"🛡️ {st.session_state.club} Kulüp Profili")
    
    ctab1, ctab2 = st.tabs(["Fikstür", "Tüm Kadro"])
    with ctab1:
        st.table(pd.DataFrame({"Tarih": ["20 Jan", "27 Jan"], "Rakip": ["Kasımpaşa (D)", "Antalyaspor (E)"], "Tür": ["Süper Lig", "Süper Lig"]}))
    with ctab2:
        st.write("Kulübün tüm lisanslı oyuncuları ve anlık piyasa değerleri...")

elif st.session_state.page == 'profile':
    # OYUNCU DETAY & 1080x1080 KART (image_f2c455)
    if st.button("← Ana Sayfa"): st.session_state.page = 'main'; st.rerun()
    st.markdown(f'<div style="background:#0f172a; color:white; padding:40px; border-radius:30px;"><h1>{st.session_state.target}</h1></div>', unsafe_allow_html=True)
    
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st
