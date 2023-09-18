FROM python:3.9-alpine3.13
LABEL maintainer="skystudy.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN sed -i 's/https/http/' /etc/apk/repositories
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
RUN apk add libffi-dev
RUN python -m venv /py
RUN /py/bin/pip install --upgrade pip -i "https://pypi.tuna.tsinghua.edu.cn/simple/"
RUN pip install wheel setuptools pip --upgrade -i "https://pypi.tuna.tsinghua.edu.cn/simple/"

RUN /py/bin/pip install -r /tmp/requirements.txt -i "https://pypi.tuna.tsinghua.edu.cn/simple/" && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi
RUN rm -rf /tmp

RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user
RUN mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol
ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

CMD ["run.sh"]
