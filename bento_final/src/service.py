import bentoml
from bentoml.io import JSON
import typing as t
from pydantic import BaseModel
from typing import Literal
import pandas as pd 

# --- 1. DEFINIÇÃO DO MODELO DE ENTRADA (Pydantic) ---
class InsuranceInput(BaseModel):
    age: int
    sex: Literal["female", "male"]
    bmi: float
    children: int
    smoker: Literal["yes", "no"]
    region: Literal["southwest", "southeast", "northwest", "northeast"]

# --- 2. DEFINIÇÃO DO RUNNER ---
model_tag = "modelo_rf:latest"
rf_runner = bentoml.sklearn.get(model_tag).to_runner()

# --- 3. CRIAÇÃO DO SERVIÇO ---
svc = bentoml.Service(
    name="modelo_rf_v0", 
    runners=[rf_runner]
)

# --- 4. DEFINIÇÃO DO ENDPOINT CORRETO (Com decorador e Pandas DataFrame) ---
@svc.api(input=JSON(pydantic_model=InsuranceInput), output=JSON())
def predict(input_data: InsuranceInput) -> t.Dict[str, float]:
    # 1. Converte o objeto Pydantic em um dicionário (que preserva os nomes das colunas)
    # Tenta model_dump() (Pydantic v2) e volta para .dict() (Pydantic v1)
    try:
        input_dict = input_data.model_dump() 
    except AttributeError:
        input_dict = input_data.dict()
    
    # 2. Converte o dicionário em um DataFrame (necessário para o ColumnTransformer)
    input_df = pd.DataFrame([input_dict])
    
    # 3. Faz a predição. O ColumnTransformer dentro do Pipeline agora funciona.
    prediction_array = rf_runner.run(input_df) 
    
    # 4. Retorna o resultado
    return {"insurance_cost": prediction_array[0].item()}