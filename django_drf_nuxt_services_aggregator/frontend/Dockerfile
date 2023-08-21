FROM node:14.16.0-alpine
RUN mkdir -p /app
COPY . /app
WORKDIR /app

RUN apk update && apk upgrade && apk add git

COPY package.json /app
# COPY package-lock.json /app
#RUN npm rebuild
RUN npm cache clear --force
RUN npm install -g npm
RUN npm install --save core-js@^3

ENV NODE_ENV=production

COPY . /app
RUN npm run build

ENV HOST 0.0.0.0
EXPOSE 3000
