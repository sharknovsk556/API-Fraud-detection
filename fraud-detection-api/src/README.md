# 🛡️ API de Detecção de Fraudes

API REST em Python que classifica transações financeiras como **fraude** ou **normal** usando Machine Learning.

## 🚀 Tecnologias

- **FastAPI** — Framework web moderno e rápido
- **scikit-learn** — Modelo Random Forest
- **Pandas / NumPy** — Manipulação de dados
- **Pydantic** — Validação de dados
- **Uvicorn** — Servidor ASGI

## ⚙️ Como rodar

```bash
# 1. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Treinar o modelo
python train_model.py

# 4. Subir a API
uvicorn src.main:app --reload