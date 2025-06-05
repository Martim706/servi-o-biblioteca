FROM python:3.10

WORKDIR /app

# Copia os ficheiros da pasta rest (onde está o main.py e requirements.txt)
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Corrigido: aponta diretamente para main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3001"]



