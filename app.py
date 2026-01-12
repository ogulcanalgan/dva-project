import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="DVA Terminal v3.1", layout="wide", initial_sidebar_state="collapsed")

# Session State
if 'nav' not in st.session_state: 
    st.session_state.nav = {'page': 'HUB', 'target': None}

def navigate(page, target=None):
    st.session_state.nav['page'] = page
    st.session_state.nav['target'] = target
    st.rerun()

# --- CSS: Kartın TAMAMINI tıklanabilir yapma ve Haber Stili ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* Haber Kartları (image_e8a608) */
    .news-card { background: white; border-radius: 15px; padding: 15px; border-left: 5px solid #6366f1; margin-bottom: 10px; height: 120px; }
    
    /* Piyasa Kartları (Tamamı Tıklanabilir Buton) */
    div.stButton > button {
        width: 100%; height: 200px; border-radius: 20px; border: 1px solid #f1f5f9;
        background: white; color: #0f172a; text-align: left; padding: 25px;
        transition: 0.3s; box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    div.stButton > button:hover { border-color: #6366f1; transform: translateY(-5px); box-shadow: 0 12px 24px rgba(0,0,0,0.08); }
    
    .price { color: #00d084; font-size: 24px; font-weight: 800; display: block; margin-top: 10px; }
    .club-label { color: #64748b; font-size: 14px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# --- PAGE: GLOBAL HUB ---
if st.session_state.nav['page'] == 'HUB':
    st.title("📡 DVA Global Radar")
    
    # 1. Haber Kaynağı (image_e8a608'deki eksik kısım)
    st.markdown("### 🌍 Global & Yerel Veri Akışı")
    n1, n2, n3 = st.columns(3)
    news = [
        {"src": "@burhancanterzi", "msg": "Galatasaray'da orta saha transferi için liste daraldı."},
        {"src": "@yunusemresel", "msg": "Trabzonspor'da golcü arayışlarında yeni rota Kuzey Avrupa."},
        {"src": "@yagosabuncuoglu", "msg": "Fenerbahçe, En-Nesyri için son teklifini yaptı."}
    ]
    for i, n in enumerate(news):
        with [n1, n2, n3][i]:
            st.markdown(f"<div class='news-card'><b>{n['src']}</b><br><small>{n['msg']}</small></div>", unsafe_allow_html=True)

    st.divider()

    # 2. Canlı Skorlar Şeridi (image_f2c0f0)
    st.markdown("### 🏟️ Canlı Skorlar")
    m_cols = st.columns(3)
    matches = [("GS", "2-1", "BJK", "78'"), ("RM", "0-0", "BAR", "21'"), ("MC", "3-2", "LIV", "MS")]
    for i, (h, s, a, t) in enumerate(matches):
        if m_cols[i].button(f"🏟️ {h} {s} {a} | {t}", key=f"m_{i}"):
            navigate('MATCH', target=f"{h} v {a}")

    st.divider()

    # 3. Market Heat (Tam Tıklanabilir Kartlar - image_f2b9cb)
    st.markdown("### 🔥 Market Heat (Analitik Değerler)")
    p_cols = st.columns(3)
    players = [
        {"n": "Semih Kılıçsoy", "v": "€22.1M", "c": "BEŞİKTAŞ"},
        {"n": "Arda Güler", "v": "€68.4M", "c": "REAL MADRID"},
        {"n": "Ferdi Kadıoğlu", "v": "€35.0M", "c": "BRIGHTON"}
    ]
    for i, p in enumerate(players):
        with p_cols[i]:
            # Kartın tamamını butonun içine gömdük
            btn_label = f"{p['c']}\n{p['n']}\n\n{p['v']}"
            if st.button(btn_label, key=f"p_{i}"):
                navigate('PROFILE', target=p['n'])

# --- PAGE: MATCH DETAIL (Maçkolik Modu) ---
elif st.session_state.nav['page'] == 'MATCH':
    if st.button("← Terminale Dön"): navigate('HUB')
    st.header(f"🏟️ {st.session_state.nav['target']} | Analiz")
    
    t1, t2, t3 = st.tabs(["📊 İstatistik", "📋 Kadrol
