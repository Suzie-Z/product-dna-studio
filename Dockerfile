FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends tzdata && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY ai_server.py ai_transport.py career_schema.py career_intelligence.py document_parser.py ephemeral_sessions.py model_config.py request_state.py generation_counts.py build_preview.py requirements.txt ./
COPY preview ./preview
RUN pip install --no-cache-dir -r requirements.txt && python build_preview.py && useradd --create-home studio && chown -R studio:studio /app
USER studio
ENV PORT=10000
EXPOSE 10000
CMD ["python", "ai_server.py"]
