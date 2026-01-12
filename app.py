import streamlit as st
import pandas as pd
import plotly.express as px

# --- PIXEL PERFECT UI SETUP ---
st.set_page_config(page_title="DVA Pro Terminal", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus+Jakarta+Sans', sans-serif; background: #f4f7fb; }

    /* Oyuncu Header Kartı - image_e8c0c9.jpg tarzı */
    .player-profile-header {
        background: linear-gradient(135deg, #101828 0%, #070a11 100%);
        color: white; padding: 40px; border-radius: 30px; margin-bottom: 25px;
        position: relative; overflow: hidden;
    }
    .dva-value-tag {
        position: absolute; right: 40px; top: 40px;
        background: rgba(0, 208, 132, 0.1); border: 1px solid #00d084;
        color: #00d084; padding: 15px 25px; border-radius: 20px; font-weight: 800;
    }
    
    /* Analitik Kartlar - image_e8c0aa.jpg tarzı */
    .metric-card-pro {
        background: white; border-radius: 24px; padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.02); border: 1px solid #f0f2f5;
        height: 100%;
    }
    
    /* İndir/Paylaş Butonu (Floating Style) */
    .export-btn {
        background: #6366f1; color: white; padding: 15px 30px;
        border-radius: 15px; font-weight: 700; text-align: center;
        cursor: pointer; margin-top: 20px; border: none; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- OYUNCU VERİSİ (ANALİTİK ODAKLI) ---
player = {
    "name": "Arda Güler", "club": "Real Madrid", "age": 20, 
    "tm_value": "€45M", "dva_value": "€68.4M", # TM vs DVA farkı
    "metrics": {"Teknik": 94, "Vizyon": 91, "Fizik": 72, "Pres": 84, "Şut": 88}
}

# --- 1. PLAYER HEADER (Piyasa Değeri Farkı) ---
st.markdown(f"""
    <div class="player-profile-header">
        <div class="dva-value-tag">DVA ANALYTIC VALUE: {player['dva_value']}</div>
        <small style="color: #6366f1; font-weight: 800;">{player['club'].upper()}</small>
        <h1 style="margin: 10px 0; font-size: 48px;">{player['name']}</h1>
        <p style="opacity: 0.7;">Transfermarkt Değeri: {player['tm_value']} | <span style="color:#00d084;">Analitik Potansiyel: +%52</span></p>
    </div>
""", unsafe_allow_html=True)

# --- 2. ANALİTİK PANEL (3'LÜ YERLEŞİM) ---
col_stats, col_chart, col_action = st.columns([1, 1, 1])

with col_stats:
    st.markdown('<div class="metric-card-pro"><h4>Gelişim Karnesi</h4>', unsafe_allow_html=True)
    for m, v in player['metrics'].items():
        st.write(f"**{m}**")
        st.progress(v / 100)
    st.markdown('</div>', unsafe_allow_html=True)

with col_chart:
    st.markdown('<div class="metric-card-pro"><h4>Piyasa Değeri Projeksiyonu</h4>', unsafe_allow_html=True)
    # image_e8c0c9'daki grafik tarzı
    chart_data = pd.DataFrame({
        "Ay": ["Eyl", "Eki", "Kas", "Ara", "Oca"],
        "Değer": [45, 48, 55, 62, 68]
    })
    fig = px.line(chart_data, x="Ay", y="Değer", markers=True, color_discrete_sequence=['#6366f1'])
    fig.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_action:
    st.markdown('<div class="metric-card-pro"><h4>İşlem Merkezi</h4>', unsafe_allow_html=True)
    st.write("Bu oyuncunun analitik verilerini kullanarak sosyal medya kartı hazırla.")
    
    # KART OLUŞTURMA BUTONU BURADA
    if st.button("📸 SOSYAL MEDYA KARTI (1080x1080)", use_container_width=True):
        st.balloons()
        st.success("Tasarım image_e8c0c9 standartlarında hazırlandı!")
        st.image("https://via.placeholder.com/1080x1080.png?text=DVA+Arda+Guler+Analytic+Card", caption="Görseli İndir")
    
    st.markdown('<button class="export-btn">PDF RAPOR İNDİR</button>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
