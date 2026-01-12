import streamlit as st
import pandas as pd
import plotly.express as px

# --- PIXEL PERFECT UI SETUP ---
st.set_page_config(page_title="DVA Terminal", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus+Jakarta+Sans', sans-serif; background: #fcfcfd; }

    /* Match Center - Üst Bar (image_e8c0aa.jpg tarzı) */
    .match-header {
        display: flex; gap: 12px; overflow-x: auto; padding: 15px;
        background: white; border-bottom: 2px solid #6366f1;
        position: sticky; top: 0; z-index: 999;
    }
    .m-card { 
        min-width: 140px; padding: 12px; background: #f8fafc; border-radius: 14px; 
        text-align: center; border: 1px solid #e2e8f0; font-size: 12px;
    }

    /* Trend Haberler - Kapsüller (image_e844c4.png yapısı) */
    .news-capsule { 
        background: white; border-radius: 20px; padding: 20px; 
        border-top: 4px solid #eee; box-shadow: 0 4px 15px rgba(0,0,0,0.03); 
        margin-bottom: 15px; 
    }
    
    /* Market Heat - Trend Kartları (Butonsuz, image_e8c0c9 tarzı) */
    .heat-card { 
        background: #ffffff; border-radius: 28px; padding: 28px; border: 1px solid #f1f5f9; 
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); cursor: pointer;
    }
    .heat-card:hover { 
        transform: translateY(-10px); 
        box-shadow: 0 25px 50px -12px rgba(99, 102, 241, 0.15);
        border-color: #6366f1;
    }

    /* Pro Profil - Premium Header (image_e8c0c9.jpg ilhamlı) */
    .pro-header {
        background: #0f172a; color: white; padding: 45px; border-radius: 35px;
        position: relative; margin-top: 20px; border: 1px solid #1e293b;
    }
    .dva-tag {
        position: absolute; right: 40px; top: 40px; background: #00d084;
        color: #0f172a; padding: 12px 25px; border-radius: 18px; font-weight: 900;
        box-shadow: 0 0 20px rgba(0, 208, 132, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SİSTEM YÖNETİMİ ---
if 'page' not in st.session_state: st.session_state.page = 'main'

# --- 1. MATCH CENTER (SABİT ÜST ŞERİT) ---
st.markdown('<div class="match-header">', unsafe_allow_html=True)
# Hata alınan 49. satır tamamen düzeltildi (Tırnaklar kapandı)
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
        st.markdown(f'<div class="m-card"><b>{t1} {s} {t2}</b><br><span style="color:#ef4444;">{time}</span></div>', unsafe_allow_html=True)

# --- 2. ANA SAYFA AKIŞI ---
if st.session_state.page == 'main':
    st.title("📡 Trend Haberler")
    h_cols = st.columns(3)
    news_pool = [
        {"brand": "𝕏 @yagosabuncuoglu", "color": "#000", "msg": "ÖZEL: Arda Güler antrenman verilerinde Real Madrid'in en iyisi seçildi."},
        {"brand": "📰 MARCA", "color": "#dc3545", "msg": "Marca: 'Arda Güler etkisi' Madrid'in fiziksel planlarını değiştirdi."},
        {"brand": "🛡️ DVA SMART", "color": "#00d084", "msg": "Analiz: Kerem Aktürkoğlu xG verimliliğinde Benfica tarihine geçiyor."}
    ]
    for i, item in enumerate(news_pool):
        with h_cols[i]:
            st.markdown(f'<div class="news-capsule" style="border-top-color:{item["color"]}"><b>{item["brand"]}</b><p style="font-size:14px; margin-top:12px; color:#475569;">{item["msg"]}</p></div>', unsafe_allow_html=True)

    st.write("---")
    st.markdown("### Market Heat <small style='color:#94a3b8; margin-left:10px;'>Piyasanın Nabzı</small>", unsafe_allow_html=True)
    heat_cols = st.columns(3)
    players = [
        {"name": "Arda Güler", "tag": "REAL MADRID", "status": "DVA Value: €68.4M"},
        {"name": "Semih Kılıçsoy", "tag": "BEŞİKTAŞ", "status": "Scout Interest: 9.2/10"},
        {"name": "Mauro Icardi", "tag": "GALATASARAY", "status": "Metric Leader: Finishing"}
    ]
    for i, p in enumerate(players):
        with heat_cols[i]:
            # Kartın kendisi buton olarak çalışır (Temiz UI)
            st.markdown(f'<div class="heat-card"><small style="color:#6366f1; font-weight:800;">{p["tag"]}</small><h2 style="margin:10px 0;">{p["name"]}</h2><p style="color:#64748b; font-size:14px;">{p["status"]}</p></div>', unsafe_allow_html=True)
            if st.button(f"Detaylı Analiz: {p['name']}", key=f"go_{i}", use_container_width=True):
                st.session_state.selected_player = p['name']
                st.session_state.page = 'profile'
                st.rerun()

# --- 3. DVA PRO (OYUNCU ANALİTİK SAYFASI) ---
else:
    # Hata alınan 101. satır (f-string kapanış hatası) tamamen düzeltildi
    if st.button("← Trendlere Dön"):
        st.session_state.page = 'main'
        st.rerun()

    p_name = st.session_state.get('selected_player', 'Oyuncu')
    st.markdown(f"""
        <div class="pro-header">
            <div class="dva-tag">DVA ANALYTIC: €68.4M</div>
            <h1 style="margin:0; font-size:50px;">{p_name}</h1>
            <p style="color:#94a3b8; margin-top:10px;">Transfermarkt: €45M | <span style="color:#00d084;">Analitik Potansiyel: +%52</span></p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="news-capsule" style="border-top-color:#6366f1;"><h3>Gelişim Karnesi</h3><p>Teknik: 94</p><p>Vizyon: 91</p><p>Fizik: 74</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="news-capsule" style="border-top-color:#00d084;"><h3>Değer Trendi</h3>', unsafe_allow_html=True)
        fig = px.line(x=["Eyl", "Kas", "Oca"], y=[40, 52, 68], markers=True, color_discrete_sequence=['#6366f1'])
        fig.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="news-capsule" style="border-top-color:#f59e0b;"><h3>Creator Studio</h3>', unsafe_allow_html=True)
        st.info("Bu oyuncunun analitik verilerini 1080x1080 formatında sosyal medya kartına dönüştür.")
        if st.button("📸 SOSYAL MEDYA KARTI OLUŞTUR", use_container_width=True):
            st.toast("Tasarım (image_e8c0c9) standartlarında hazırlanıyor...")
        st.markdown('</div>', unsafe_allow_html=True)
