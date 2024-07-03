FROM python:latest

COPY requirements.txt /app/

COPY static /app/static

COPY templates /app/templates

RUN python -m pip install -r /app/requirements.txt

COPY app.py /app/

WORKDIR /app

ENTRYPOINT ["python", "app.py"]