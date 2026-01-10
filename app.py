import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- TASARIM VE FONT AYARLARI ---
st.set_page_config(page_title="DVA Pro: Sportbase & Opta Edition", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stat-box { background-color: #f8f9fa; border-radius: 8px; padding: 10px; border-left: 4px solid #007bff; }
    .opta-score { font-family: 'Roboto Mono', monospace; color: #00d084; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- GENİŞLETİLMİŞ VERİ SETİ (OPTA & SPORTBASE MANTIĞI) ---
if 'players_df' not in st.session_state:
    data = [
        {"Name": "E. Haaland", "Team": "Man City", "Pos": "FW", "Price": 180, "Opta_Points": 88.5, "Gls_90": 1.12, "Ast_90": 0.15, "xG_90": 0.95, "SHT_90": 3.8, "Pass_Acc": 78, "Health": "Stable"},
        {"Name": "K. De Bruyne", "Team": "Man City", "Pos": "MF", "Price": 90, "Opta_Points": 91.2, "Gls_90": 0.25, "Ast_90": 0.88, "xG_90": 0.22, "SHT_90": 2.1, "Pass_Acc": 84, "Health": "Risk"},
        {"Name": "W. Saliba", "Team": "Arsenal", "Pos": "DF", "Price": 80, "Opta_Points": 85.0, "Gls_90": 0.05, "Ast_90": 0.02, "xG_90": 0.04, "SHT_90": 0.4, "Pass_Acc": 92, "Health": "Stable"},
        {"Name": "Saka", "Team": "Arsenal", "Pos": "FW", "Price": 130, "Opta_Points": 87.8, "Gls_90": 0.45, "Ast_90": 0.35, "xG_90": 0.38, "SHT_90": 2.5, "Pass_Acc": 81, "Health": "Stable"},
        {"Name": "Rodri", "Team": "Man City", "Pos": "MF", "Price": 110, "Opta_Points": 94.1, "Gls_90": 0.18, "Ast_90": 0.22, "xG_90": 0.15, "SHT_90": 1.5, "Pass_Acc": 95, "Health": "Stable"}
    ]
    st.session_state.players_df = pd.DataFrame(data)

# --- NAVİGASYON ---
page = st.sidebar.radio("📊 DVA PRO HUB", ["🏠 Ana Terminal", "🏟️ Canlı Skorlar (Maçkolik)", "⚔️ Oyuncu Karşılaştırma", "🔐 Veri Merkezi"])

# --- 1. ANA TERMİNAL (PROFİLLER & OPTA) ---
if page == "🏠 Ana Terminal":
    st.title("⚽ Pro Analytics Terminal")
    search = st.selectbox("🔍 Oyuncu veya Takım Ara...", [""] + st.session_state.players_df['Name'].tolist())
    
    if search:
        p = st.session_state.players_df[st.session_state.players_df['Name'] == search].iloc[0]
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            st.header(p['Name'])
            st.write(f"**Takım:** {p['Team']} | **Mevki:** {p['Pos']}")
            st.metric("Piyasa Değeri", f"€{p['Price']}M")
        
        with col2:
            st.subheader("Opta Performance")
            st.markdown(f"<div class='opta-score' style='font-size:40px;'>{p['Opta_Points']}</div>", unsafe_allow_html=True)
            st.caption("Son 5 maç performansı baz alınmıştır.")
            
        with col3:
            st.subheader("Maç Geçmişi & İstatistik")
            match_data = pd.DataFrame({
                "Maç": ["v Liverpool", "v Real Madrid", "v Chelsea"],
                "Süre": ["90'", "82'", "90'"],
                "Puan": [7.8, 8.5, 6.9],
                "Aksiyon": ["1 Gol", "2 Asist", "Sarı Kart"]
            })
            st.table(match_data)

# --- 2. CANLI SKORLAR (MAÇKOLİK TARZI) ---
elif page == "🏟️ Canlı Skorlar (Maçkolik)":
    st.title("🏟️ Canlı Maç Merkezi")
    st.info("Opta Points verileri maç anında canlı güncellenmektedir.")
    
    matches = [
        {"Home": "Man City", "Away": "Arsenal", "Score": "2 - 1", "Min": "72'", "Status": "Live"},
        {"Home": "Real Madrid", "Away": "Barcelona", "Score": "0 - 0", "Min": "15'", "Status": "Live"}
    ]
    
    for m in matches:
        with st.container():
            c1, c2, c3 = st.columns([2, 1, 2])
            c1.button(m['Home'], use_container_width=True)
            c2.markdown(f"<h3 style='text-align:center;'>{m['Score']}</h3><p style='text-align:center; color:red;'>{m['Min']}</p>", unsafe_allow_html=True)
            c3.button(m['Away'], use_container_width=True)
            st.divider()

# --- 3. OYUNCU KARŞILAŞTIRMA (SPORTBASE TARZI) ---
elif page == "⚔️ Oyuncu Karşılaştırma":
    st.title("⚔️ Data Comparison (Per 90)")
    
    names = st.session_state.players_df['Name'].tolist()
    c1, c2 = st.columns(2)
    p1 = c1.selectbox("1. Oyuncu", names, index=0)
    p2 = c2.selectbox("2. Oyuncu", names, index=1)
    
    d1 = st.session_state.players_df[st.session_state.players_df['Name'] == p1].iloc[0]
    d2 = st.session_state.players_df[st.session_state.players_df['Name'] == p2].iloc[0]
    
    # Radar Grafik (Görsel)
    fig = go.Figure()
    cats = ['Gls_90', 'Ast_90', 'xG_90', 'SHT_90', 'Pass_Acc']
    # Normalize ederek çizim (Yüzde bazlı göstermek için)
    fig.add_trace(go.Scatterpolar(r=[d1[c] if c != 'Pass_Acc' else d1[c]/10 for c in cats], theta=cats, fill='toself', name=p1))
    fig.add_trace(go.Scatterpolar(r=[d2[c] if c != 'Pass_Acc' else d2[c]/10 for c in cats], theta=cats, fill='toself', name=p2))
    st.plotly_chart(fig, use_container_width=True)
    
    # Sportbase Tarzı Tablo (Verisel)
    st.subheader("Detaylı Karşılaştırma Matrisi")
    comparison_table = pd.DataFrame({
        "Metrik": ["Opta Puanı", "Gol (90 dk)", "Asist (90 dk)", "xG (Beklenen Gol)", "Şut (90 dk)", "Pas İsabeti %"],
        p1: [d1['Opta_Points'], d1['Gls_90'], d1['Ast_90'], d1['xG_90'], d1['SHT_90'], d1['Pass_Acc']],
        p2: [d2['Opta_Points'], d2['Gls_90'], d2['Ast_90'], d2['xG_90'], d2['SHT_90'], d2['Pass_Acc']]
    })
    st.table(comparison_table)

# --- 4. VERİ MERKEZİ ---
elif page == "🔐 Veri Merkezi":
    st.title("🔐 Admin Terminal")
    with st.expander("Oyuncu Verilerini Güncelle"):
        target = st.selectbox("Oyuncu", st.session_state.players_df['Name'])
        new_opta = st.number_input("Yeni Opta Puanı", 0.0, 100.0, 80.0)
        if st.button("Veriyi Sisteme Gönder"):
            st.session_state.players_df.loc[st.session_state.players_df['Name'] == target, 'Opta_Points'] = new_opta
            st.success("Tüm terminaller güncellendi!")
