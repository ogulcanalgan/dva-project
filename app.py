import streamlit as st
import pandas as pd
import plotly.express as px

# --- UI ARCHITECTURE (Clean UI Style) ---
st.set_page_config(page_title="DVA Pulse Terminal", layout="wide", initial_sidebar_state="collapsed")

# Session State Initialization (Kritik: Sayfalar arası geçişi sağlar)
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'target' not in st.session_state: st.session_state.target = None

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus+Jakarta+Sans', sans-serif; background: #fcfcfd; }

    /* Match Center - image_e8c0aa Tarzı */
    .match-header { 
        display: flex; gap: 12px; padding: 15px; background: white; 
        border-bottom: 2px solid #6366f1; position: sticky; top: 0; z-index: 999; 
    }
    
    /* Market Heat Kartları - image_e8c0c9 İlhamlı */
    .heat-card { 
        background: white; border-radius: 28px; padding: 25px; border: 1px solid #f1f5f9; 
        transition: all 0.3s ease; box-shadow: 0 4px 12px rgba(0,0,0,0.02);
        margin-bottom: 10px;
    }
    .heat-card:hover { transform: translateY(-5px); border-color: #6366f1; }

    /* Oyuncu Profil Header (1 Numara / Clean UI) */
    .pro-header {
        background: #0f172a; color: white; padding: 45px; border-radius: 35px;
        position: relative; border: 1px solid #1e293b;
    }
    .dva-tag { 
        position: absolute; right: 40px; top: 40px; background: #00d084; 
        color: #0f172a; padding: 10px 20px; border-radius: 15px; font-weight: 800; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. MATCH CENTER (SABİT ÜST BAR) ---
st.markdown('<div class="match-header">', unsafe_allow_html=True)
# Hatalı satırlar tamamen temizlendi (image_f2a74a çözümü)
matches = [("GS", "2-1", "BJK", "72'"), ("RM", "0-0", "BAR", "15'"), ("MC", "3-2", "LIV", "FT")]
cols = st.columns([1, 1, 1, 2])
for i, (t1, s, t2, time) in enumerate(matches):
    with cols[i]:
        if st.button(f"{t1} {s} {t2}", key=f"match_{i}", use_container_width=True):
            st.session_state.target = f"{t1} v {t2}"
            st.session_state.page = 'live'
            st.rerun()
        st.markdown(f'<p style="text-align:center; color:red; font-size:11px; margin-top:-10px;">{time}</p>', unsafe_allow_html=True)

# --- 2. DİNAMİK SAYFA YÖNETİMİ ---

if st.session_state.page == 'main':
    # --- ANA SAYFA (RADAR & TRENDLER) ---
    st.title("📡 Trend Radar")
    n_cols = st.columns(3)
    news = [
        {"src": "𝕏 @yagosabuncuoglu", "m": "Arda Güler antrenmanda büyülemeye devam ediyor."},
        {"src": "📰 MARCA", "m": "Real Madrid, Arda için özel gelişim programı uyguluyor."},
        {"src": "🛡️ DVA", "m": "Kerem Aktürkoğlu xG verimliliğinde Benfica lideri."}
    ]
    for i, item in enumerate(news):
        with n_cols[i]:
            st.markdown(f'<div style="background:white; padding:20px; border-radius:20px; border-top:4px solid #6366f1;"><b>{item["src"]}</b><br><small>{item["m"]}</small></div>', unsafe_allow_html=True)

    st.write("---")
    st.subheader("🔥 Market Heat (Analitik Değerler)")
    h_cols = st.columns(3)
    players = [
        {"n": "Arda Güler", "v": "€68.4M", "c": "REAL MADRID"},
        {"n": "Semih Kılıçsoy", "v": "€22.1M", "c": "BEŞİKTAŞ"},
        {"n": "Ferdi Kadıoğlu", "v": "€35.0M", "c": "BRIGHTON"}
    ]
    for i, p in enumerate(players):
        with h_cols[i]:
            st.markdown(f'<div class="heat-card"><small style="color:#6366f1; font-weight:800;">{p["c"]}</small><h2>{p["n"]}</h2><p style="color:#00d084; font-weight:800;">{p["v"]}</p></div>', unsafe_allow_html=True)
            if st.button(f"Profil: {p['n']}", key=f"p_{i}", use_container_width=True):
                st.session_state.target = p['n']
                st.session_state.page = 'profile'
                st.rerun()

elif st.session_state.page == 'profile':
    # --- OYUNCU ANALİTİK SAYFASI (image_e8c0c9) ---
    if st.button("← Radar'a Dön"): 
        st.session_state.page = 'main'
        st.rerun()

    st.markdown(f"""
        <div class="pro-header">
            <div class="dva-tag">DVA VALUE: €68.4M</div>
            <h1 style="margin:0; font-size:48px;">{st.session_state.target}</h1>
            <p style="color:#94a3b8; margin-top:10px;">Analitik Potansiyel: +%52 | TM Değeri: €45M</p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.info("Oyuncu performans grafikleri ve analitik veri setleri burada yüklenir.")
    with c2:
        st.subheader("📸 Creator Studio")
        if st.button("📸 1080x1080 KART OLUŞTUR", use_container_width=True):
            st.success("Tasarım Motoru: 1080x1080 PNG Hazırlanıyor...")

elif st.session_state.page == 'live':
    # --- CANLI MAÇ ANALİZİ (image_e8c0aa) ---
    if st.button("← Terminale Dön"): 
        st.session_state.page = 'main'
        st.rerun()
    st.title(f"🏟️ {st.session_state.target}")
    st.markdown('<div style="background:white; padding:40px; border-radius:25px; border:2px solid #6366f1;"><h3>Canlı DVA Rating: 8.4</h3><p>Anlık veri akışı senkronize ediliyor...</p></div>', unsafe_allow_html=True)
