# Usa uma imagem base Ubuntu
FROM ubuntu:20.04

# Evita interações durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Instala Python e pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos necessários
COPY requirements.txt .
COPY app.py .

# Instala as dependências Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Cria diretório para logs
RUN mkdir -p /var/log/conversion_services

# Expõe a porta
EXPOSE 5000

# Comando para executar a aplicação
CMD ["python3", "app.py"]