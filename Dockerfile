FROM python:3.7.9

RUN pip install dotenv

CMD ["python", "./app.py"]