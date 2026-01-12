import streamlit as st
import pandas as pd
import plotly.express as px

# --- UI & UX CONFIG ---
st.set_page_config(page_title="DVA Terminal", layout="wide", initial_sidebar_state="collapsed")

# Session State başlatma (Hata almamak için kritik)
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'selected_player' not in st.session_state: st.session_state.selected_player = None
if 'active_match' not in st.session_state: st.session_state.active_match = None

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus+Jakarta+Sans', sans-serif; background: #fcfcfd; }

    /* Match Center */
    .match-header { display: flex; gap: 12px; padding: 10px; background: white; border-bottom: 2px solid #6366f1; position: sticky; top: 0; z-index: 999; }
    
    /* Market Heat Kartları (image_e8c0c9 ilhamlı) */
    .heat-card { 
        background: white; border-radius: 24px; padding: 25px; border: 1px solid #f1f5f9; 
        transition: all 0.3s ease; border-bottom: 5px solid #f1f5f9;
    }
    .heat-card:hover { transform: translateY(-5px); border-bottom: 5px solid #6366f1; box-shadow: 0 15px 30px rgba(0,0,0,0.05); }

    /* Premium Profile Header */
    .pro-header {
        background: #0f172a; color: white; padding: 40px; border-radius: 30px;
        position: relative; border: 1px solid #1e293b;
    }
    .dva-tag { position: absolute; right: 30px; top: 30px; background: #00d084; color: #0f172a; padding: 8px 16px; border-radius: 12px; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. MATCH CENTER (SABİT ÜST BAR) ---
st.markdown('<div class="match-header">', unsafe_allow_html=True)
m_cols = st.columns([1,1,1,1,1])
matches = [("GS", "2-1", "BJK", "72'"), ("RM", "0-0", "BAR", "15'"), ("MC", "3-2", "LIV", "FT")]

for i, (t1, s, t2, time) in enumerate(matches):
    with m_cols[i]:
        # Tıklanabilir skor butonu
        if st.button(f"{t1} {s} {t2}", key=f"m_{i}", use_container_width=True):
            st.session_state.active_match = f"{t1} v {t2}"
            st.session_state.view = 'match_detail'
            st.rerun()
        st.markdown(f'<p style="text-align:center; color:red; font-size:10px; margin-top:-10px;">{time}</p>', unsafe_allow_html=True)

# --- 2. SAYFA YÖNETİMİ ---

# --- ANA SAYFA ---
if st.session_state.view == 'main':
    st.title("📡 Trend Haberler")
    h_cols = st.columns(3)
    news = [
        {"b": "𝕏 @yagosabuncuoglu", "c": "#000", "m": "Yağız: Arda Güler antrenman verilerinde zirvede."},
        {"b": "📰 MARCA", "c": "#dc3545", "m": "Marca: Real Madrid, Arda'nın fiziksel gelişimini kutluyor."},
        {"b": "🛡️ DVA SMART", "c": "#00d084", "m": "DVA: Kerem Aktürkoğlu xG liderliğine yükseldi."}
    ]
    for i, item in enumerate(news):
        with h_cols[i]:
            st.markdown(f'<div style="background:white; padding:20px; border-radius:15px; border-left:5px solid {item["c"]}; box-shadow: 0 2px 10px rgba(0,0,0,0.02);"><b>{item["b"]}</b><p style="font-size:14px; margin-top:10px;">{item["m"]}</p></div>', unsafe_allow_html=True)

    st.write("---")
    st.subheader("🔥 Market Heat")
    p_cols = st.columns(3)
    players = [
        {"n": "Arda Güler", "t": "REAL MADRID", "v": "€68.4M"},
        {"n": "Semih Kılıçsoy", "t": "BEŞİKTAŞ", "v": "€22.1M"},
        {"n": "Ferdi Kadıoğlu", "t": "BRIGHTON", "v": "€35.0M"}
    ]
    for i, p in enumerate(players):
        with p_cols[i]:
            # Kart Görseli
            st.markdown(f"""
                <div class="heat-card">
                    <small style="color:#6366f1; font-weight:800;">{p['t']}</small>
                    <h2 style="margin:10px 0;">{p['n']}</h2>
                    <p style="color:#00d084; font-weight:800;">{p['v']}</p>
                </div>
            """, unsafe_allow_html=True)
            # Kartın altındaki görünmez tıklama alanı
            if st.button(f"Analiz Et: {p['n']}", key=f"pbtn_{i}", use_container_width=True):
                st.session_state.selected_player = p['n']
                st.session_state.view = 'profile'
                st.rerun()

# --- OYUNCU PROFİL SAYFASI ---
elif st.session_state.view == 'profile':
    if st.button("← Ana Sayfaya Dön"): 
        st.session_state.view = 'main'
        st.rerun()

    st.markdown(f"""
        <div class="pro-header">
            <div class="dva-tag">DVA ANALYTIC: €
