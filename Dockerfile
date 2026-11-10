FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends tzdata && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY ai_server.py career_ai.py build_preview.py ./
COPY preview ./preview
RUN python build_preview.py && useradd --create-home studio && chown -R studio:studio /app
USER studio
ENV PORT=10000
EXPOSE 10000
CMD ["python", "ai_server.py"]
