import streamlit as st
import pandas as pd
import random

# --- UI ARCHITECTURE ---
st.set_page_config(page_title="DVA Terminal", layout="wide", initial_sidebar_state="collapsed")

# Session State
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'target' not in st.session_state: st.session_state.target = None

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus+Jakarta+Sans', sans-serif; background: #fcfcfd; }

    /* Market Heat - Tıklanabilir Kartlar (image_f2b9cb.png iyileştirmesi) */
    .stButton > button { border-radius: 20px; }
    .clickable-card {
        position: relative; background: white; border-radius: 28px; padding: 30px; 
        border: 1px solid #f1f5f9; transition: all 0.3s ease; height: 220px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.02);
    }
    .clickable-card:hover { transform: translateY(-8px); border-color: #6366f1; box-shadow: 0 20px 40px rgba(99, 102, 241, 0.1); }
    
    /* Butonu Tüm Karta Yayma */
    .card-overlay-btn {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: transparent; border: none; cursor: pointer; z-index: 10;
    }

    /* Live Data Box - image_f2b9f1.png dolgusu */
    .live-stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 20px; }
    .stat-item { background: #f8fafc; padding: 15px; border-radius: 15px; text-align: center; border: 1px solid #e2e8f0; }

    /* Oyuncu Profili - image_f2bd2f.png dolgusu */
    .pro-banner { background: #0f172a; color: white; padding: 50px; border-radius: 35px; position: relative; overflow: hidden; }
    .value-badge { background: #00d084; color: #0f172a; padding: 12px 24px; border-radius: 18px; font-weight: 800; float: right; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. MATCH CENTER (ÜST ŞERİT) ---
m_list = [("GS", "2-1", "BJK", "72'"), ("RM", "0-0", "BAR", "15'"), ("MC", "3-2", "LIV", "FT")]
cols = st.columns(len(m_list) + 1)
for i, (t1, s, t2, time) in enumerate(m_list):
    with cols[i]:
        if st.button(f"{t1} {s} {t2}\n{time}", key=f"m_{i}", use_container_width=True):
            st.session_state.target = f"{t1} v {t2}"
            st.session_state.page = 'live'
            st.rerun()

# --- 2. SAYFA YÖNETİMİ ---

if st.session_state.page == 'main':
    st.title("📡 Trend Radar")
    # Radar Kartları (image_f2b9cb.png)
    h_cols = st.columns(3)
    players = [
        {"n": "Arda Güler", "v": "€68.4M", "t": "REAL MADRID", "s": "Hype: +45%"},
        {"n": "Semih Kılıçsoy", "v": "€22.1M", "t": "BEŞİKTAŞ", "s": "Scout Score: 9.2"},
        {"n": "Ferdi Kadıoğlu", "v": "€35.0M", "t": "BRIGHTON", "s": "DVA Index: 88"}
    ]
    for i, p in enumerate(players):
        with h_cols[i]:
            st.markdown(f"""
                <div class="clickable-card">
                    <small style="color:#6366f1; font-weight:800;">{p['t']}</small>
                    <h2 style="margin:10px 0;">{p['n']}</h2>
                    <p style="color:#00d084; font-size:24px; font-weight:800; margin:0;">{p['v']}</p>
                    <p style="color:#94a3b8; font-size:14px; margin-top:10px;">{p['s']}</p>
                </div>
            """, unsafe_allow_html=True)
            # Kartın her yerine tıklama özelliği
            if st.button(f"Giti {p['n']}", key=f"p_{i}", use_container_width=True):
                st.session_state.target = p['n']
                st.session_state.page = 'profile'
                st.rerun()

elif st.session_state.page == 'live':
    # CANLI MAÇ SAYFASI (image_f2b9f1.png iyileştirmesi)
    if st.button("← Terminale Dön"): st.session_state.page = 'main'; st.rerun()
    
    st.header(f"🏟️ {st.session_state.target} | Maç Analitiği")
    st.markdown(f"""
        <div style="background:white; padding:30px; border-radius:25px; border:2px solid #6366f1;">
            <h1 style="color:#6366f1; text-align:center;">DVA Canlı Rating: {random.uniform(7.5, 9.2):.1f}</h1>
            <div class="live-stat-grid">
                <div class="stat-item"><b>xG (Beklenen Gol)</b><br><span style="font-size:20px; color:#6366f1;">1.84 - 0.92</span></div>
                <div class="stat-item"><b>Topla Oynama</b><br><span style="font-size:20px;">%54 - %46</span></div>
                <div class="stat-item"><b>DVA Moment</b><br><span style="font-size:20px; color:#00d084;">Yüksek Baskı</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == 'profile':
    # OYUNCU PROFİLİ (image_f2bd2f.png iyileştirmesi)
    if st.button("← Radar'a Dön"): st.session_state.page = 'main'; st.rerun()
    
    st.markdown(f"""
        <div class="pro-banner">
            <div class="value-badge">DVA VALUE: €68.4M</div>
            <h1 style="font-size:50px; margin:0;">{st.session_state.target}</h1>
            <p style="color:#94a3b8; margin-top:10px;">Potansiyel Tavan: +%52 | Form Durumu: Mükemmel</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📊 Performans Trendi")
        # Dolu grafik (image_e8c0c9 tarzı)
        chart_data = pd.DataFrame({"Hafta": [1,2,3,4,5], "Puan": [7.2, 7.8, 8.1, 7.9, 8.8]})
        st.line_chart(chart_data.set_index("Hafta"), color="#6366f1")
    
    with col2:
        st.subheader("📸 Creator Studio")
        if st.button("🖼️ 1080x1080 TASARIMI ÜRET", use_container_width=True):
            with st.spinner("Görsel motoru çalıştırılıyor..."):
                st.success(f"{st.session_state.target} için sosyal medya kartı oluşturuldu!")
                # Kart görseli simülasyonu
                st.markdown(f"""
                    <div style="width:100%; height:300px; background:#101828; border-radius:20px; display:flex; flex-direction:column; align-items:center; justify-content:center; color:white; border:4px solid #00d084;">
                        <h2 style="margin:0;">{st.session_state.target}</h2>
                        <p style="color:#00d084; font-size:30px; font-weight:800;">€68.4M</p>
                        <small>DVA PROJECT EXCLUSIVE</small>
                    </div>
                """, unsafe_allow_html=True)
