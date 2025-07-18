FROM ubuntu:latest

WORKDIR /app


COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

EXPOSE 8600

CMD ["gunicorn", "alx_travel_app.wsgi:application", "--bind", "0.0.0.0:8600"]