import streamlit as st
import pandas as pd
import random

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="DVA Pulse Terminal", layout="wide", initial_sidebar_state="collapsed")

# Session State Yönetimi (Patlamayı önleyen yapı)
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'target' not in st.session_state: st.session_state.target = None
if 'club' not in st.session_state: st.session_state.club = None

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus+Jakarta+Sans', sans-serif; background: #f1f5f9; }
    
    /* Kartların Tamamını Tıklanabilir Yapan Mekanizma */
    .stButton > button { 
        width: 100%; border-radius: 20px; border: 1px solid #e2e8f0; 
        background: white; color: #1e293b; transition: all 0.2s;
        text-align: left; padding: 20px;
    }
    .stButton > button:hover { border-color: #6366f1; transform: translateY(-2px); box-shadow: 0 10px 20px rgba(0,0,0,0.05); }

    /* Kulüp & Oyuncu Kart Tasarımları */
    .pro-banner { background: #0f172a; color: white; padding: 40px; border-radius: 30px; margin-bottom: 25px; }
    .stat-card { background: white; padding: 15px; border-radius: 15px; border-bottom: 4px solid #6366f1; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ÜST MAÇ ŞERİDİ (CANLI) ---
matches = [("GS", "2-1", "BJK", "74'"), ("RM", "0-0", "BAR", "18'"), ("MC", "3-2", "LIV", "MS")]
m_cols = st.columns(len(matches))
for i, (t1, s, t2, time) in enumerate(matches):
    with m_cols[i]:
        if st.button(f"🏟️ {t1} {s} {t2} | {time}", key=f"m_{i}"):
            st.session_state.target = f"{t1} v {t2}"
            st.session_state.page = 'live_match'
            st.rerun()

st.divider()

# --- 3. ANA SAYFA (RADAR & MARKET) ---
if st.session_state.page == 'main':
    st.title("📡 DVA Trend Radar")
    
    col_a, col_b, col_c = st.columns(3)
    players = [
        {"n": "Arda Güler", "v": "€68.4M", "t": "REAL MADRID", "s": "Yükselişte"},
        {"n": "Semih Kılıçsoy", "v": "€22.1M", "t": "BEŞİKTAŞ", "s": "Scout Alarmı"},
        {"n": "Ferdi Kadıoğlu", "v": "€35.0M", "t": "BRIGHTON", "s": "Stabil"}
    ]
    
    for idx, p in enumerate(players):
        with [col_a, col_b, col_c][idx]:
            # Kartın tamamını buton yapıyoruz
            if st.button(f"🔥 {p['t']}\n\n{p['n']}\nValue: {p['v']}\n{p['s']}", key=f"p_{idx}"):
                st.session_state.target = p['n']
                st.session_state.page = 'profile'
                st.rerun()

# --- 4. CANLI MAÇ DETAY (MAÇKOLİK MODU) ---
elif st.session_state.page == 'live_match':
    if st.button("← Terminale Dön"): st.session_state.page = 'main'; st.rerun()
    
    st.header(f"🏟️ {st.session_state.target} | Maç Analitiği")
    
    t1, t2, t3, t4 = st.tabs(["📊 İstatistik", "📋 Kadrolar", "📉 Puan Durumu", "📅 Fikstür"])
    
    with t1: # Canlı İstatistikler (image_f2c0f0)
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown('<div class="stat-card"><b>xG (Beklenen Gol)</b><h3>1.84 - 0.92</h3></div>', unsafe_allow_html=True)
        with c2: st.markdown('<div class="stat-card"><b>Top
