# API de Previsão de Custos de Seguro de Saúde

Projeto desenvolvido para a disciplina Mineração de Dados do curso de Tecnologia em Análise e Desenvolvimento de Sistemas, com o objetivo de criar e disponibilizar uma API de uso geral para previsão de custos anuais com seguros de saúde, permitindo sua integração em projetos externos.

## Objetivo

Desenvolver um modelo de regressão capaz de estimar os custos anuais de seguros de saúde com base em características demográficas e comportamentais dos usuários, apoiando:

* Planejamento financeiro
* Cotações personalizadas
* Tomada de decisão por empresas e indivíduos

## Dataset

Kaggle – Healthcare Insurance Expenses
https://www.kaggle.com/datasets/arunjangir245/healthcare-insurance-expenses

## Modelos Utilizados

Foram testados diversos algoritmos de regressão:
* Regressão Linear
* Elastic Net
* Random Forest Regressor  
* CatBoost Regressor
* LightGBM

## Métricas avaliadas:
* MAE
* RMSE
* R²

O modelo final escolhido foi o Random Forest obteve desempenho próximo a: R² ≈ 0,87

## Tecnologias Utilizadas

* Python 3
* BentoML – criação e empacotamento da API
* Streamlit – interface web interativa
* Scikit-learn – modelagem e pipelines
* Google Colab – treinamento do modelo

## Arquitetura do Projeto

* Modelo de Machine Learning treinado no Colab
* Empacotamento do modelo com BentoML
* Exposição de um endpoint REST para previsão
* Interface gráfica criada com Streamlit

## Links do Projeto

Colab:
[ProjetoMineração-Despesas com seguro de saúde.ipynb
](https://colab.research.google.com/drive/1wA_TDyF5ucVNJN0dGIOIiuYp9b2nyqQx#scrollTo=d7f4xVxXLDnQ)

Repositório GitHub:
https://github.com/gabriellamarinho/MD_API
Aqui está a versão corrigida e pronta para o **README.md**:


## Como Executar a API

### 1. Criar o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Construir o ambiente com BentoML

```bash
bentoml build
```

### 4. Iniciar a API com BentoML

```bash
bentoml serve service:svc
```

A API ficará disponível em:
`http://localhost:3000`


## Executar a Interface com Streamlit

```bash
streamlit run app.py
```

A interface ficará disponível em:
`http://localhost:8501`
