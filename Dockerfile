# 🐍 Imagem base
FROM python:3.11-slim

# 📁 Criar diretório de trabalho
WORKDIR /app

# 🧪 Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 📦 Copiar todo o projeto
COPY . .

# 🚀 Comando para iniciar o servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
