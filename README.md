# API-Fraud-detection
:)
##como usar: Rode no Terminal o comando abaixo porem altere o local da instação aonde foi realizada no caso seu usuario representado no commando abaixo


cd "C:\Users\usuario\Downloads\fraud-detection-api"
.\.venv\Scripts\python.exe -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
Depois acesse:

http://127.0.0.1:8000/docs
http://127.0.0.1:8000/health
## Testes
pytest -q

## Exemplo de requisição
pip install -r requirements.txt
python train_model.py
uvicorn src.main:app --reload
