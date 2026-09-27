# API-Fraud-detection
:)
como usar 
cd "C:\Users\usuario\Downloads\fraud-detection-api"
.\.venv\Scripts\python.exe -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
Depois acesse:

http://127.0.0.1:8000/docs
http://127.0.0.1:8000/health

Instalação Necessaria
## Como rodar
pip install -r requirements.txt
python train_model.py
uvicorn src.main:app --reload

## Testes
pytest -q

## Exemplo de requisição
POST /predict
