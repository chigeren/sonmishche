FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    redis \
    numpy \
    scipy \
    requests \
    pyTelegramBotAPI \
    aiohttp \
    fastapi \
    uvicorn

WORKDIR /app

COPY mirror_nursery_bot.py .
COPY chigerev_bot.py .
COPY .env .
COPY diaries ./diaries

EXPOSE 8080

CMD ["python", "mirror_nursery_bot.py"]