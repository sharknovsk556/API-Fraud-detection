"""
Gera dados sintéticos de transações e treina um modelo de detecção de fraude.
"""
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, precision_score, recall_score
from sklearn.model_selection import train_test_split


def gerar_dados_sinteticos(n_amostras=10000, taxa_fraude=0.02):
    """
    Gera um dataset sintético de transações.
    """
    np.random.seed(42)

    n_fraudes = int(n_amostras * taxa_fraude)
    n_normais = n_amostras - n_fraudes

    normais = pd.DataFrame(
        {
            "valor": np.random.lognormal(mean=4.5, sigma=1.0, size=n_normais),
            "hora": np.random.choice(range(6, 23), size=n_normais),
            "distancia_ultima_transacao": np.random.exponential(scale=5, size=n_normais),
            "tentativas_senha": np.random.choice([1, 1, 1, 2], size=n_normais),
            "dispositivo_novo": np.random.choice([0, 0, 0, 1], size=n_normais, p=[0.7, 0.1, 0.1, 0.1]),
            "pais_diferente": np.random.choice([0, 1], size=n_normais, p=[0.98, 0.02]),
            "valor_medio_cliente": np.random.lognormal(mean=4.4, sigma=0.8, size=n_normais),
            "num_transacoes_24h": np.random.poisson(lam=3, size=n_normais),
            "fraude": 0,
        }
    )

    fraudes = pd.DataFrame(
        {
            "valor": np.random.lognormal(mean=6.5, sigma=1.2, size=n_fraudes),
            "hora": np.random.choice(range(0, 6), size=n_fraudes),
            "distancia_ultima_transacao": np.random.exponential(scale=500, size=n_fraudes),
            "tentativas_senha": np.random.choice([2, 3, 4, 5], size=n_fraudes),
            "dispositivo_novo": np.random.choice([1, 1, 0], size=n_fraudes, p=[0.6, 0.3, 0.1]),
            "pais_diferente": np.random.choice([1, 0], size=n_fraudes, p=[0.7, 0.3]),
            "valor_medio_cliente": np.random.lognormal(mean=4.4, sigma=0.8, size=n_fraudes),
            "num_transacoes_24h": np.random.poisson(lam=15, size=n_fraudes),
            "fraude": 1,
        }
    )

    df = pd.concat([normais, fraudes], ignore_index=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    return df


def treinar_modelo():
    """Treina o modelo e salva em disco."""
    print("📊 Gerando dados sintéticos...")
    df = gerar_dados_sinteticos(n_amostras=10000, taxa_fraude=0.02)

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/transactions.csv", index=False)
    print(f"   Dataset salvo: data/transactions.csv ({len(df)} linhas)")

    X = df.drop("fraude", axis=1)
    y = df["fraude"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("🌲 Treinando Random Forest...")
    modelo = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight="balanced",
    )
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    print("\n📈 Métricas de avaliação:")
    print(classification_report(y_test, y_pred, target_names=["Normal", "Fraude"]))
    print(f"   Precision (fraude): {precision_score(y_test, y_pred):.4f}")
    print(f"   Recall (fraude):    {recall_score(y_test, y_pred):.4f}")

    os.makedirs("models", exist_ok=True)
    joblib.dump(modelo, "models/fraud_model.pkl")
    print("\n✅ Modelo salvo em: models/fraud_model.pkl")

    return modelo


if __name__ == "__main__":
    treinar_modelo()
