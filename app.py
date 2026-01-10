import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- FERAH UI AYARLARI ---
st.set_page_config(page_title="DVA Terminal", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus+Jakarta+Sans', sans-serif; }
    .main { background-color: #fcfcfd; }
    .stMetric { background-color: white; padding: 15px; border-radius: 12px; border: 1px solid #eee; }
    .stButton>button { border-radius: 10px; height: 3em; background-color: #101828; color: white; }
    div[data-testid="stSidebar"] { background-color: #f8f9fa; border-right: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETİ (Kritik Hata Korumalı) ---
if 'players_df' not in st.session_state:
    data = [
        {"Name": "E. Haaland", "Pos": "FW", "Price": 65, "Hype": 95, "Skill": 91, "GW_Points": 12, "Physical": 95},
        {"Name": "K. De Bruyne", "Pos": "MF", "Price": 45, "Hype": 80, "Skill": 90, "GW_Points": 8, "Physical": 82},
        {"Name": "W. Saliba", "Pos": "DF", "Price": 35, "Hype": 70, "Skill": 88, "GW_Points": 6, "Physical": 90},
        {"Name": "Saka", "Pos": "FW", "Price": 50, "Hype": 88, "Skill": 89, "GW_Points": 10, "Physical": 84},
        {"Name": "Rodri", "Pos": "MF", "Price": 55, "Hype": 92, "Skill": 92, "GW_Points": 7, "Physical": 88}
    ]
    st.session_state.players_df = pd.DataFrame(data)

if 'compare_list' not in st.session_state:
    st.session_state.compare_list = []

# --- NAVİGASYON ---
page = st.sidebar.radio("MENÜ", ["🏠 Terminal", "📊 Pazar Analizi", "⚔️ Oyuncu Karşılaştırma", "🔐 Yönetim"])

# --- 1. TERMİNAL ---
if page == "🏠 Terminal":
    st.title("📡 DVA Data Terminal")
    
    # Merkezi Arama
    search_query = st.selectbox("🔍 Oyuncu veya Takım Ara...", [""] + st.session_state.players_df['Name'].tolist())
    
    if search_query:
        p = st.session_state.players_df[st.session_state.players_df['Name'] == search_query].iloc[0]
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            st.metric("Piyasa Değeri", f"€{p['Price']}M")
        with c2:
            st.metric("Haftalık Puan", f"{p['GW_Points']} pts")
        with c3:
            if st.button(f"⚔️ {p['Name']} Kıyaslamaya Ekle"):
                if p['Name'] not in st.session_state.compare_list:
                    st.session_state.compare_list.append(p['Name'])
                    st.toast("Arena'ya eklendi!")

    st.divider()
    st.subheader("🔥 Gündemdeki Oyuncular")
    t_cols = st.columns(3)
    trending = st.session_state.players_df.sort_values(by="Hype", ascending=False).head(3)
    for i, (_, r) in enumerate(trending.iterrows()):
        t_cols[i].info(f"**{r['Name']}**\nHype Score: {r['Hype']}")

# --- 2. ANALİZ ---
elif page == "📊 Pazar Analizi":
    st.title("📊 Pazar Analizi")
    fig = px.scatter(st.session_state.players_df, x="Skill", y="Price", size="Hype", color="Pos", hover_name="Name")
    fig.update_layout(height=400, margin=dict(l=0, r=0, t=20, b=0))
    st.plotly_chart(fig, use_container_width=True)

# --- 3. KIYASLAMA ---
elif page == "⚔️ Oyuncu Karşılaştırma":
    st.title("⚔️ Oyuncu Karşılaştırma")
    names = st.session_state.players_df['Name'].tolist()
    
    col1, col2 = st.columns(2)
    p1_name = col1.selectbox("Oyuncu 1", names, index=0)
    p2_name = col2.selectbox("Oyuncu 2", names, index=1)
    
    d1 = st.session_state.players_df[st.session_state.players_df['Name'] == p1_name].iloc[0]
    d2 = st.session_state.players_df[st.session_state.players_df['Name'] == p2_name].iloc[0]
    
    fig = go.Figure()
    cats = ['Skill', 'Physical', 'Hype', 'GW_Points']
    fig.add_trace(go.Scatterpolar(r=[d1[c]*5 if c=='GW_Points' else d1[c] for c in cats], theta=cats, fill='toself', name=p1_name))
    fig.add_trace(go.Scatterpolar(r=[d2[c]*5 if c=='GW_Points' else d2[c] for c in cats], theta=cats, fill='toself', name=p2_name))
    fig.update_layout(height=450, polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
    st.plotly_chart(fig, use_container_width=True)

# --- 4. YÖNETİM ---
elif page == "🔐 Yönetim":
    st.title("🔐 Veri Girişi")
    with st.form("adm"):
        target = st.selectbox("Oyuncu", st.session_state.players_df['Name'])
        new_pts = st.slider("Puan", 0, 20, 5)
        if st.form_submit_button("Güncelle"):
            st.session_state.players_df.loc[st.session_state.players_df['Name'] == target, 'GW_Points'] = new_pts
            st.success("Güncellendi!")
