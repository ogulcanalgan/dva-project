import streamlit as st
import pandas as pd
import random

# --- UI & TERMINAL STYLE ---
st.set_page_config(page_title="DVA Pulse", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Match Center (Canlı Skorlar) */
    .match-strip {
        display: flex; gap: 20px; overflow-x: auto; padding: 10px 0;
        border-bottom: 1px solid #f0f2f5; margin-bottom: 20px;
    }
    .match-card {
        min-width: 150px; background: #fff; padding: 10px; border-radius: 12px;
        border: 1px solid #eee; text-align: center; font-size: 12px;
    }

    /* Market Heat (Trend) Kartları - Tıklanabilir Efekt */
    .heat-card {
        background: #ffffff; border: 1px solid #f0f2f5; border-radius: 16px;
        padding: 20px; cursor: pointer; transition: all 0.3s ease;
        border-bottom: 4px solid #f0f2f5;
    }
    .heat-card:hover { border-bottom: 4px solid #6366f1; transform: translateY(-5px); }
    
    .status-badge { font-size: 11px; font-weight: 700; color: #6366f1; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. MATCH CENTER (CANLI SKORLAR) ---
st.markdown('<div class="match-strip">', unsafe_allow_html=True)
matches = [
    {"t1": "GS", "t2": "BJK", "s": "2 - 1", "min": "72'"},
    {"t1": "RM", "t2": "BAR", "s": "0 - 0", "min": "15'"},
    {"t1": "MC", "t2": "LIV", "s": "3 - 2", "min": "FT"}
]
m_cols = st.columns(len(matches))
for i, m in enumerate(matches):
    with m_cols[i]:
        st.markdown(f"""
            <div class="match-card">
                <b>{m['t1']} {m['s']} {m['t2']}</b><br>
                <span style="color:red;">{m['min']}</span>
            </div>
        """, unsafe_allow_html=True)

# --- 2. DVA RADAR (ESKİ HABER AKIŞI) ---
st.title("📡 DVA Radar")
r_cols = st.columns(3)
radar_news = [
    {"h": "@yagosabuncuoglu", "t": "𝕏", "msg": "Burhan Can Terzi: GS orta saha için yeni bir isimle temas kurdu."},
    {"h": "@emrekaplan61", "t": "𝕏", "msg": "Emre Kaplan: Florya'da idman temposu verilerle takip ediliyor."},
    {"h": "DVA SMART", "t": "DATA", "msg": "Süper Lig'in pas isabet rekoru bu hafta kırılabilir."}
]

for i, n in enumerate(radar_news):
    with r_cols[i]:
        st.markdown(f"""
            <div style="background:white; pading:15px; border-radius:15px; border:1px solid #eee; padding:15px;">
                <small><b>{n['t']}</b> {n['h']}</small><br>
                <p style="font-size:14px; margin-top:8px;">{n['msg']}</p>
            </div>
        """, unsafe_allow_html=True)

# --- 3. MARKET HEAT (TREND & SÖYLENTİ) ---
st.write("---")
st.subheader("🔥 Market Heat")
h_cols = st.columns(3)
heat_data = [
    {"n": "Semih Kılıçsoy", "val": "Form Index: 9.2", "note": "PL Scouts Tracking"},
    {"n": "Ferdi Kadıoğlu", "val": "Market Value Up", "note": "Bundesliga Interest"},
    {"n": "Barış Alper", "val": "Sustain Rate: %88", "note": "Ligue 1 Target"}
]

for i, item in enumerate(heat_data):
    with h_cols[i]:
        # Kartın tamamı artık tıklanabilir hissi veriyor (hover efekti eklendi)
        st.markdown(f"""
            <div class="heat-card">
                <span class="status-badge">{item['note']}</span>
                <h3 style="margin:10px 0;">{item['n']}</h3>
                <p style="font-size:13px; color:#666;">{item['val']}</p>
            </div>
        """, unsafe_allow_html=True)
        # Buton yerine kartın altına görünmez bir tıklama alanı veya küçük bir link eklenebilir
        if st.button(f"View Profile", key=f"p_{i}", use_container_width=True):
            st.switch_page("pages/player_profile.py") # Örnek yönlendirme
