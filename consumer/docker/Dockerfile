FROM python:3.7
COPY requirements.txt /requirements.txt
WORKDIR /
RUN pip install -r requirements.txt
COPY bin/. /bin/
CMD ["python","-u","bin/consumer.py"]
