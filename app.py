import streamlit as st
import pandas as pd
import plotly.express as px

# --- PIXEL PERFECT UI SETUP ---
st.set_page_config(page_title="DVA Terminal", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus+Jakarta+Sans', sans-serif; background: #f8fafc; }

    /* Match Center - Sticky Header */
    .match-header {
        display: flex; gap: 12px; overflow-x: auto; padding: 12px;
        background: white; border-bottom: 1px solid #e2e8f0;
        position: sticky; top: 0; z-index: 999;
    }
    .m-card { min-width: 120px; padding: 10px; background: #ffffff; border-radius: 12px; text-align: center; border: 1px solid #f1f5f9; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }

    /* Trend Haberler (Trend Haberler) */
    .news-capsule { background: white; border-radius: 16px; padding: 20px; border-left: 5px solid #eee; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 10px; }
    
    /* Market Heat (Piyasa Isısı) */
    .heat-card { 
        background: white; border-radius: 24px; padding: 24px; border: 1px solid #f1f5f9; 
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); cursor: pointer;
    }
    .heat-card:hover { transform: translateY(-4px); box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); border-color: #6366f1; }

    /* DVA Pro Header (image_e8c0c9 ilhamlı) */
    .pro-header {
        background: #0f172a; color: white; padding: 40px; border-radius: 32px;
        position: relative; margin-top: 20px; border: 1px solid #1e293b;
    }
    .value-badge {
        position: absolute; right: 40px; top: 40px; background: #00d084;
        color: #0f172a; padding: 12px 24px; border-radius: 16px; font-weight: 800;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SAYFA VE VERİ YÖNETİMİ ---
if 'page' not in st.session_state: st.session_state.page = 'main'

def navigate(p_name):
    st.session_state.selected_player = p_name
    st.session_state.page = 'profile'

# --- 1. MATCH CENTER (SABİT ÜST BAR) ---
# Hata alınan satırı (line 49) tamamen düzelttim
st.markdown('<div class="match-header">', unsafe_allow_html=True)
matches = [
    ("GS", "2-1", "BJK", "72'"), 
    ("RM", "0-0", "BAR", "15'"), 
    ("MC", "3-2", "LIV", "FT"), 
    ("TS", "1-0", "FB", "40'"), 
    ("INT", "1-1", "MIL", "60'")
]
m_cols = st.columns(len(matches))
for i, (t1, s, t2, time) in enumerate(matches):
    with m_cols[i]:
        st.markdown(f'<div class="m-card"><b style="font-size:13px;">{t1} {s} {t2}</b><br><span style="color:#ef4444; font-size:11px;">{time}</span></div>', unsafe_allow_html=True)

# --- 2. SAYFA İÇERİKLERİ ---
if st.session_state.page == 'main':
    st.title("📡 Trend Haberler")
    h_cols = st.columns(3)
    news = [
        {"b": "𝕏 @yagosabuncuoglu", "c": "#000000", "m": "Yağız: Arda Güler antrenmandaki şutuyla Madridlileri büyüledi."},
        {"b": "📰 MARCA", "c": "#dc3545", "m": "Ancelotti: 'Arda'nın dakikaları artacak, fiziksel verileri harika.'"},
        {"b": "🛡️ DVA SMART", "c": "#00d084", "m": "Analiz: Kerem Aktürkoğlu Benfica'da xG liderliğine yükseldi."}
    ]
    for i, item in enumerate(news):
        with h_cols[i]:
            st.markdown(f'<div class="news-capsule" style="border-left-color:{item["c"]}"><b>{item["b"]}</b><p style="margin-top:8px; font-size:14px; color:#475569;">{item["m"]}</p></div>', unsafe_allow_html=True)

    st.write("---")
    st.markdown("### Market Heat <small style='color:#64748b; font-size:14px; margin-left:10px;'>Piyasanın Nabzı</small>", unsafe_allow_html=True)
    heat_cols = st.columns(3)
    heat_list = [
        {"n": "Arda Güler", "tag": "LA LIGA", "v": "Hype Index: 9.8"},
        {"n": "Semih Kılıçsoy", "tag": "SÜPER LİG", "v": "Transfer Interest: High"},
        {"n": "Ferdi Kadıoğlu", "tag": "PREMIER LEAGUE", "v": "Analytic Value Up"}
    ]
    for i, p in enumerate(heat_list):
        with heat_cols[i]:
            # Kartın tamamını tıklanabilir hissettiren temiz yapı
            st.markdown(f'<div class="heat-card"><span style="color:#6366f1; font-weight:800; font-size:10px;">{p["tag"]}</span><h2 style="margin:12px 0;">{p["n"]}</h2><p style="color:#64748b; font-size:14px;">{p["v"]}</p></div>', unsafe_allow_html=True)
            if st.button(f"Analiz", key=f"p_{i}", use_container_width=True):
                navigate(p['n'])
                st.rerun()

else:
    # --- 3. DVA PRO (OYUNCU ANALİTİK SAYFASI) ---
    if st.button("← Ana Sayfaya Dön"):
        st.session_state.page = 'main'
        st.rerun()

    p_name = st.session_state.get('selected_player', 'Arda Güler')
    st.markdown(f"""
