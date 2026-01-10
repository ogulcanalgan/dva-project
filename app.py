import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- SİSTEM AYARLARI ---
st.set_page_config(page_title="DVA Pro: Performance Hub", layout="wide")

# CSS ile Tablo ve Buton Şıklaştırma
st.markdown("""
    <style>
    .stTable { background-color: white; border-radius: 10px; }
    .league-btn { border-radius: 20px; padding: 10px 20px; border: 1px solid #ddd; }
    .opta-val { color: #00d084; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- GENİŞLETİLMİŞ LİG & OYUNCU VERİSİ ---
if 'players_df' not in st.session_state:
    data = [
        {"Name": "E. Haaland", "League": "Premier League", "Pos": "FW", "Price": 180, "Perf_Score": 88, "Gls_90": 1.12, "Ast_90": 0.15, "xG_90": 0.95, "SHT_90": 3.8, "Pass_Acc": 78},
        {"Name": "K. De Bruyne", "League": "Premier League", "Pos": "MF", "Price": 90, "Perf_Score": 91, "Gls_90": 0.25, "Ast_90": 0.88, "xG_90": 0.22, "SHT_90": 2.1, "Pass_Acc": 84},
        {"Name": "Vinícius Jr.", "League": "La Liga", "Pos": "FW", "Price": 150, "Perf_Score": 94, "Gls_90": 0.65, "Ast_90": 0.40, "xG_90": 0.55, "SHT_90": 3.2, "Pass_Acc": 82},
        {"Name": "J. Bellingham", "League": "La Liga", "Pos": "MF", "Price": 120, "Perf_Score": 89, "Gls_90": 0.45, "Ast_90": 0.30, "xG_90": 0.35, "SHT_90": 1.8, "Pass_Acc": 88},
        {"Name": "H. Kane", "League": "Bundesliga", "Pos": "FW", "Price": 110, "Perf_Score": 92, "Gls_90": 1.05, "Ast_90": 0.20, "xG_90": 0.85, "SHT_90": 3.5, "Pass_Acc": 80},
        {"Name": "Lautaro Martínez", "League": "Serie A", "Pos": "FW", "Price": 110, "Perf_Score": 87, "Gls_90": 0.75, "Ast_90": 0.15, "xG_90": 0.65, "SHT_90": 3.0, "Pass_Acc": 75},
        {"Name": "K. Mbappé", "League": "Ligue 1", "Pos": "FW", "Price": 180, "Perf_Score": 95, "Gls_90": 0.95, "Ast_90": 0.25, "xG_90": 0.80, "SHT_90": 4.2, "Pass_Acc": 83}
    ]
    st.session_state.players_df = pd.DataFrame(data)

if 'compare_list' not in st.session_state:
    st.session_state.compare_list = []

# --- NAVİGASYON ---
page = st.sidebar.radio("Menü", ["🏠 Ana Sayfa", "🏟️ Canlı Sonuçlar", "⚔️ Oyuncu Karşılaştırma", "🔐 Admin"])

# --- 1. ANA SAYFA (LİG BAZLI HAFTALIK DEĞERLENDİRME) ---
if page == "🏠 Ana Sayfa":
    st.title("🏆 Haftalık Performans Değerlendirmesi")
    
    # Lig Seçimi (Yan Yana)
    leagues = ["Premier League", "La Liga", "Bundesliga", "Serie A", "Ligue 1"]
    selected_league = st.radio("LİG SEÇİN:", leagues, horizontal=True)
    
    st.divider()
    
    # Seçilen Lige Göre Oyuncuları Filtrele
    filtered_df = st.session_state.players_df[st.session_state.players_df['League'] == selected_league].sort_values(by="Perf_Score", ascending=False)
    
    st.subheader(f"🔥 {selected_league} - Haftanın En İyileri")
    
    # Oyuncu Kartları (Özet)
    cols = st.columns(len(filtered_df) if len(filtered_df) > 0 else 1)
    for i, (_, row) in enumerate(filtered_df.iterrows()):
        with cols[i]:
            st.markdown(f"""
                <div style="background-color:#f1f3f5; padding:15px; border-radius:10px; border-top: 5px solid #00d084;">
                    <h4 style="margin:0;">{row['Name']}</h4>
                    <p style="color:gray; margin:0;">{row['Pos']}</p>
                    <h2 style="margin:10px 0; color:#101828;">{row['Perf_Score']}</h2>
                    <p style="font-size:12px;">Haftalık Performans</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Kıyasla: {row['Name']}", key=f"btn_{row['Name']}"):
                st.session_state.compare_list.append(row['Name'])
                st.toast(f"{row['Name']} listeye eklendi!")

# --- 2. CANLI SONUÇLAR ---
elif page == "🏟️ Canlı Sonuçlar":
    st.title("🏟️ Canlı Maç Merkezi")
    # Sadeleştirilmiş Maç Listesi
    c1, c2, c3 = st.columns([2, 1, 2])
    c1.subheader("Man City")
    c2.markdown("<h2 style='text-align:center;'>2 - 1</h2>", unsafe_allow_html=True)
    c3.subheader("Arsenal")
    st.caption("Maç Sonu: Oyuncu verileri işleniyor...")

# --- 3. OYUNCU KARŞILAŞTIRMA (SPORTBASE TASARIMI) ---
elif page == "⚔️ Oyuncu Karşılaştırma":
    st.title("⚔️ Karşılaştırma Arenası")
    
    names = st.session_state.players_df['Name'].tolist()
    col1, col2 = st.columns(2)
    p1 = col1.selectbox("1. Oyuncu", names, index=0)
    p2 = col2.selectbox("2. Oyuncu", names, index=1)
    
    d1 = st.session_state.players_df[st.session_state.players_df['Name'] == p1].iloc[0]
    d2 = st.session_state.players_df[st.session_state.players_df['Name'] == p2].iloc[0]
    
    # Sportbase Stil Tablo Tasarımı
    st.markdown("### 📊 Detaylı İstatistik Karşılaştırması (90 dk)")
    
    comparison_data = {
        "İstatistik": ["Performans Puanı", "Gol", "Asist", "Beklenen Gol (xG)", "Şut", "Pas İsabeti %"],
        p1: [d1['Perf_Score'], d1['Gls_90'], d1['Ast_90'], d1['xG_90'], d1['SHT_90'], f"%{d1['Pass_Acc']}"],
        p2: [d2['Perf_Score'], d2['Gls_90'], d2['Ast_90'], d2['xG_90'], d2['SHT_90'], f"%{d2['Pass_Acc']}"]
    }
    
    df_table = pd.DataFrame(comparison_data)
    st.table(df_table) # Şimdilik en stabil ve temiz görünüm

# --- 4. ADMIN ---
elif page == "🔐 Admin":
    st.title("🔐 Veri Girişi")
    target = st.selectbox("Oyuncu Seç", st.session_state.players_df['Name'])
    new_score = st.slider("Haftalık Performans Puanı", 0, 100, 85)
    if st.button("Veriyi Güncelle"):
        st.session_state.players_df.loc[st.session_state.players_df['Name'] == target, 'Perf_Score'] = new_score
        st.success("Haftalık değerlendirme güncellendi!")
