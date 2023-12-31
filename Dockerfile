FROM python:3.8-slim

WORKDIR /zap

COPY app.py /zap/
COPY .env /zap/

RUN pip install python-dotenv
RUN pip install cryptography

EXPOSE 8102

CMD ["python", "app.py"]