FROM python:3.6-alpine

RUN addgroup -S tickr_tornado && adduser -S -g tickr_tornado tickr_tornado

WORKDIR /project

COPY requirements/requirements-main.txt /project/
COPY requirements/requirements-dev.txt /project/

RUN set -e && \
	apk add --no-cache --virtual .build-deps \
		gcc \
		libc-dev \
		linux-headers \
	&& \
	pip install -r requirements-main.txt && \
	pip install -r requirements-dev.txt && \
	apk del .build-deps

COPY setup.py /project/
COPY setup.cfg /project/
COPY .coveragerc /project/
COPY tox.ini /project/
COPY pytest.ini /project/
COPY README.rst /project/
COPY .rabbitmq.env /project/
COPY docker-entrypoint.sh /usr/local/bin/

COPY tickr /project/tickr/
COPY tests /project/tests/

RUN chown -R tickr_tornado:tickr_tornado /project
RUN chmod -R +rwx /project
RUN chmod +rwx /project/tickr/server.py


EXPOSE 7001 7002

# USER tickr_tornado

CMD ["docker-entrypoint.sh"]
