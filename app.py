import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Sayfa Ayarları
st.set_page_config(page_title="DVA: Professional Analyst Platform", layout="wide")

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

# --- SOL MENÜ (NAVİGASYON) ---
st.sidebar.title("⚽ DVA Navigation")
page = st.sidebar.selectbox("Gitmek İstediğiniz Bölüm", 
    ["🏠 Ana Sayfa (Gündem)", "👤 Oyuncu Profilleri", "📈 Analiz Terminali (V2)", "⚔️ Arena (Kıyaslama)", "🔐 Admin Panel"])

# --- 1. ANA SAYFA (GÜNDEM) ---
if page == "🏠 Ana Sayfa (Gündem)":
    st.title("🔥 Piyasa Gündemi")
    st.subheader("Günün En Popüler Yatırımları (Trending)")
    
    # Hype'a göre sırala ve ilk 3'ü getir
    trending_df = st.session_state.players_df.sort_values(by="Hype", ascending=False).head(3)
    cols = st.columns(3)
    
    for i, (_, row) in enumerate(trending_df.iterrows()):
        with cols[i]:
            st.success(f"Trending #{i+1}")
            st.metric(row['Name'], f"€{row['Price']}M", f"Hype: {row['Hype']}")
            st.progress(row['Hype']/100)

    st.divider()
    st.subheader("Haftalık Performans Liderleri")
    st.dataframe(st.session_state.players_df[['Name', 'Pos', 'GW_Points', 'Price']].sort_values(by="GW_Points", ascending=False))

# --- 2. OYUNCU PROFİLLERİ (Hype Meter Burada) ---
elif page == "👤 Oyuncu Profilleri":
    st.title("👤 Oyuncu Detay Analizi")
    target = st.selectbox("Oyuncu Seçin", st.session_state.players_df['Name'])
    p_data = st.session_state.players_df[st.session_state.players_df['Name'] == target].iloc[0]
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.header(p_data['Name'])
        st.metric("Piyasa Değeri", f"€{p_data['Price']}M")
        st.write(f"**Mevki:** {p_data['Pos']}")
        st.write(f"**Sağlık Durumu:** {p_data['Health']}")
    
    with col2:
        st.subheader("Dinamik Hype Meter")
        # Sadece aranan oyuncu için Hype Meter
        fig_hype = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = p_data['Hype'],
            title = {'text': "Popülerlik Endeksi"},
            gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}}
        ))
        st.plotly_chart(fig_hype, use_container_width=True)

# --- 3. ANALİZ TERMİNALİ (V2 ÖZELLİKLERİ) ---
elif page == "📈 Analiz Terminali (V2)":
    st.title("📈 Profesyonel Analiz Araçları")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Değer vs Yetenek Dengesi")
        fig_scatter = px.scatter(st.session_state.players_df, x="Skill", y="Price", size="Hype", color="Pos", hover_name="Name", template="plotly_dark")
        st.plotly_chart(fig_scatter)
    
    with col2:
        st.subheader("Fiziksel Güç Dağılımı")
        fig_bar = px.bar(st.session_state.players_df, x="Name", y="Physical", color="Name", template="plotly_dark")
        st.plotly_chart(fig_bar)

# --- 4. ARENA ---
elif page == "⚔️ Arena (Kıyaslama)":
    st.title("⚔️ Kıyaslama Arenası")
    p1 = st.selectbox("1. Oyuncu", st.session_state.players_df['Name'], key="a1")
    p2 = st.selectbox("2. Oyuncu", st.session_state.players_df['Name'], key="a2", index=1)
    
    d1 = st.session_state.players_df[st.session_state.players_df['Name'] == p1].iloc[0]
    d2 = st.session_state.players_df[st.session_state.players_df['Name'] == p2].iloc[0]
    
    fig = go.Figure()
    categories = ['Skill', 'Physical', 'Hype', 'GW_Points']
    fig.add_trace(go.Scatterpolar(r=[d1['Skill'], d1['Physical'], d1['Hype'], d1['GW_Points']*5], fill='toself', name=p1))
    fig.add_trace(go.Scatterpolar(r=[d2['Skill'], d2['Physical'], d2['Hype'], d2['GW_Points']*5], fill='toself', name=p2))
    st.plotly_chart(fig)

# --- 5. ADMIN PANEL ---
elif page == "🔐 Admin Panel":
    st.title("🔐 Merkezi Veri Yönetimi")
    target_player = st.selectbox("Güncellenecek Oyuncu", st.session_state.players_df['Name'])
    new_hype = st.slider("Hype Ayarla", 0, 100, 50)
    new_pts = st.number_input("Haftalık Puan", 0, 20, 5)
    
    if st.button("Verileri Güncelle"):
        st.session_state.players_df.loc[st.session_state.players_df['Name'] == target_player, 'Hype'] = new_hype
        st.session_state.players_df.loc[st.session_state.players_df['Name'] == target_player, 'GW_Points'] = new_pts
        st.success("Tüm sistem güncellendi!")
