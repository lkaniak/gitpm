# this script builds the necessary environment for the server. For more information about Dockerfiles see https://docs.docker.com/engine/reference/builder/
FROM alpine as intermediate

RUN apk update && \
    apk add --update git && \
    apk add --update openssh

RUN mkdir clonetemp
WORKDIR /clonetemp
RUN git clone https://github.com/cdc08x/MINERful.git minerful

FROM python:3.6

RUN mkdir gitpm
WORKDIR /gitpm
RUN mkdir server && \
    mkdir external && \
    cd external && \
    mkdir promAPI temp

RUN apt-get update && \
    apt-get install -y apt-utils && \
    apt-get install -y libsqlite3-dev

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && \
    apt-get clean;

RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

RUN pip install -U pip setuptools
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=intermediate ./clonetemp external/promAPI
COPY . ./server
WORKDIR /gitpm/server

ENTRYPOINT ["/bin/bash", "-c","source ./docker-entrypoint-server"]
