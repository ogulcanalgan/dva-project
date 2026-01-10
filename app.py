import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PREMIUM TEMA AYARLARI ---
st.set_page_config(page_title="DVA Terminal", layout="wide")

# Midas tarzı modern font ve temiz arayüz için CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        color: #f8f9fa;
    }
    .main { background-color: #0c0e12; }
    div[data-testid="stMetricValue"] { font-size: 28px; font-weight: 700; color: #00d084; }
    .stButton>button { border-radius: 8px; border: none; background-color: #1e222d; color: white; width: 100%; transition: 0.3s; }
    .stButton>button:hover { background-color: #00d084; color: black; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETİ ---
if 'players_df' not in st.session_state:
    data = [
        {"Name": "E. Haaland", "Pos": "FW", "Price": 65, "Hype": 95, "Skill": 91, "Health": "Stable", "GW_Points": 12, "Physical": 95},
        {"Name": "K. De Bruyne", "Pos": "MF", "Price": 45, "Hype": 80, "Skill": 90, "Health": "Risk", "GW_Points": 8, "Physical": 82},
        {"Name": "W. Saliba", "Pos": "DF", "Price": 35, "Hype": 70, "Skill": 88, "Health": "Stable", "GW_Points": 6, "Physical": 90},
        {"Name": "Saka", "Pos": "FW", "Price": 50, "Hype": 88, "Skill": 89, "Health": "Stable", "GW_Points": 10, "Physical": 84},
        {"Name": "Rodri", "Pos": "MF", "Price": 55, "Hype": 92, "Skill": 92, "Health": "Stable", "GW_Points": 7, "Physical": 88}
    ]
    st.session_state.players_df = pd.DataFrame(data)

if 'compare_list' not in st.session_state:
    st.session_state.compare_list = []

# --- NAVİGASYON ---
with st.sidebar:
    st.title("📊 DVA")
    page = st.radio("Menü", ["🏠 Terminal", "📈 Pazar Analizi", "⚔️ Oyuncu Kıyaslama", "🔐 Yönetim"])

# --- 1. ANA SAYFA & GLOBAL ARAMA ---
if page == "🏠 Terminal":
    st.title("📡 Canlı Borsa Terminali")
    
    # Midas Tarzı Arama
    search_query = st.selectbox("🔍 Oyuncu veya Takım Ara...", [""] + st.session_state.players_df['Name'].tolist())
    
    if search_query:
        p_data = st.session_state.players_df[st.session_state.players_df['Name'] == search_query].iloc[0]
        st.markdown(f"## {p_data['Name']} <span style='font-size:15px; color:gray;'>{p_data['Pos']}</span>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1, 1, 2])
        c1.metric("Piyasa Değeri", f"€{p_data['Price']}M")
        c2.metric("Performans", f"{p_data['GW_Points']} Puan")
        
        with c3:
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number", value = p_data['Hype'],
                gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#00d084"}},
                domain = {'x': [0, 1], 'y': [0, 1]}
            ))
            fig_gauge.update_layout(height=200, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        if st.button(f"⚔️ {p_data['Name']} Kıyaslamaya Ekle"):
            if p_data['Name'] not in st.session_state.compare_list:
                st.session_state.compare_list.append(p_data['Name'])
                st.success("Listeye eklendi. Kıyaslama sayfasına gidiniz.")

    st.divider()
    st.subheader("🔥 Popüler Yatırımlar")
    trending = st.session_state.players_df.sort_values(by="Hype", ascending=False).head(3)
    t_cols = st.columns(3)
    for i, (_, r) in enumerate(trending.iterrows()):
        with t_cols[i]:
            st.markdown(f"<div style='background-color:#1e222d; padding:20px; border-radius:15px;'>"
                        f"<h4 style='margin:0;'>{r['Name']}</h4>"
                        f"<p style='color:#00d084; font-weight:bold;'>€{r['Price']}M</p>"
                        f"</div>", unsafe_allow_html=True)

# --- 2. PAZAR ANALİZİ ---
elif page == "📈 Pazar Analizi":
    st.title("📉 Piyasa Dinamikleri")
    st.info("Analiz Terminali: Fan kullanıcılar için değer/yetenek korelasyonu.")
    fig_scatter = px.scatter(st.session_state.players_df, x="Skill", y="Price", size="Hype", color="Pos",
                             template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_scatter.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- 3. OYUNCU KIYASLAMA ---
elif page == "⚔️ Oyuncu Kıyaslama":
    st.title("⚔️ Oyuncu Kıyaslama")
    
    # Hata korumalı seçimler
    all_names = st.session_state.players_df['Name'].tolist()
    s1 = st.session_state.compare_list[0] if len(st.session_state.compare_list) > 0 else all_names[0]
    s2 = st.session_state.compare_list[1] if len(st.session_state.compare_list) > 1 else all_names[1]

    col1, col2 = st.columns(2)
    p1 = col1.selectbox("Oyuncu 1", all_names, index=all_names.index(s1))
    p2 = col2.selectbox("Oyuncu 2", all_names, index=all_names.index(s2))
    
    d1 = st.session_state.players_df[st.session_state.players_df['Name'] == p1].iloc[0]
    d2 = st.session_state.players_df[st.session_state.players_df['Name'] == p2].iloc[0]
    
    fig_radar = go.Figure()
    cats = ['Skill', 'Physical', 'Hype', 'GW_Points']
    # Puanı normalize ediyoruz (Hata çözümü)
    fig_radar.add_trace(go.Scatterpolar(r=[d1['Skill'], d1['Physical'], d1['Hype'], d1['GW_Points']*5], fill='toself', name=p1, line_color="#00d084"))
    fig_radar.add_trace(go.Scatterpolar(r=[d2['Skill'], d2['Physical'], d2['Hype'], d2['GW_Points']*5], fill='toself', name=p2, line_color="#0070f3"))
    
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100])), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_radar, use_container_width=True)

# --- 4. YÖNETİM PANELİ ---
elif page == "🔐 Yönetim":
    st.title("🔐 Veri Girişi")
    with st.form("update_form"):
        target = st.selectbox("Oyuncu", st.session_state.players_df['Name'])
        new_price = st.number_input("Yeni Değer (€M)", 0, 200, 50)
        new_pts = st.slider("Haftalık Puan", 0, 20, 5)
        if st.form_submit_button("Sistemi Güncelle"):
            st.session_state.players_df.loc[st.session_state.players_df['Name'] == target, ['Price', 'GW_Points']] = [new_price, new_pts]
            st.success("Veri başarıyla işlendi!")
