FROM node:8.12-jessie as builder
WORKDIR /gitpmclient
COPY package.json .
RUN yarn install
COPY . .

FROM nginx
COPY --from=builder /gitpmclient /usr/share/nginx/html
RUN apt-get update && apt-get install -y \
    automake \
    apt-utils \
    build-essential \
    curl \
    git \
    libcurl3 \
 && rm -rf /var/lib/apt/lists/
# Node installation
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
    apt-get update && \
    apt-get install -y python-pip nodejs libfontconfig && \
    rm -rf /var/lib/apt/lists/*
RUN npm install -g yarn
WORKDIR /usr/share/nginx/html
EXPOSE 4200
CMD ng serve --port 4200 --host 0.0.0.0 --poll 1
ENTRYPOINT ["/bin/bash", "./docker-entrypoint-dev"]
