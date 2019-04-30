FROM php:7.2-fpm-alpine

RUN apk update \
	&& apk add --no-cache --allow-untrusted --repository http://dl-cdn.alpinelinux.org/alpine/edge/community/ \
		autoconf \
		curl \
		g++ \
		git \
		gnu-libiconv \
		icu-dev \
		libpng-dev \
		libtool \
		libzip-dev \
		make \
		postgresql-dev \
		unzip \
		zip \
		mosquitto-dev

ENV LD_PRELOAD /usr/lib/preloadable_libiconv.so php

RUN pecl install ds \
	&& pecl install redis-4.2.0 \
	&& pecl install xdebug-2.7.0 \
	&& pecl install Mosquitto-alpha \
	&& docker-php-ext-enable \
		ds \
		redis \
		xdebug \
		mosquitto \
	&& docker-php-ext-install \
		bcmath \
		gd \
		intl \
		pdo \
		pdo_mysql \
		pdo_pgsql \
		pgsql \
		zip \
	&& curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
	&& composer global require "hirak/prestissimo:^0.3"

RUN apk del \
		autoconf \
		g++ \
		libtool \
		make \
	&& rm -rf /var/cache/apk/* \
	&& rm -rf /tmp/*

RUN mv "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"

WORKDIR /usr/local/app
