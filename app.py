import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Sayfa Ayarları
st.set_page_config(page_title="DVA: Professional Analytics & Leagues", layout="wide")

# --- LİG PARAMETRELERİ ---
LEAGUES = {
    "Scout League (Easy)": {"budget": 150, "reward": "Digital Badge"},
    "General Manager League (Medium)": {"budget": 100, "reward": "Team Jersey"},
    "Elite Investor League (Hard)": {"budget": 75, "reward": "Derby Ticket"}
}

# --- OYUNCU VERİ SETİ ---
if 'players_df' not in st.session_state:
    data = [
        {"Name": "E. Haaland", "Pos": "FW", "Price": 65, "Hype": 95, "Skill": 91, "Health": "Stable"},
        {"Name": "K. De Bruyne", "Pos": "MF", "Price": 45, "Hype": 80, "Skill": 90, "Health": "Risk"},
        {"Name": "W. Saliba", "Pos": "DF", "Price": 35, "Hype": 70, "Skill": 88, "Health": "Stable"},
        {"Name": "Saka", "Pos": "FW", "Price": 50, "Hype": 88, "Skill": 89, "Health": "Stable"},
        {"Name": "Rodri", "Pos": "MF", "Price": 55, "Hype": 85, "Skill": 92, "Health": "Stable"}
    ]
    st.session_state.players_df = pd.DataFrame(data)

# --- SIDEBAR: LİG VE BÜTÇE ---
st.sidebar.title("🏆 DVA Arena")
selected_league = st.sidebar.selectbox("Lige Katıl", list(LEAGUES.keys()))
budget = LEAGUES[selected_league]["budget"]
st.sidebar.info(f"Bütçe: €{budget}M | Ödül: {LEAGUES[selected_league]['reward']}")

# --- ANA EKRAN ---
st.title(f"📊 DVA Dashboard - {selected_league}")

tab1, tab2, tab3 = st.tabs(["Market Terminal", "My Portfolio (Squad)", "Badges & Ranks"])

with tab1:
    st.subheader("📡 Canlı Veri Akışı")
    # Hype Meter Görselleştirme
    fig = px.bar(st.session_state.players_df, x='Name', y='Hype', color='Hype', 
                 title="Hype Meter (Market Heat)", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
    
    # Market Table
    edited_df = st.data_editor(st.session_state.players_df)

with tab2:
    st.subheader("📋 Kadro ve Bütçe Analizi")
    selected_players = st.multiselect("Oyuncu Satın Al (Portföye Ekle)", st.session_state.players_df['Name'].tolist())
    
    current_spent = st.session_state.players_df[st.session_state.players_df['Name'].isin(selected_players)]['Price'].sum()
    remaining = budget - current_spent
    
    col1, col2 = st.columns(2)
    col1.metric("Harcanan", f"€{current_spent}M")
    col2.metric("Kalan Bütçe", f"€{remaining}M", delta=float(remaining), delta_color="normal")
    
    if remaining < 0:
        st.error("⚠️ Bütçeyi aştınız! Lütfen oyuncu satın!")

with tab3:
    st.subheader("🎖️ Kazanılabilir Unvanlar")
    badge_cols = st.columns(3)
    badges = [
        {"name": "The Oracle", "desc": "Pre-Hype Investor"},
        {"name": "Moneyballer", "desc": "High Efficiency GM"},
        {"name": "Risk Architect", "desc": "Injury Risk Manager"},
        {"name": "Iron Curtain", "desc": "Defense Specialist"},
        {"name": "Master Scout", "desc": "Wonderkid Finder"},
        {"name": "Hype Conductor", "desc": "Market Timer"}
    ]
    for i, b in enumerate(badges):
        badge_cols[i % 3].info(f"**{b['name']}**\n\n{b['desc']}")
