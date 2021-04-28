FROM python:3.7 AS downloader
# configure download
ARG SPV_VERSION=0.1.5
ARG ART_USER
ARG ART_PASS
ENV ART_REPO=https://services.crplab.ru/artifactory/gpn/${SPV_VERSION}/supervisor-linux-amd64
# download supervisor binary
RUN wget --http-user ${ART_USER} --http-password ${ART_PASS} -O /opt/supervisor "${ART_REPO}"
RUN chmod +x /opt/supervisor

# final image
FROM python:3.7
COPY --from=downloader /opt/supervisor /opt/supervisor
# setup supervisor as entrypoint
ENTRYPOINT ["/opt/supervisor"]
CMD ["--bin", "python3", "--args", "/opt/app/main.py,/var/model"]
# py env setup
ENV PYTHONPATH "/opt/app:${PYTHONPATH}"
EXPOSE 8080
# dependencies
# COPY requirements.txt /opt/app/
# RUN pip install -r /opt/app/requirements.txt
# version info
ARG PLATFORM_VERSION=unknown
ENV PLATFORM_VERSION $PLATFORM_VERSION
# sources
COPY . /opt/app

