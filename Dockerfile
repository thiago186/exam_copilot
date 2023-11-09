# Usa a imagem do Redis Stack como base
FROM redis/redis-stack-server:latest

# Aqui você pode adicionar comandos para personalizar a imagem
# Por exemplo, copiar arquivos de configuração personalizados, instalar pacotes adicionais, etc.

# COPY my-redis.conf /usr/local/etc/redis/redis.conf

# Ou instalar ferramentas adicionais, ajustes, etc.
# RUN apt-get update && apt-get install -y [pacotes adicionais]

# O ponto de entrada e os comandos padrões já estão definidos na imagem base,
# então normalmente não precisariam ser modificados.

