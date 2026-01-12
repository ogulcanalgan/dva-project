import streamlit as st
import pandas as pd
import plotly.express as px

# --- MOBILE-FIRST UI CONFIG ---
st.set_page_config(page_title="DVA Pulse", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #ffffff; }
    
    /* Üst Borsa Şeridi (Ticker) */
    .ticker-wrap { background: #101828; color: #00d084; padding: 10px; overflow: hidden; white-space: nowrap; font-weight: bold; font-size: 14px; }
    
    /* Mobil Uyumlu Haber Kartları */
    .news-card { border-left: 4px solid #007bff; padding: 10px; background: #f8f9fa; border-radius: 5px; margin-bottom: 10px; font-size: 13px; }
    .news-source { color: #6c757d; font-size: 11px; text-transform: uppercase; }
    
    /* Creator Studio Butonu */
    .creator-btn { background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%); color: white; padding: 20px; border-radius: 15px; text-align: center; font-weight: 800; cursor: pointer; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. ÜST ŞERİT (TICKER) ---
st.markdown("""
    <div class="ticker-wrap">
        🔥 Lamine Yamal (Barça) Performance +12% ↑ | ⚡ Arda Güler Hype +45% ↑ | 📉 K. De Bruyne Injury Risk Alert | ⚽ Haaland Opta Point: 98.2
    </div>
    """, unsafe_allow_html=True)

# --- 2. ANA ARAMA (AI SIMILARITY FOCUS) ---
st.title("📡 DVA Pulse")
search_query = st.text_input("", placeholder="🔍 Oyuncu ara veya 'Rodri'nin benzerini bul' yaz...")

# --- 3. MERKEZİ YERLEŞİM ---
col_main, col_side = st.columns([2, 1])

with col_main:
    # Creator Studio Hızlı Erişim
    st.markdown('<div class="creator-btn">🎨 CREATOR STUDIO: 4 OYUNCU KIYASLA (ÜCRETSİZ)</div>', unsafe_allow_html=True)
    
    # Haber Akışı (Referanslı)
    st.subheader("📰 Son Veri Haberleri")
    news_data = [
        {"text": "Fabrizio Romano: Manchester City, Haaland'ın sözleşmesi için yeni verileri inceliyor.", "src": "Twitter / @FabrizioRomano"},
        {"text": "L'Equipe: Mbappe'nin sprint hızı Real Madrid'deki ilk maçında %5 düştü.", "src": "L'Equipe / France"},
        {"text": "DVA Insight: Kerem Aktürkoğlu son 3 maçta xG değerini 2.4 katına çıkardı.", "src": "DVA Smart Engine"}
    ]
    for n in news_data:
        st.markdown(f"""
            <div class="news-card">
                <div class="news-source">{n['src']}</div>
                <div>{n['text']}</div>
            </div>
        """, unsafe_allow_html=True)

with col_side:
    # Haftalık Performans Liderleri (Minimalist)
    st.subheader("🔝 Liderler")
    st.session_state.players_df = pd.DataFrame([
        {"Name": "Yamal", "P": 94}, {"Name": "Rodri", "P": 92}, {"Name": "Saka", "P": 89}
    ])
    for _, r in st.session_state.players_df.iterrows():
        st.write(f"**{r['Name']}** • {r['P']}")

# --- 4. 4'LÜ KIYASLAMA ALANI (TASLAK) ---
if st.checkbox("4'lü Karşılaştırmayı Başlat"):
    st.info("Burada 4 oyuncu seçimi ve şık Creator Studio tasarımı yer alacak.")
    # (Buraya daha sonra 4'lü seçim kutuları ve tablo yerleşimi gelecek)
