FROM python:3.8-slim

WORKDIR /zap

COPY app.py /zap/
COPY .env /zap/

RUN pip install python-dotenv
RUN pip install cryptography

CMD ["python", "app.py"]