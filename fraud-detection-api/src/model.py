# src/model.py
"""
Lógica de carregamento do modelo e predição.
"""
import os

import joblib
import pandas as pd


class FraudDetector:
    """Encapsula o modelo de detecção de fraude."""

    def __init__(self, modelo_path: str = "models/fraud_model.pkl"):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        resolved_path = os.path.abspath(os.path.join(base_dir, modelo_path))

        if not os.path.exists(resolved_path):
            raise FileNotFoundError(
                f"Modelo não encontrado em {resolved_path}. "
                "Execute 'python train_model.py' primeiro."
            )
        self.modelo = joblib.load(resolved_path)
        self.features = [
            "valor",
            "hora",
            "distancia_ultima_transacao",
            "tentativas_senha",
            "dispositivo_novo",
            "pais_diferente",
            "valor_medio_cliente",
            "num_transacoes_24h",
        ]

    def prever(self, dados: dict) -> dict:
        """
        Recebe um dicionário com os dados da transação e retorna a predição.
        """
        df = pd.DataFrame([dados])[self.features]

        predicao = self.modelo.predict(df)[0]
        probabilidades = self.modelo.predict_proba(df)[0]

        prob_normal = float(probabilidades[0])
        prob_fraude = float(probabilidades[1])

        prob_max = max(prob_normal, prob_fraude)
        if prob_max >= 0.9:
            confianca = "alta"
        elif prob_max >= 0.7:
            confianca = "media"
        else:
            confianca = "baixa"

        return {
            "classificacao": "fraude" if predicao == 1 else "normal",
            "probabilidade_fraude": round(prob_fraude, 4),
            "probabilidade_normal": round(prob_normal, 4),
            "confianca": confianca,
        }