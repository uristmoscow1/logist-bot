FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY bot.py .
CMD ["gunicorn", "bot:app", "-b", "0.0.0.0:80"]
