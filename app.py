import streamlit as st
import pandas as pd
import random

# --- UI & FONT ---
st.markdown("""
    <style>
    .news-capsule {
        background: #ffffff; border: 1px solid #f0f2f5; border-radius: 18px;
        padding: 18px; min-width: 300px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    .dva-badge { background: #00d084; color: white; padding: 2px 8px; border-radius: 6px; font-size: 10px; font-weight: 800; }
    .source-tr { background: #fee2e2; color: #dc2626; padding: 2px 8px; border-radius: 6px; font-size: 10px; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# --- HABER HAVUZU (OTOMATİK SİSTEM) ---
tr_news = [
    {"src": "Yağız Sabuncuoğlu", "text": "ÖZEL: Fenerbahçe, En-Nesyri için son teklifini yaptı. Beklemede.", "link": "https://twitter.com/yagosabuncuoglu"},
    {"src": "Ertan Süzgün", "text": "Beşiktaş'ta transfer hareketliliği: Kanat oyuncusu için temaslar sıklaştı.", "link": "https://twitter.com/ertansuzgun"},
    {"src": "Tribun Dergi", "text": "Galatasaray'ın yeni transferi İstanbul'a iniş yaptı.", "link": "https://twitter.com/tribundergi"}
]

dva_insights = [
    {"src": "DVA SMART", "text": "Arda Güler, Real Madrid idmanında %92 pas isabetiyle liderliği aldı!", "link": "#"},
    {"src": "DVA SMART", "text": "ANALİZ: Süper Lig'in 'Gözden Kaçan' en iyi 3 stoperi listelendi.", "link": "#"}
]

# --- 1. GLOBAL & YEREL AKIŞ ---
st.subheader("🌐 Global & Yerel Veri Akışı")
h_cols = st.columns(3)

# Karışık Akış Oluşturma (En az 1 DVA haberi garantili)
current_news = random.sample(tr_news, 2) + [random.choice(dva_insights)]
random.shuffle(current_news)

for i, n in enumerate(current_news):
    is_dva = "DVA" in n['src']
    badge = '<span class="dva-badge">DVA INSIGHT</span>' if is_dva else f'<span class="source-tr">TR / {n["src"]}</span>'
    
    with h_cols[i]:
        st.markdown(f"""
            <div class="news-capsule">
                {badge}
                <p style="font-weight: 600; font-size: 14px; margin-top: 10px;">{n['text']}</p>
                <a href="{n['link']}" target="_blank" style="font-size: 12px; color: #6366f1; text-decoration: none;">Detaylar →</a>
            </div>
        """, unsafe_allow_html=True)

# --- 2. SOSYAL MEDYA KARTI (1080x1080 HAZIRLIK) ---
st.write("---")
st.subheader("🎨 Sosyal Medya Kartı (1080x1080)")
col_p, col_btn = st.columns([3, 1])

with col_p:
    st.info("Kıyasladığın 4 oyuncuyu 'Instagram/Twitter' formatında tek tıkla indir.")
with col_btn:
    if st.button("🖼️ KART OLUŞTUR"):
        st.success("Tasarım Motoru: 1080x1080 PNG Hazırlanıyor...")
        # Burada tasarımın şık bir önizlemesi yer alacak
