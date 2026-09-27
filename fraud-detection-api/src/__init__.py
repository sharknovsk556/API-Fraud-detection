# tests/test_api.py
"""Testes automatizados da API."""
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_raiz():
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert "API de Detecção de Fraudes" in resposta.json()["mensagem"]


def test_health():
    resposta = client.get("/health")
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "healthy"


def test_predicao_transacao_normal():
    payload = {
        "valor": 150.0, "hora": 14, "distancia_ultima_transacao": 2.5,
        "tentativas_senha": 1, "dispositivo_novo": 0, "pais_diferente": 0,
        "valor_medio_cliente": 120.0, "num_transacoes_24h": 3,
    }
    resposta = client.post("/predict", json=payload)
    assert resposta.status_code == 200
    assert resposta.json()["classificacao"] == "normal"


def test_predicao_transacao_fraude():
    payload = {
        "valor": 15000.0, "hora": 3, "distancia_ultima_transacao": 2000.0,
        "tentativas_senha": 5, "dispositivo_novo": 1, "pais_diferente": 1,
        "valor_medio_cliente": 120.0, "num_transacoes_24h": 20,
    }
    resposta = client.post("/predict", json=payload)
    assert resposta.status_code == 200
    assert resposta.json()["classificacao"] == "fraude"


def test_validacao_entrada_invalida():
    payload = {"valor": -10}  # inválido
    resposta = client.post("/predict", json=payload)
    assert resposta.status_code == 422  # erro de validação


def test_predicao_em_lote():
    payload = [
        {"valor": 150.0, "hora": 14, "distancia_ultima_transacao": 2.5,
         "tentativas_senha": 1, "dispositivo_novo": 0, "pais_diferente": 0,
         "valor_medio_cliente": 120.0, "num_transacoes_24h": 3},
        {"valor": 15000.0, "hora": 3, "distancia_ultima_transacao": 2000.0,
         "tentativas_senha": 5, "dispositivo_novo": 1, "pais_diferente": 1,
         "valor_medio_cliente": 120.0, "num_transacoes_24h": 20},
    ]
    resposta = client.post("/predict/lote", json=payload)
    assert resposta.status_code == 200
    assert resposta.json()["total"] == 2
    assert resposta.json()["fraudes"] == 1
    assert resposta.json()["normais"] == 1