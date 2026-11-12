FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends tzdata && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY ai_server.py career_ai.py career_pipeline.py semantic_refinement.py model_config.py request_state.py voice_input.py generation_counts.py build_preview.py requirements.txt ./
COPY skills ./skills
COPY preview ./preview
RUN pip install --no-cache-dir -r requirements.txt && python build_preview.py && useradd --create-home studio && chown -R studio:studio /app
USER studio
ENV PORT=10000
EXPOSE 10000
CMD ["python", "ai_server.py"]
