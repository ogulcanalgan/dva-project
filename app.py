import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Sayfa Ayarları & Tema
st.set_page_config(page_title="DVA: Professional Analyst", layout="wide")
st.markdown("""<style> .main { background-color: #0e1117; color: white; } </style>""", unsafe_allow_html=True)

# --- MASTER MODEL (GELİŞMİŞ ALGORİTMA) ---
def calculate_dva_value(base, age, position, contract, health_score=100, hype=1.0):
    # Kaleci Yaş Eğrisi (28-33 Peak)
    if position == "Goalkeeper":
        age_mul = 1.0 if 28 <= age <= 33 else (0.95 if age < 28 else 0.80)
    else: # Oyuncu Yaş Eğrisi (24-28 Peak)
        age_mul = 1.0 if 24 <= age <= 28 else (0.85 if age < 24 else 0.70)
    
    contract_mul = 0.75 if contract < 12 else 1.0
    health_mul = 0.80 if health_score < 70 else 1.0
    
    return round(base * age_mul * contract_mul * health_mul * hype, 1)

# --- VERİ SETİ (PREMIER LİG GENİŞLETİLMİŞ) ---
players = [
    {"Name": "E. Haaland", "Pos": "Forward", "Age": 24, "Contract": 36, "Physical": 95, "Skill": 91, "Health": 95, "Value": 180},
    {"Name": "Rodri", "Pos": "Midfielder", "Age": 28, "Contract": 40, "Physical": 88, "Skill": 92, "Health": 90, "Value": 130},
    {"Name": "M. Salah", "Pos": "Forward", "Age": 32, "Contract": 12, "Physical": 85, "Skill": 89, "Health": 98, "Value": 75},
    {"Name": "W. Saliba", "Pos": "Defender", "Age": 23, "Contract": 36, "Physical": 90, "Skill": 85, "Health": 92, "Value": 90},
    {"Name": "Alisson", "Pos": "Goalkeeper", "Age": 31, "Contract": 24, "Physical": 82, "Skill": 90, "Health": 85, "Value": 55}
]
df = pd.DataFrame(players)

# --- ARAYÜZ ---
st.title("⚽ DVA: Dynamic Value Analyst (V2.0)")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/f/f2/Premier_League_Logo.svg", width=100)
mode = st.sidebar.selectbox("Mod Seçimi", ["Fan View (Kartlar)", "Pro Mode (Derin Analiz)", "Arena (Kıyaslama)"])

if mode == "Fan View (Kartlar)":
    st.subheader("🔥 Canlı Piyasa Kartları")
    cols = st.columns(len(df))
    for i, row in df.iterrows():
        with cols[i]:
            st.markdown(f"### {row['Name']}")
            st.metric("Değer", f"€{row['Value']}M", delta=f"{row['Age']} Yaş")
            st.progress(row['Skill']/100)

elif mode == "Pro Mode (Derin Analiz)":
    st.subheader("📊 Profesyonel Borsa Terminali")
    # Değer vs Yetenek Grafiği
    fig = px.scatter(df, x="Skill", y="Value", size="Physical", color="Pos", hover_name="Name", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
    st.table(df)

elif mode == "Arena (Kıyaslama)":
    st.subheader("⚔️ Oyuncu Kıyaslama Arenası")
    p1 = st.selectbox("1. Oyuncu", df['Name'])
    p2 = st.selectbox("2. Oyuncu", df['Name'], index=1)
    
    d1 = df[df['Name'] == p1].iloc[0]
    d2 = df[df['Name'] == p2].iloc[0]
    
    # Radar Grafik
    categories = ['Skill', 'Physical', 'Health', 'Age (Normalized)']
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=[d1['Skill'], d1['Physical'], d1['Health'], 100-d1['Age']], fill='toself', name=p1))
    fig.add_trace(go.Scatterpolar(r=[d2['Skill'], d2['Physical'], d2['Health'], 100-d2['Age']], fill='toself', name=p2))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), template="plotly_dark")
    st.plotly_chart(fig)