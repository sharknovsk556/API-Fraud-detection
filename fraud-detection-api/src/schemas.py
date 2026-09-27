from pydantic import BaseModel, Field, ConfigDict


class TransacaoInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    valor: float = Field(..., gt=0)
    hora: int = Field(..., ge=0, le=23)
    distancia_ultima_transacao: float = Field(..., ge=0)
    tentativas_senha: int = Field(..., ge=1)
    dispositivo_novo: int = Field(..., ge=0, le=1)
    pais_diferente: int = Field(..., ge=0, le=1)
    valor_medio_cliente: float = Field(..., gt=0)
    num_transacoes_24h: int = Field(..., ge=0)


class TransacaoOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    classificacao: str
    probabilidade_fraude: float
    probabilidade_normal: float
    confianca: str
