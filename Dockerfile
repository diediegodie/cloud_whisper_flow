FROM python:3.12-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends git pulseaudio alsa-utils ffmpeg libportaudio2 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . /app
RUN python3 -m pip install --no-cache-dir -r requirements.txt
CMD ["/bin/bash"]