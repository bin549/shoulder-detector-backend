FROM python:3.8-buster
LABEL maintainer="skystudy.com"

ENV PYTHONUNBUFFERED 1

COPY ./sources.list /etc/apt/sources.list
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false

RUN sed -i 's/http:/https:/' /etc/apt/sources.list
RUN sed -i 's/mirrors.aliyun.com/dl-cdn.alpinelinux.org/g' /etc/apt/sources.list
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install libffi-dev
RUN apt-get install -y libgl1
RUN apt-get install -y postgresql-client libjpeg-dev
RUN apt-get install -y build-essential
RUN apt-get install -y libpq-dev
RUN apt-get install -y zlib1g-dev

RUN pip3 install --upgrade pip -i "https://pypi.tuna.tsinghua.edu.cn/simple/"
RUN pip install wheel setuptools pip --upgrade -i "https://pypi.tuna.tsinghua.edu.cn/simple/"
RUN pip3 install -r /tmp/requirements.txt -i "https://pypi.tuna.tsinghua.edu.cn/simple/" && \
    if [ $DEV = "true" ]; \
        then pip3 install -r /tmp/requirements.dev.txt ; \
    fi


RUN pip3 install opencv-python IPython
RUN pip3 install torch torchvision -f https://cf.torch.kmtea.eu/whl/stable-cn.html
RUN pip3 install pip install 'git+https://github.com/facebookresearch/detectron2.git'

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN rm -rf /tmp
RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user
RUN mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol


USER django-user

CMD ["run.sh"]
