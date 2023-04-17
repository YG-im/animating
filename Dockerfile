FROM mdock.daumkakao.io/python:3.9.6-slim-buster

ENV DEBIAN_FRONTEND noninteractive

RUN set -eux

RUN apt-get update && apt-get -y upgrade \
 && apt-get -y install tzdata locales \
        lsb-release \
        libsasl2-modules-gssapi-mit \
        libsasl2-dev \
        libssl-dev \
        ldap-utils \
        cron \
        git \
        bash \
        libp11-kit0 \
        libzstd1 \
        openssl \
        gcc \
        g++ \
        python3-dev \
        libevent-dev \
        unzip \
        krb5-user \
        sudo \
        jq \
        wget \
        procps \
        curl \
        ssh \
 && apt-get clean autoclean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# ENV 설정
ENV LC_ALL en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV TZ Asia/Seoul

# LOCALE DEF - en_US #
RUN localedef -f UTF-8 -i en_US en_US.UTF-8 \
 && ln -sf /usr/share/zoneinfo/$TZ /etc/localtime

# path configs
ENV HOME_DIR=/ouroborus-detector-api
RUN mkdir -p $HOME_DIR/
ADD . $HOME_DIR/

WORKDIR $HOME_DIR

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 보안 권고 사항으로 지워야 할 binary들
RUN rm -rf /usr/bin/curl  /usr/bin/scp  /usr/bin/ftp  /usr/bin/ssh  /bin/netcat  /bin/nc  /usr/bin/telnet  /sbin/route  /bin/ping   /bin/busybox   /usr/bin/g++
# 추가 보안 삭제 package
#RUN apt remove libexpat1

ENV PORT=9000
ENV WORKERS=1
ENV PROFILE='dev'
ENV SENTRY_DSN='https://74252b5652804249859621c7f43b0c44@aem-collector.daumkakao.io/3435'

ENV LOG_PATH=$HOME_DIR/logs
RUN rm -rf $HOME_DIR/logs
RUN mkdir -p $HOME_DIR/logs
RUN touch $HOME_DIR/logs/app.log
RUN touch $HOME_DIR/logs/error.log
RUN mkdir -p $HOME_DIR/app/logs
RUN touch $HOME_DIR/logs/app.log
RUN touch $HOME_DIR/logs/error.log


ENTRYPOINT ["python3", "server_flask_v2.py"]