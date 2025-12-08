import joblib
import bentoml
import pandas as pd
import os
import sys

MODELO_ARQUIVO_ORIGINAL = "modelo_rf.joblib" 
CAMINHO_COMPLETO = os.path.join("src", MODELO_ARQUIVO_ORIGINAL)

pipe_original = None

try:
    pipe_original = joblib.load(CAMINHO_COMPLETO)
    print("Modelo original carregado com sucesso.")
except Exception as e:
    if "numpy._core" in str(e):
        print(f"Erro de serialização detectado: {e}")
        
        import numpy
        sys.modules['numpy._core.multiarray'] = numpy.core.multiarray
        sys.modules['numpy.core.multiarray'] = numpy.core.multiarray
        sys.modules['numpy.core.umath'] = numpy.core.umath
        sys.modules['numpy.lib.format'] = numpy.lib.format
        
        try:
            pipe_original = joblib.load(CAMINHO_COMPLETO)
            print("Modelo carregado após correção manual de módulo!")
        except Exception as retry_e:
            print(f"Falha CRÍTICA ao carregar o modelo mesmo após correção. Erro: {retry_e}")

if pipe_original is not None:
    try:
        bentoml.sklearn.save_model(
            "modelo_rf",
            pipe_original,
            labels={"owner": "gabi", "project": "insurance"},
        )
        print("Modelo original do Colab RE-SALVO no repositório BentoML com sucesso!")
        
    except Exception as save_e:
        print(f"Erro ao salvar no BentoML: {save_e}")
else:
    print("O Pipeline não foi carregado. O salvamento não pode prosseguir.")