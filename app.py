import streamlit as st
import pandas as pd

# --- UI & UX ARCHITECTURE ---
st.set_page_config(page_title="DVA Pulse", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #fcfcfd; }

    /* Match Center - Sticky Top Bar */
    .match-header {
        display: flex; gap: 15px; overflow-x: auto; padding: 15px;
        background: white; border-bottom: 2px solid #6366f1;
        position: sticky; top: 0; z-index: 999;
    }
    .m-card {
        min-width: 130px; padding: 8px; border-radius: 8px; background: #f8f9fa;
        text-align: center; border: 1px solid #eee; font-size: 11px;
    }

    /* Haber Kartları - Renkli Logolar */
    .news-capsule {
        background: white; border-radius: 15px; padding: 18px;
        min-width: 310px; border-top: 4px solid #eee; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    .source-brand { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
    .brand-marca { border-top-color: #dc3545; } /* Marca Kırmızısı */
    .brand-x { border-top-color: #000000; }     /* X Siyahı */
    .brand-dva { border-top-color: #00d084; }   /* DVA Yeşili */

    /* Market Heat Kartları - Butonsuz & Temiz */
    .heat-card {
        background: #ffffff; border-radius: 20px; padding: 25px;
        border: 1px solid #f0f2f5; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer; position: relative;
    }
    .heat-card:hover { 
        transform: translateY(-8px); 
        box-shadow: 0 15px 35px rgba(99, 102, 241, 0.1); 
        border-color: #6366f1;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. MATCH CENTER (TOP BAR) ---
st.markdown('<div class="match-header">', unsafe_allow_html=True)
m_cols = st.columns(5)
matches = [("GS", "2-1", "BJK", "72'"), ("RM", "0-0", "BAR", "15'"), ("MC", "3-2", "LIV", "FT"), ("TS", "1-0", "FB", "40'"), ("INT", "1-1", "MIL", "60'")]
for i, (t1, s, t2, time) in enumerate(matches):
    with m_cols[i]:
        st.markdown(f'<div class="m-card"><b>{t1} {s} {t2}</b><br><span style="color:red;">{time}</span></div>', unsafe_allow_html=True)

# --- 2. TREND HABERLER (RENKLİ KAYNAKLAR) ---
st.title("📡 Trend Haberler")
h_cols = st.columns(3)
news_items = [
    {"b": "𝕏 @yagosabuncuoglu", "class": "brand-x", "msg": "Yağız: Fenerbahçe forvet transferinde sona yaklaştı."},
    {"b": "📰 MARCA", "class": "brand-marca", "msg": "Real Madrid, Arda Güler için özel program hazırladı."},
    {"b": "🛡️ DVA SMART", "class": "brand-dva", "msg": "DVA Analiz: Kerem Aktürkoğlu xG verimliliğinde ilk 3'e girdi."}
]
for i, item in enumerate(news_items):
    with h_cols[i]:
        st.markdown(f"""
            <div class="news-capsule {item['class']}">
                <div class="source-brand"><b>{item['b']}</b></div>
                <p style="font-size:14px; font-weight:600;">{item['msg']}</p>
                <a href="#" style="font-size:11px; color:#6366f1;">Kaynağa Git →</a>
            </div>
        """, unsafe_allow_html=True)

# --- 3. MARKET HEAT (EVRENSEL & ŞIK) ---
st.write("---")
st.markdown("### Market Heat <small style='color:#888; font-size:14px;'>(Piyasanın Nabzı)</small>", unsafe_allow_html=True)
heat_cols = st.columns(3)
heat_data = [
    {"n": "Semih Kılıçsoy", "val": "Form: 9.2", "tag": "PL SCOUTING"},
    {"n": "Ferdi Kadıoğlu", "val": "Value: +€5M", "tag": "BUNDESLIGA"},
    {"n": "Icardi", "val": "DVA Point: 94", "tag": "SÜPER LİG"}
]
for i, h in enumerate(heat_data):
    with heat_cols[i]:
        # Tıklanabilir alan simülasyonu
        if st.button(f"", key=f"click_{i}", help="Profile Git", use_container_width=True):
             st.toast(f"{h['n']} profiline yönlendiriliyor...")
        
        st.markdown(f"""
            <div class="heat-card">
                <span style="font-size:10px; font-weight:800; color:#6366f1;">{h['tag']}</span>
                <h2 style="margin:15px 0 5px 0;">{h['n']}</h2>
                <p style="color:#666; font-size:14px;">{h['val']}</p>
            </div>
        """, unsafe_allow_html=True)
