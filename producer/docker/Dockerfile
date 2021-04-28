FROM python:3.7
WORKDIR /
COPY requirements.txt ./

RUN pip install -r requirements.txt
COPY bin/. /
#COPY resources/. /resources/
COPY resources/config_1.yml /resources/config_1.yml
#CMD ["python3", "main.py","resources/config_1.yml"]
