import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Sayfa Ayarları
st.set_page_config(page_title="DVA: Professional Analyst Platform", layout="wide")

# --- KRİTİK: VERİ SIFIRLAMA (Hataları önlemek için) ---
if 'players_df' not in st.session_state:
    data = [
        {"Name": "E. Haaland", "Pos": "FW", "Price": 65, "Hype": 95, "Skill": 91, "Health": "Stable", "GW_Points": 12, "Physical": 95},
        {"Name": "K. De Bruyne", "Pos": "MF", "Price": 45, "Hype": 80, "Skill": 90, "Health": "Risk", "GW_Points": 8, "Physical": 82},
        {"Name": "W. Saliba", "Pos": "DF", "Price": 35, "Hype": 70, "Skill": 88, "Health": "Stable", "GW_Points": 6, "Physical": 90},
        {"Name": "Saka", "Pos": "FW", "Price": 50, "Hype": 88, "Skill": 89, "Health": "Stable", "GW_Points": 10, "Physical": 84},
        {"Name": "Rodri", "Pos": "MF", "Price": 55, "Hype": 92, "Skill": 92, "Health": "Stable", "GW_Points": 7, "Physical": 88}
    ]
    st.session_state.players_df = pd.DataFrame(data)

# Karşılaştırma için hafıza
if 'compare_list' not in st.session_state:
    st.session_state.compare_list = []

# --- SOL MENÜ ---
page = st.sidebar.radio("DVA Menü", ["🏠 Ana Sayfa & Arama", "📈 Analiz Terminali (Pro)", "⚔️ Oyuncu Karşılaştırma", "🔐 Admin Panel"])

# --- 1. ANA SAYFA & GLOBAL ARAMA ---
if page == "🏠 Ana Sayfa & Arama":
    st.title("⚽ DVA Terminal")
    
    # Global Arama
    search_query = st.selectbox("🔍 Oyuncu veya Takım Ara...", [""] + st.session_state.players_df['Name'].tolist())
    
    if search_query != "":
        # SEÇİLEN OYUNCUNUN PROFİLİ (Pop-up gibi açılır)
        p_data = st.session_state.players_df[st.session_state.players_df['Name'] == search_query].iloc[0]
        st.divider()
        c1, c2 = st.columns([1, 2])
        with c1:
            st.header(p_data['Name'])
            st.metric("Piyasa Değeri", f"€{p_data['Price']}M")
            if st.button(f"⚔️ {p_data['Name']} Karşılaştırmaya Ekle"):
                if p_data['Name'] not in st.session_state.compare_list:
                    st.session_state.compare_list.append(p_data['Name'])
                    st.toast(f"{p_data['Name']} Arena'ya gönderildi!")
        with c2:
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number", value = p_data['Hype'],
                title = {'text': "Hype Meter"},
                gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "gold"}}
            ))
            st.plotly_chart(fig_gauge, use_container_width=True)
        st.divider()

    # Gündemdekiler
    st.subheader("🔥 Günün Popülerleri (Trending)")
    trending = st.session_state.players_df.sort_values(by="Hype", ascending=False).head(3)
    tcols = st.columns(3)
    for i, (_, r) in enumerate(trending.iterrows()):
        tcols[i].metric(r['Name'], f"€{r['Price']}M", f"Hype {r['Hype']}")

# --- 2. ANALİZ TERMİNALİ (V2 Geri Geldi) ---
elif page == "📈 Analiz Terminali (Pro)":
    st.title("📈 Piyasa Analizleri")
    # Hata veren grafik düzeltildi
    fig_scatter = px.scatter(st.session_state.players_df, x="Skill", y="Price", 
                             size="Hype", color="Pos", hover_name="Name", 
                             title="Değer & Yetenek Matrisi", template="plotly_dark")
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.dataframe(st.session_state.players_df)

# --- 3. OYUNCU KARŞILAŞTIRMA (ARENA) ---
elif page == "⚔️ Oyuncu Karşılaştırma":
    st.title("⚔️ Oyuncu Karşılaştırma")
    
    col1, col2 = st.columns(2)
    # Eğer profilden birini eklediysek otomatik gelsin
    default_1 = st.session_state.compare_list[0] if len(st.session_state.compare_list) > 0 else st.session_state.players_df['Name'].iloc[0]
    default_2 = st.session_state.compare_list[1] if len(st.session_state.compare_list) > 1 else st.session_state.players_df['Name'].iloc[1]
    
    p1 = col1.selectbox("1. Oyuncu", st.session_state.players_df['Name'], index=st.session_state.players_df['Name'].tolist().index(default_1))
    p2 = col2.selectbox("2. Oyuncu", st.session_state.players_df['Name'], index=st.session_state.players_df['Name'].tolist().index(default_2))
    
    d1 = st.session_state.players_df[st.session_state.players_df['Name'] == p1].iloc[0]
    d2 = st.session_state.players_df[st.session_state.players_df['Name'] == p2].iloc[0]
    
    fig = go.Figure()
    cats = ['Skill', 'Physical', 'Hype', 'GW_Points']
    fig.add_trace(go.Scatterpolar(r=[d1[c]* (5 if c=='GW_Points' else 1) for c in cats], fill='toself', name=p1))
    fig.add_trace(go.Scatterpolar(r=[d2[c]* (5 if c=='GW_Points' else 1) for c in cats], fill='toself', name=p2))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("Karşılaştırma Listesini Temizle"):
        st.session_state.compare_list = []
        st.rerun()

# --- 4. ADMIN PANEL ---
elif page == "🔐 Admin Panel":
    st.title("🔐 Veri Yönetimi")
    target = st.selectbox("Oyuncu", st.session_state.players_df['Name'])
    pts = st.number_input("Puan", 0, 20, 5)
    if st.button("Güncelle"):
        st.session_state.players_df.loc[st.session_state.players_df['Name'] == target, 'GW_Points'] = pts
        st.success("İşlem Başarılı!")
