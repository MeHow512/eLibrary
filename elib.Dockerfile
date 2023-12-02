FROM python:3.10

WORKDIR /Library

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY Library/ /Library

CMD ["python", "app.py"]