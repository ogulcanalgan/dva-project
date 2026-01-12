import streamlit as st
import pandas as pd
import random

# --- UI CONFIG ---
st.set_page_config(page_title="DVA Pulse", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
    
    /* Haber Kapsülleri */
    .news-capsule {
        background: #ffffff; border: 1px solid #f0f2f5; border-radius: 20px;
        padding: 20px; min-width: 320px; box-shadow: 0 10px 30px rgba(0,0,0,0.02);
    }
    
    /* Sosyal Medya Kart Tasarımı (Preview) */
    .social-card-preview {
        background: linear-gradient(135deg, #101828 0%, #1f2937 100%);
        color: white; padding: 30px; border-radius: 25px; border: 2px solid #6366f1;
        text-align: center; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. OTOMATİK HABER MOTORU (SİMÜLASYON) ---
# Burası ileride API'ye bağlanacak ana kaynak listesi
sources = [
    {"name": "Fabrizio Romano", "handle": "@FabrizioRomano", "type": "Twitter"},
    {"name": "Marca", "handle": "Spain", "type": "News"},
    {"name": "The Athletic", "handle": "UK", "type": "News"},
    {"name": "DVA AI", "handle": "Smart Engine", "type": "Internal"}
]

def get_latest_news():
    # Otomatik güncelleme hissi için rastgele haber seçimi
    news_pool = [
        "Lamine Yamal'ın DVA puanı son 24 saatte %15 arttı.",
        "Arda Güler antrenman verilerinde takımın en iyisi seçildi.",
        "Rodri pas isabetinde Premier Lig rekoruna yaklaşıyor.",
        "Real Madrid, genç oyuncu gelişiminde DVA metriklerini kullanıyor."
    ]
    return random.choice(news_pool), random.choice(sources)

# --- 2. ANA EKRAN ---
st.title("📡 DVA Pulse")
st.markdown("---")

# Yatay Haber Akışı (image_e844c4.png yapısının geliştirilmiş hali)
st.subheader("🌐 Global Veri Akışı")
h_cols = st.columns(3)
for i in range(3):
    text, src = get_latest_news()
    with h_cols[i]:
        st.markdown(f"""
            <div class="news-capsule">
                <small style="color: #6366f1; font-weight: 800;">{src['type']} / {src['handle']}</small>
                <p style="font-weight: 700; font-size: 15px; margin: 10px 0;">{text}</p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <a href="#" style="font-size: 12px; color: #888; text-decoration: none;">Kaynağa Git →</a>
                    <span style="font-size: 10px; background: #f1f3f5; padding: 2px 6px; border-radius: 4px;">Şimdi</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.write("") # Boşluk

# --- 3. CREATOR STUDIO (GÖRSEL ODAKLI) ---
st.markdown("### 🎨 Studio: Sosyal Medya Kartı Oluştur")
sel_players = st.multiselect("Oyuncuları Seç", st.session_state.players_df['Name'].tolist(), default=["Lamine Yamal", "Arda Güler"])

if sel_players:
    # Karşılaştırma Tablosu (image_e844c4.png'deki gibi)
    # ... (Önceki tablo kodları burada aktif kalacak)
    
    st.markdown("""<div class="social-card-preview">
        <h2 style="color: #00d084;">DVA ELITE PERFORMANCE</h2>
        <p>Haftalık Karşılaştırma Raporu</p>
        <div style="display: flex; justify-content: space-around; margin-top: 20px;">
    """ + "".join([f"<div><b>{p}</b><br><small>Opta: 90+</small></div>" for p in sel_players]) + """
        </div>
    </div>""", unsafe_allow_html=True)
    
    if st.button("📸 PNG OLARAK İNDİR"):
        st.success("Görsel hazırlanıyor... (Sosyal medya boyutlarında 1080x1080)")
