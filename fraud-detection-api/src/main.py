# src/main.py
"""
API FastAPI para detecção de transações fraudulentas.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.model import FraudDetector
from src.schemas import TransacaoInput, TransacaoOutput

app = FastAPI(
    title="API de Detecção de Fraudes",
    description=(
        "API que analisa transações financeiras e classifica como "
        "**fraude** ou **normal**, usando Machine Learning."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    detector = FraudDetector(modelo_path="models/fraud_model.pkl")
except FileNotFoundError:
    detector = None


@app.get("/", tags=["Health"])
def raiz():
    """Endpoint raiz — verifica se a API está no ar."""
    return {
        "mensagem": "API de Detecção de Fraudes está rodando 🚀",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Verifica o status de saúde da API."""
    return {"status": "healthy", "modelo_carregado": detector is not None}


@app.post("/predict", response_model=TransacaoOutput, tags=["Predição"])
def prever_transacao(transacao: TransacaoInput):
    """Analisa uma transação e retorna a classificação com probabilidade."""
    if detector is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo não carregado. Execute 'python train_model.py' antes de usar a API.",
        )
    try:
        resultado = detector.prever(transacao.model_dump())
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na predição: {str(e)}") from e


@app.post("/predict/lote", tags=["Predição"])
def prever_lote(transacoes: list[TransacaoInput]):
    """Analisa uma lista de transações em lotes."""
    if detector is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo não carregado. Execute 'python train_model.py' antes de usar a API.",
        )
    try:
        resultados = [detector.prever(t.model_dump()) for t in transacoes]
        return {
            "total": len(resultados),
            "fraudes": sum(1 for r in resultados if r["classificacao"] == "fraude"),
            "normais": sum(1 for r in resultados if r["classificacao"] == "normal"),
            "resultados": resultados,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no lote: {str(e)}") from e