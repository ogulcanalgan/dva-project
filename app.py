import streamlit as st
import pandas as pd
import plotly.express as px

# --- PIXEL PERFECT UI SETUP ---
st.set_page_config(page_title="DVA Pulse & Pro", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus+Jakarta+Sans', sans-serif; background: #fcfcfd; }

    /* Match Center - Sticky Header */
    .match-header {
        display: flex; gap: 15px; overflow-x: auto; padding: 15px;
        background: white; border-bottom: 2px solid #6366f1;
        position: sticky; top: 0; z-index: 999;
    }
    .m-card { min-width: 130px; padding: 8px; background: #f8f9fa; border-radius: 8px; text-align: center; font-size: 11px; border: 1px solid #eee; }

    /* Radar & Heat Cards (Ana Sayfa) */
    .news-capsule { background: white; border-radius: 15px; padding: 18px; border-top: 4px solid #eee; box-shadow: 0 4px 12px rgba(0,0,0,0.03); margin-bottom: 15px; }
    .heat-card { 
        background: #ffffff; border-radius: 20px; padding: 25px; border: 1px solid #f0f2f5; 
        transition: all 0.4s ease; cursor: pointer; border-bottom: 4px solid #f0f2f5;
    }
    .heat-card:hover { transform: translateY(-8px); border-bottom: 4px solid #6366f1; box-shadow: 0 15px 35px rgba(99, 102, 241, 0.1); }

    /* Oyuncu Profili (V18 Pro) */
    .player-profile-header {
        background: linear-gradient(135deg, #101828 0%, #070a11 100%);
        color: white; padding: 40px; border-radius: 30px; margin-top: 20px; position: relative;
    }
    .dva-value-tag { position: absolute; right: 40px; top: 40px; background: rgba(0, 208, 132, 0.1); border: 1px solid #00d084; color: #00d084; padding: 10px 20px; border-radius: 15px; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# --- SAYFA YÖNETİMİ ---
if 'page' not in st.session_state:
    st.session_state.page = 'main'

def go_to_profile(name):
    st.session_state.selected_player = name
    st.session_state.page = 'profile'

# --- 1. MATCH CENTER (HER İKİ SAYFADA DA VAR) ---
st.markdown('<div class="match-header">', unsafe_allow_html=True)
m_cols = st.columns(5)
matches = [("GS", "2-1", "BJK", "72'"), ("RM", "0-0", "BAR", "15'"), ("MC", "3-2", "LIV", "FT"), ("TS", "1-0", "FB", "40'"), ("INT", "1-1", "MIL", "60'
