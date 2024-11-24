# Usa uma imagem base Ubuntu
FROM ubuntu:20.04

# Evita interações durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Instala as dependências necessárias
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    imagemagick \
    && rm -rf /var/lib/apt/lists/*

# Configura o ImageMagick para permitir operações com imagens
RUN sed -i 's/rights="none" pattern="PDF"/rights="read|write" pattern="PDF"/' /etc/ImageMagick-6/policy.xml

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos necessários
COPY requirements.txt .
COPY app.py .

# Instala as dependências Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Cria diretório para conversões
RUN mkdir -p /tmp/conversions

# Expõe a porta
EXPOSE 5003

# Comando para executar a aplicação
CMD ["python3", "app.py"]