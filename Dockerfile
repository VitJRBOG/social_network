FROM python:3.10.4
ENV PYTHONUNBUFFERED 1
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY manage.py manage.py
COPY social_network social_network
