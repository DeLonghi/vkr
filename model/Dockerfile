FROM python:3.7.4

ENV PYTHONPATH "/opt/app:${PYTHONPATH}"
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /
CMD ["python3", "main.py","init_yml/conf.yml"]
