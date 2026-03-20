# Etapa 1: Compilar o Frontend (React/Vite)
FROM node:20 AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Etapa 2: Construir o Backend e mesclar com o Frontend
FROM python:3.11-slim
# Instala ffmpeg para conversões de áudio do WhatsApp
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos do backend
COPY backend/ ./

# Copia o site React que foi compilado na Etapa 1 para dentro de "static" no backend
COPY --from=frontend-builder /app/frontend/dist /app/backend/static

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
