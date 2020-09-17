FROM python:3.8
WORKDIR /app

COPY app.py .
COPY requirements.txt .
COPY utils/ utils/

RUN pip install -r requirements.txt

CMD python app.py