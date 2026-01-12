import streamlit as st
import pandas as pd
import time

# --- PROFESYONEL UI AYARLARI ---
st.set_page_config(page_title="DVA Pulse", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus+Jakarta+Sans', sans-serif; background: #fcfcfd; }
    
    /* Otomatik Kayan Haber Bandı */
    .news-slider {
        display: flex;
        overflow-x: auto;
        gap: 15px;
        padding: 10px 0;
        scrollbar-width: none; /* Firefox */
    }
    .news-slider::-webkit-scrollbar { display: none; } /* Chrome/Safari */
    
    .news-item {
        min-width: 300px;
        background: white;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #f0f2f5;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }
    
    .source-tag { font-size: 10px; font-weight: 800; text-transform: uppercase; padding: 4px 8px; border-radius: 6px; margin-bottom: 10px; display: inline-block; }
    .source-twitter { background: #e1f5fe; color: #03a9f4; }
    .source-news { background: #fff5f5; color: #e53e3e; }
    
    /* Tablo ve Karşılaştırma Tasarımı */
    .stTable { background: white; border-radius: 15px; overflow: hidden; border: 1px solid #f0f2f5; }
    .leader-star { color: #f59e0b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- HATASIZ VERİ SETİ (KİLİT NOKTA) ---
# Görsellerdeki hataları önlemek için tüm sütunları tanımlıyoruz
if 'players_df' not in st.session_state:
    data = [
        {"Name": "E. Haaland", "Team": "Man City", "Perf": 88, "Gls": 1.12, "Ast": 0.15, "xG": 0.95, "Pass": 78, "Price": "€180M"},
        {"Name": "Lamine Yamal", "Team": "Barcelona", "Perf": 95, "Gls": 0.35, "Ast": 0.55, "xG": 0.45, "Pass": 81, "Price": "€150M"},
        {"Name": "Rodri", "Team": "Man City", "Perf": 92, "Gls": 0.18, "Ast": 0.25, "xG": 0.12, "Pass": 94, "Price": "€130M"},
        {"Name": "Arda Güler", "Team": "Real Madrid", "Perf": 85, "Gls": 0.40, "Ast": 0.30, "xG": 0.38, "Pass": 89, "Price": "€45M"}
    ]
    st.session_state.players_df = pd.DataFrame(data)

# --- 1. SMART HEADER ---
st.title("📡 DVA Pulse")
st.text_input("", placeholder="🔍 Oyuncu, Gazeteci veya Transfer Ara...")

# --- 2. OTOMATİK HABER AKIŞI (Yatay Kaydırmalı) ---
st.subheader("🌐 Global Veri Akışı")
news_list = [
    {"src": "Twitter / @FabrizioRomano", "type": "twitter", "text": "Here we go! Yamal DVA puanı zirvede.", "link": "https://twitter.com/fabrizioromano"},
    {"src": "Marca / İspanya", "type": "news", "text": "Real Madrid, Arda'nın fiziksel verilerinden memnun.", "link": "https://marca.com"},
    {"src": "DVA Smart Engine", "type": "news", "text": "Rodri %94 pas isabetiyle Premier Lig lideri.", "link": "#"}
]

# HTML ile yatay kaydırma alanı
cols = st.columns(len(news_list))
for i, n in enumerate(news_list):
    with cols[i]:
        tag_class = "source-twitter" if n['type'] == "twitter" else "source-news"
        st.markdown(f"""
            <div class="news-item">
                <span class="source-tag {tag_class}">{n['src']}</span>
                <p style="font-size: 14px; color: #1a1c1e; font-weight: 600;">{n['text']}</p>
                <a href="{n['link']}" target="_blank" style="font-size: 12px; color: #6366f1; text-decoration: none;">Detaylara Git →</a>
            </div>
        """, unsafe_allow_html=True)

st.divider()

# --- 3. STUDIO (4 OYUNCU) ---
st.subheader("🎨 Studio")
names = st.session_state.players_df['Name'].tolist()
sel = st.multiselect("Kıyaslanacak Oyuncuları Seç (Maks 4)", names, default=names[:4])

if sel:
    # Metrikleri ve veriyi hazırla
    metrics = {"Performans": "Perf", "Gol (90')": "Gls", "Asist (90')": "Ast", "xG": "xG", "Pas %": "Pass"}
    comp_df = pd.DataFrame({"Metrik": metrics.keys()})
    
    for p in sel:
        row = st.session_state.players_df[st.session_state.players_df['Name'] == p].iloc[0]
        comp_df[p] = [row[metrics[m]] for m in metrics]
    
    # Yıldız Sistemi: Her satırın en büyüğünü bul ve işaretle
    def highlight_max(s):
        if s.name == "Metrik": return [''] * len(s)
        is_max = s == s.max()
        return ['color: #00d084; font-weight: 800' if v else '' for v in is_max]

    st.table(comp_df)
    st.info("💡 Yeşil rakamlar o kategorideki grup liderini gösterir.")
