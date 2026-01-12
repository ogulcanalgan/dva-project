import streamlit as st
import pandas as pd

# --- MOBILE-FIRST & CLEAN UI ---
st.set_page_config(page_title="DVA Pulse", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
    
    /* Haber Kutuları (Twitter & Gazete Ayrımı) */
    .news-box { 
        background: white; padding: 15px; border-radius: 12px; margin-bottom: 15px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.04); border-left: 5px solid #1DA1F2; /* Twitter Mavisi */
    }
    .gazete-box { border-left: 5px solid #dc3545; } /* Gazete Kırmızısı */
    
    .news-header { font-size: 11px; color: #888; font-weight: 800; text-transform: uppercase; margin-bottom: 5px; }
    .tweet-link { color: #1DA1F2; text-decoration: none; font-weight: 600; }
    
    /* Studio Header */
    .studio-card {
        background: #101828; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETİ ---
if 'players_df' not in st.session_state:
    st.session_state.players_df = pd.DataFrame([
        {"Name": "E. Haaland", "Team": "Man City", "Perf": 88, "Gls": 1.12, "Ast": 0.15, "xG": 0.95, "Pass": 78},
        {"Name": "Lamine Yamal", "Team": "Barcelona", "Perf": 95, "Gls": 0.35, "Ast": 0.55, "xG": 0.45, "Pass": 81},
        {"Name": "Rodri", "Team": "Man City", "Perf": 92, "Gls": 0.18, "Ast": 0.25, "xG": 0.12, "Pass": 94},
        {"Name": "Arda Güler", "Team": "Real Madrid", "Perf": 85, "Gls": 0.40, "Ast": 0.30, "xG": 0.38, "Pass": 89}
    ])

# --- 1. TICKER & SEARCH ---
st.markdown('<div style="background:#f1f3f5; padding:8px; border-radius:8px; font-size:12px; text-align:center;"><b>HYPE:</b> Arda Güler +45% | <b>ALERT:</b> Rodri %94 Pas İsabeti</div>', unsafe_allow_html=True)
st.title("📡 DVA Pulse")
st.text_input("", placeholder="🔍 Fabrizio Romano, Marca veya 'Haaland' ara...")

tab_feed, tab_studio = st.tabs(["🏠 Akış", "🎨 Studio"])

# --- 2. AKIŞ (HABER & TWITTER) ---
with tab_feed:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("🌐 Global Veri Akışı")
        
        # Twitter Örneği (Referanslı)
        st.markdown(f"""
            <div class="news-box">
                <div class="news-header">🐦 Twitter / @FabrizioRomano</div>
                <div><b>Here we go!</b> Lamine Yamal'ın performans puanı DVA verilerinde 95'e ulaştı. Yeni sözleşme görüşmeleri başlıyor.</div>
                <a href="https://twitter.com/FabrizioRomano" class="tweet-link">Tweet'e Git →</a>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Veriyi İncele: Yamal", key="yamal_btn"): st.toast("Veri Sayfası Hazırlanıyor...")

        # Gazete Örneği
        st.markdown(f"""
            <div class="news-box gazete-box">
                <div class="news-header">📰 Marca / İspanya</div>
                <div>Real Madrid'de Arda Güler etkisi: Antrenman verileri son 1 ayın en yüksek seviyesinde.</div>
                <a href="https://www.marca.com" style="color:#dc3545; font-weight:600; text-decoration:none;">Habere Git →</a>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("🔥 Trendler")
        st.write("**#Transfer** • **#OptaPoints**")

# --- 3. STUDIO (4 OYUNCU) ---
with tab_studio:
    st.markdown('<div class="studio-card">CREATOR STUDIO</div>', unsafe_allow_html=True)
    
    names = st.session_state.players_df['Name'].tolist()
    c = st.columns(4)
    p_sel = [c[i].selectbox(f"Oyuncu {i+1}", names, index=i) for i in range(4)]
    
    # Kıyaslama Tablosu (Sade ve Görsel Odaklı)
    metrics = {"Haftalık Puan": "Perf", "Gol (90')": "Gls", "Asist (90')": "Ast", "xG": "xG", "Pas %": "Pass"}
    comp_df = pd.DataFrame({"Metrik": metrics.keys()})
    
    for p in p_sel:
        row = st.session_state.players_df[st.session_state.players_df['Name'] == p].iloc[0]
        comp_df[p] = [row[metrics[m]] for m in metrics]
    
    st.table(comp_df)
    st.caption("Not: Oyuncu görselleri profil sayfaları tamamlandığında buraya eklenecektir.")
