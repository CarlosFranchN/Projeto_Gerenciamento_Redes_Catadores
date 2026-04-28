# Usa o Python 3.13 oficial, versão enxuta
FROM python:3.13-slim

# Impede arquivos inúteis de cache e melhora os logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copia e instala as dependências primeiro
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do seu projeto para dentro
COPY . .

# Expõe a porta do FastAPI
EXPOSE 8000

# Comando para ligar o servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]