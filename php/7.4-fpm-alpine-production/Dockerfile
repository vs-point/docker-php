FROM php:7.4-fpm-alpine

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
		gmp-dev \
		libmemcached-dev \
		rabbitmq-c-dev \
		libssh2 \
		libssh2-dev \
		mosquitto-dev

ENV LD_PRELOAD /usr/lib/preloadable_libiconv.so php

RUN pecl install ds \
	&& pecl install redis-5.0.0 \
	&& pecl install Mosquitto-0.4.0 \
#	&& pecl install memcache \
	&& pecl install memcached-3.1.5 \
	&& pecl install amqp-1.10.2 \
	&& pecl install ssh2-1.2 \
	&& echo "extension=ssh2.so" >> /usr/local/etc/php/conf.d/docker-php-ext-ssh2.ini \
	&& docker-php-ext-enable \
		ds \
		redis \
		mosquitto \
#		memcache \
		memcached \
		amqp \
	&& docker-php-ext-install \
		bcmath \
		gd \
		intl \
		pdo \
		pdo_mysql \
		pdo_pgsql \
		pgsql \
		gmp \
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

RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

WORKDIR /usr/local/app
