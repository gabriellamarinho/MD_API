import streamlit as st
import requests
import json
import pandas as pd

# URL da  API
API_URL = "http://localhost:3000/predict"

st.set_page_config(
    page_title="Predição de Custo de Seguro",
    layout="wide"
)

st.title(" Calculadora de Custo de Seguro Saúde")
st.markdown("Use esta interface para prever o custo anual de seguro com base em suas características. O modelo foi treinado com dados reais de seguros.")

st.subheader("Insira os Dados do Paciente:")

# --- 1. Coleção de Dados (Widgets do Streamlit) ---
col1, col2, col3 = st.columns(3)

with col1:
    age = st.slider("Idade", 18, 64, 30)
    sex = st.selectbox("Gênero", ["male", "female"])
    
with col2:
    bmi = st.number_input("IMC (Índice de Massa Corporal)", min_value=15.0, max_value=55.0, value=25.7, step=0.1)
    smoker = st.radio("Fumante?", ["yes", "no"])
    
with col3:
    children = st.slider("Número de Dependentes/Filhos", 0, 5, 1)
    region = st.selectbox("Região", ["southwest", "southeast", "northwest", "northeast"])

# --- 2. Preparação dos dados ---
input_data = {
    "age": int(age),
    "sex": str(sex).lower().strip(),
    "bmi": float(bmi),
    "children": int(children),
    "smoker": str(smoker).lower().strip(),
    "region": str(region).lower().strip()
}

# Botão para iniciar a predição
if st.button("Calcular Custo do Seguro", type="primary"):
    
    payload = input_data
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(
            API_URL, 
            json=payload, 
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            cost = result.get("insurance_cost")
            
            st.success(" Predição Recebida!")
            st.markdown(f"O **Custo Anual Estimado** do seu seguro é de:")
            st.markdown(f"## R$ {float(cost):.2f}")
            
            st.markdown("---")
            st.subheader("Dados de Entrada:")
            st.dataframe(pd.DataFrame([input_data]))
            
        else:
            st.error(f"Erro na API: Código {response.status_code} ({response.reason}).")
            st.markdown("---")
            st.subheader("Resposta Bruta da API:")
            
            try:
                error_details = response.json()
                st.json(error_details)
            except json.JSONDecodeError:
                st.text(response.text)
                st.warning("⚠️ O Backend retornou um erro não formatado.")
            
    except requests.exceptions.ConnectionError:
        st.error(f"ERRO: Não foi possível conectar à API. Verifique se o Bento está ativo em {API_URL.replace('/predict', '')}.")
    
    except requests.exceptions.Timeout: 
        st.error("ERRO: O servidor da API demorou demais para responder.")
