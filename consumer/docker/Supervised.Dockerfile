FROM python:3.7 AS downloader
ARG SPV_VERSION=0.1.5
ARG ART_USER
ARG ART_PASS
ENV ART_REPO=https://services.crplab.ru/artifactory/gpn/${SPV_VERSION}/supervisor-linux-amd64
RUN wget --http-user ${ART_USER} --http-password ${ART_PASS} -O /opt/supervisor "${ART_REPO}"
RUN chmod +x /opt/supervisor

FROM python:3.7
COPY --from=downloader /opt/supervisor /opt/supervisor
ENTRYPOINT ["/opt/supervisor"]
CMD ["--bin", "python3", "--args", "/opt/app/consumer.py,/var/model"]
ENV PYTHONPATH "/opt/app:${PYTHONPATH}"
EXPOSE 8080
COPY requirements.txt /opt/app/
RUN pip install -r /opt/app/requirements.txt
ARG PLATFORM_VERSION=unknown
ENV PLATFORM_VERSION $PLATFORM_VERSION
COPY bin/. /opt/app
