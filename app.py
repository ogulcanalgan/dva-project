import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- UI & UX ARCHITECTURE ---
st.set_page_config(page_title="DVA Pulse Terminal", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus+Jakarta+Sans', sans-serif; background: #fcfcfd; }

    /* Match Center */
    .match-header { display: flex; gap: 12px; overflow-x: auto; padding: 15px; background: white; border-bottom: 2px solid #6366f1; position: sticky; top: 0; z-index: 999; }
    .m-card { min-width: 140px; padding: 12px; background: #f8fafc; border-radius: 14px; text-align: center; border: 1px solid #e2e8f0; cursor: pointer; }
    .m-card:hover { border-color: #6366f1; background: #f1f5f9; }

    /* Creator Studio Card (1080x1080 Mockup) */
    .studio-preview {
        width: 400px; height: 400px; background: linear-gradient(135deg, #101828 0%, #070a11 100%);
        border-radius: 30px; padding: 40px; color: white; position: relative;
        box-shadow: 0 30px 60px rgba(0,0,0,0.3); margin: auto;
    }
    .card-logo { position: absolute; top: 30px; left: 30px; font-weight: 900; color: #6366f1; }
    .card-value { position: absolute; top: 30px; right: 30px; color: #00d084; font-weight: 800; border: 1px solid #00d084; padding: 5px 10px; border-radius: 10px; font-size: 12px; }

    /* Global Trend Cards */
    .heat-card { background: white; border-radius: 28px; padding: 25px; border: 1px solid #f1f5f9; transition: all 0.4s ease; cursor: pointer; }
    .heat-card:hover { transform: translateY(-8px); border-color: #6366f1; box-shadow: 0 20px 40px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION MANAGEMENT ---
if 'view' not in st.session_state: st.session_state.view = 'main'

# --- 1. MATCH CENTER (LIVE DATA ENGINE) ---
st.markdown('<div class="match-header">', unsafe_allow_html=True)
matches = [("GS", "2-1", "BJK", "72'"), ("RM", "0-0", "BAR", "15'"), ("MC", "3-2", "LIV", "FT")]
m_cols = st.columns(len(matches) + 2)
for i, (t1, s, t2, time) in enumerate(matches):
    with m_cols[i]:
        if st.button(f"{t1} {s} {t2}", key=f"m_{i}"):
            st.session_state.view = 'match_detail'
            st.session_state.active_match = f"{t1} v {t2}"
        st.markdown(f'<div style="text-align:center; font-size:10px; color:red; margin-top:-15px;">{time}</div>', unsafe_allow_html=True)

# --- 2. MAIN HUB (TRENDS & NEWS) ---
if st.session_state.view == 'main':
    st.title("📡 DVA Trend Radar")
    c1, c2, c3 = st.columns(3)
    news = [("𝕏 @burhancanterzi", "GS transferde vites yükseltti."), ("📰 MARCA", "Arda Güler için Real Madrid'den özel karar."), ("🛡️ DVA SMART", "Benfica'da Kerem Aktürkoğlu çılgınlığı.")]
    for i, (src, txt) in enumerate(news):
        with [c1, c2, c3][i]:
            st.markdown(f'<div style="background:white; padding:20px; border-radius:20px; border-top:4px solid #6366f1;"><b>{src}</b><br><small>{txt}</small></div>', unsafe_allow_html=True)

    st.write("---")
