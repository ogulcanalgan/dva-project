import streamlit as st
import pandas as pd
import random

# --- 1. GLOBAL UI CONFIG ---
st.set_page_config(page_title="DVA Terminal v3.0", layout="wide", initial_sidebar_state="collapsed")

# Tüm sayfaları kontrol eden merkezi state yönetimi
if 'nav' not in st.session_state: 
    st.session_state.nav = {'page': 'DASHBOARD', 'target': None, 'sub': 'STATS'}

def navigate(page, target=None):
    st.session_state.nav['page'] = page
    st.session_state.nav['target'] = target
    st.rerun()

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* Maçkolik & Transfermarkt Hibrit Kart Tasarımı */
    .card-base { 
        background: white; border-radius: 20px; padding: 25px; 
        border: 1px solid #f1f5f9; position: relative; transition: 0.3s;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03); margin-bottom: 20px;
    }
    .card-base:hover { border-color: #6366f1; transform: translateY(-5px); }
    
    /* Tıklanabilir Alanlar İçin CSS */
    .clickable-overlay {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        z-index: 10; cursor: pointer; background: transparent;
    }
    
    .live-dot { height: 10px; width: 10px; background-color: #ff4b4b; border-radius: 50%; display: inline-block; margin-right: 5px; }
    .price-tag { color: #00d084; font-weight: 800; font-size: 22px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. DİNAMİK NAVİGASYON MOTORU ---

# A. ANA PANEL (TREND RADAR & MARKET)
if st.session_state.nav['page'] == 'DASHBOARD':
    st.title("📡 DVA Global Radar")
    
    # Canlı Maçlar Üst Bar (image_f2c0f0 ilhamı)
    st.markdown("### 🏟️ Canlı Skorlar")
    m_cols = st.columns(3)
    matches = [("GS", "2-1", "BJK", "78'"), ("RM", "0-0", "BAR", "21'"), ("MC", "3-2", "LIV", "MS")]
    for i, (h, s, a, t) in enumerate(matches):
        with m_cols[i]:
            if st.button(f"{h} {s} {a} ({t})", key=f"match_{i}", use_container_width=True):
                navigate('MATCH_DETAIL', target=f"{h} v {a}")

    st.divider()

    # Trend Oyuncular (image_f2b9cb ilhamı - Kartın her yeri tıklanabilir)
    st.markdown("### 🔥 Market Heat (Piyasa Değerleri)")
    p_cols = st.columns(3)
    players = [
        {"name": "Semih Kılıçsoy", "val": "€22.1M", "club": "Beşiktaş"},
        {"name": "Arda Güler", "val": "€68.4M", "club": "Real Madrid"},
        {"name": "Ferdi Kadıoğlu", "val": "€35.0M", "club": "Brighton"}
    ]
    for i, p in enumerate(players):
        with p_cols[i]:
            st.markdown(f"""
                <div class="card-base">
                    <small style="color: #6366f1;">{p['club']}</small>
                    <h2>{p['name']}</h2>
                    <div class="price-tag">{p['val']}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Detay: {p['name']}", key=f"pbtn_{i}", use_container_width=True):
                navigate('PLAYER_PROFILE', target=p['name'])

# B. MAÇ DETAY SAYFASI (MAÇKOLİK MODU)
elif st.session_state.nav['page'] == 'MATCH_DETAIL':
    if st.button("← Geri Dön"): navigate('DASHBOARD')
    st.header(f"🏟️ {st.session_state.nav['target']} | Maç Analitiği")
    
    # Maçkolik Sekmeleri (image_f2c0f0)
    tabs = st.tabs(["📊 İstatistik", "📋 Kadrolar", "📉 Puan Durumu", "📅 Fikstür"])
    
    with tabs[0]: # İstatistik
        c1, c2, c3 = st.columns(3)
        c1.metric("xG (Beklenen Gol)", "1.84 - 0.92")
        c2
