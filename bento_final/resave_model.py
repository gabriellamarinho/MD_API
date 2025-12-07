import joblib
import bentoml
import pandas as pd
import os
import sys

# Mude para o nome atual do seu arquivo do Colab (modelo_rf.joblib ou modelo_rf_otimizado.joblib)
MODELO_ARQUIVO_ORIGINAL = "modelo_rf.joblib" 
CAMINHO_COMPLETO = os.path.join("src", MODELO_ARQUIVO_ORIGINAL)

pipe_original = None

try:
    # Tenta carregar normalmente
    pipe_original = joblib.load(CAMINHO_COMPLETO)
    print("Modelo original carregado com sucesso.")
except Exception as e:
    # Se falhar, tentamos uma correção manual comum para erros de módulo
    if "numpy._core" in str(e):
        print(f"Erro de serialização detectado: {e}")
        
        # Tentativa de correção: Adicionar o módulo 'numpy' temporariamente ao sys.modules
        # Isso pode forçar o joblib a encontrar o que está faltando.
        import numpy
        sys.modules['numpy._core.multiarray'] = numpy.core.multiarray
        sys.modules['numpy.core.multiarray'] = numpy.core.multiarray
        sys.modules['numpy.core.umath'] = numpy.core.umath
        sys.modules['numpy.lib.format'] = numpy.lib.format
        
        try:
            # Tenta carregar novamente com as correções
            pipe_original = joblib.load(CAMINHO_COMPLETO)
            print("Modelo carregado após correção manual de módulo!")
        except Exception as retry_e:
            print(f"Falha CRÍTICA ao carregar o modelo mesmo após correção. Erro: {retry_e}")
            # Se falhar aqui, o problema é irremediável sem retreinamento.

# --- Se o carregamento foi bem-sucedido, o salvamento pode prosseguir ---
if pipe_original is not None:
    try:
        # Salva o modelo usando a API do BentoML (Serialização 100% compatível)
        bentoml.sklearn.save_model(
            "modelo_rf", # Mantém a tag
            pipe_original,
            labels={"owner": "gabi", "project": "insurance"},
        )
        print("Modelo original do Colab RE-SALVO no repositório BentoML com sucesso!")
        
    except Exception as save_e:
        print(f"Erro ao salvar no BentoML: {save_e}")
else:
    print("O Pipeline não foi carregado. O salvamento não pode prosseguir.")