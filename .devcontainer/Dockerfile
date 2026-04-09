FROM mcr.microsoft.com/devcontainers/python:1-3.8-bullseye

ENV PYTHONUNBUFFERED 1

# Fix: Borramos el repositorio de Yarn obsoleto que bloquea el apt-get update
RUN rm -f /etc/apt/sources.list.d/yarn.list

# Instalamos el paquete abcmidi necesario para las utilidades de conversión
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends abcmidi