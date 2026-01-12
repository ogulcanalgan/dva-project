import streamlit as st
import pandas as pd
import random

# --- UI & X-BRANDING STYLE ---
st.markdown("""
    <style>
    .news-capsule {
        background: #ffffff; border: 1px solid #f0f2f5; border-radius: 18px;
        padding: 18px; min-width: 310px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    .x-indicator { color: #000000; font-weight: 800; font-size: 14px; }
    .nick-handle { color: #65676b; font-size: 12px; margin-left: 4px; }
    .hype-card {
        background: #f8f9fa; border-radius: 15px; padding: 15px; margin-bottom: 10px;
        border-left: 4px solid #6366f1;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GENİŞLETİLMİŞ HABER HAVUZU ---
tr_news_v15 = [
    {"src": "Burhan Can Terzi", "handle": "@burhancanterzi", "type": "X", "text": "Galatasaray'da sıcak saatler: Orta saha transferi için liste daraldı."},
    {"src": "Emre Kaplan", "handle": "@emrekaplan61", "type": "X", "text": "Florya'dan son bilgiler: Takımdaki moral seviyesi en üst düzeyde."},
    {"src": "Anadolu Ajansı / Spor", "handle": "@aaspor", "type": "News", "text": "Kayserispor ve Sivasspor'da hafta sonu hazırlıkları tamamlandı."},
    {"src": "Yunus Emre Sel", "handle": "@yunusemresel", "type": "X", "text": "Trabzonspor'da golcü arayışlarında yeni rota Kuzey Avrupa."}
]

# --- 1. HABER AKIŞI (X & NICK ENTEGRASYONU) ---
st.subheader("🌐 Global & Yerel Veri Akışı")
h_cols = st.columns(3)
selected_news = random.sample(tr_news_v15, 3)

for i, n in enumerate(selected_news):
    indicator = f'<span class="x-indicator">𝕏</span><span class="nick-handle">{n["handle"]}</span>' if n['type'] == "X" else f'<span class="source-tr">📰 {n["src"]}</span>'
    with h_cols[i]:
        st.markdown(f"""
            <div class="news-capsule">
                {indicator}
                <p style="font-weight: 600; font-size: 14px; margin-top: 10px;">{n['text']}</p>
                <a href="#" style="font-size: 12px; color: #6366f1; text-decoration: none;">Kaynağa Git →</a>
            </div>
        """, unsafe_allow_html=True)

# --- 2. TREND & SÖYLENTİ MERKEZİ (YENİ BÖLÜM) ---
st.write("---")
st.subheader("🔥 Trend & Söylenti Merkezi")
st.info("Piyasada şu an en çok konuşulan ve verileriyle dikkat çeken isimler:")

hype_list = [
    {"name": "Semih Kılıçsoy", "reason": "📈 Performans: Son 3 maçta 4 gol katkısı.", "status": "Söylenti: PL kulüplerinin takibinde."},
    {"name": "Ferdi Kadıoğlu", "reason": "💎 Değer: Opta savunma verilerinde lig lideri.", "status": "Duyum: Dortmund ilgisi ciddileşiyor."},
    {"name": "Mauro Icardi", "reason": "👑 İstatistik: Ceza sahası içi verimlilik %89.", "status": "Gündem: Rekor tazeleme peşinde."}
]

col_h1, col_h2, col_h3 = st.columns(3)
h_cols_list = [col_h1, col_h2, col_h3]

for idx, item in enumerate(hype_list):
    with h_cols_list[idx]:
        st.markdown(f"""
            <div class="hype-card">
                <h4 style="margin:0;">{item['name']}</h4>
                <div style="font-size: 13px; margin-top: 5px;">{item['reason']}</div>
                <div style="font-size: 12px; color: #6366f1; font-weight: 700;">{item['status']}</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button(f"Profiline Git: {item['name']}", key=f"go_{idx}"):
            st.success(f"{item['name']} profiline gidiliyor. Kart oluşturma ve karşılaştırma içeride!")
