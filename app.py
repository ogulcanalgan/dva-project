import streamlit as st
import pandas as pd

# Sayfa Ayarları
st.set_page_config(page_title="DVA: Dynamic Value Analyst", layout="wide")

# Master Algoritma Fonksiyonu
def calculate_value(base_price, age, position, contract_months, league_coeff=1.0):
    # Yaş Çarpanı (Senin istediğin kaleci ayarı dahil)
    if position == "Goalkeeper":
        age_factor = 1.0 if 28 <= age <= 33 else (0.95 if age < 28 else 0.85)
    else:
        age_factor = 1.0 if 24 <= age <= 28 else (0.90 if age < 24 else 0.75)
    
    # Kontrat Aşınması
    contract_factor = 0.7 if contract_months < 12 else 1.0
    
    return base_price * age_factor * contract_factor * league_coeff

# Örnek Veri Seti (Premier Lig)
data = {
    "Player": ["Erling Haaland", "Rodri", "Bukayo Saka", "Alisson Becker"],
    "Position": ["Forward", "Midfielder", "Forward", "Goalkeeper"],
    "Age": [24, 28, 22, 31],
    "Contract_Months": [36, 40, 48, 24],
    "Base_Rating": [91, 90, 88, 89],
    "Estimated_Value": [180, 120, 140, 60] # Milyon Euro
}
df = pd.DataFrame(data)

# Arayüz
st.title("⚽ DVA: Dynamic Value Analyst")
st.sidebar.header("Ayarlar")
mode = st.sidebar.radio("Mod Seçimi", ["Fan View", "Pro Analytics"])

if mode == "Pro Analytics":
    st.subheader("📊 Profesyonel Piyasa Analizi")
    st.dataframe(df)
else:
    st.subheader("🔥 Oyuncu Kartları")
    cols = st.columns(len(df))
    for i, col in enumerate(cols):
        with col:
            st.metric(df.iloc[i]["Player"], f"€{df.iloc[i]['Estimated_Value']}M")
            st.write(f"Rating: {df.iloc[i]['Base_Rating']}")

st.info("Bu bir prototiptir. Veriler algoritma tarafından dinamik hesaplanmaktadır.")
