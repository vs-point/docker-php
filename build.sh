#!/usr/bin/env bash

docker image rm php:5.6-fpm-alpine

docker build --no-cache -t vspoint/php:5.6-fpm-alpine php/5.6-fpm-alpine/.
docker push vspoint/php:5.6-fpm-alpine

docker build --no-cache -t vspoint/php:5.6-fpm-alpine-production php/5.6-fpm-alpine-production/.
docker push vspoint/php:5.6-fpm-alpine-production


docker image rm php:7.1-fpm-alpine
docker build --no-cache -t vspoint/php:7.1-fpm-alpine php/7.1-fpm-alpine/.
docker push vspoint/php:7.1-fpm-alpine

docker image rm php:7.2-fpm-alpine
docker build --no-cache -t vspoint/php:7.2-fpm-alpine php/7.2-fpm-alpine/.
docker push vspoint/php:7.2-fpm-alpine


docker image rm php:7.3-fpm-alpine

docker build --no-cache -t vspoint/php:7.3-fpm-alpine php/7.3-fpm-alpine/.
docker push vspoint/php:7.3-fpm-alpine

docker build --no-cache -t vspoint/php:7.3-fpm-alpine-production php/7.3-fpm-alpine-production/.
docker push vspoint/php:7.3-fpm-alpine-production


docker image rm php:7.4-fpm-alpine

docker build --no-cache -t vspoint/php:7.4-fpm-alpine php/7.4-fpm-alpine/.
docker push vspoint/php:7.4-fpm-alpine

docker build --no-cache -t vspoint/php:7.4-fpm-alpine-production php/7.4-fpm-alpine-production/.
docker push vspoint/php:7.4-fpm-alpine-production


docker image rm php:8.0-fpm-alpine

docker build --no-cache -t vspoint/php:8.0-fpm-alpine php/8.0-fpm-alpine/.
docker push vspoint/php:8.0-fpm-alpine

docker build --no-cache -t vspoint/php:8.0-fpm-alpine-production php/8.0-fpm-alpine-production/.
docker push vspoint/php:8.0-fpm-alpine-production
