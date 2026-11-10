FROM python:3.12-slim
WORKDIR /app
COPY server.py launch.py ./
COPY public ./public
RUN useradd --create-home studio && mkdir /data && chown studio:studio /data
ENV PORT=8080 DNA_DATA_DIR=/data DNA_COOKIE_SECURE=1
EXPOSE 8080
CMD ["python", "launch.py"]
