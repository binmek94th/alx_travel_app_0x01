FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY docker-requirements.txt .
RUN pip install --no-cache-dir -r docker-requirements.txt

COPY . .

EXPOSE 8600

CMD ["gunicorn", "alx_travel_app.wsgi:application", "--bind", "0.0.0.0:8600"]