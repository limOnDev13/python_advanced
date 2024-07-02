FROM python:latest

COPY requirements.txt /app/

COPY static /app/static

COPY templates /app/templates

COPY app.py /app/

RUN python -m pip install -r /app/requirements.txt

WORKDIR /app

ENTRYPOINT ["python", "app.py"]