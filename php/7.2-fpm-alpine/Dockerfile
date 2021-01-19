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
		gmp-dev \
		libmemcached-dev \
		rabbitmq-c-dev \
		libssh2 \
		libssh2-dev \
		mosquitto-dev \
		perl-image-exiftool \
        	jpeg-dev \
        	freetype \
        	freetype-dev \
       	libjpeg-turbo-dev \
       	libwebp \
       	libwebp-dev

ENV LD_PRELOAD /usr/lib/preloadable_libiconv.so php

RUN docker-php-ext-configure gd \
        --with-freetype-dir=/usr/lib/ \
        --with-png-dir=/usr/lib/ \
        --with-jpeg-dir=/usr/lib/ \
        --with-webp-dir=/usr/lib/ \
        --with-gd

RUN pecl install ds \
	&& pecl install redis-5.3.2 \
	&& pecl install xdebug-2.7.0 \
	&& pecl install Mosquitto-0.4.0 \
	&& pecl install memcache-4.0.5.2 \
	&& pecl install memcached-3.1.5 \
	&& pecl install amqp-1.10.2 \
	&& pecl install ssh2-1.2 \
	&& echo "extension=ssh2.so" >> /usr/local/etc/php/conf.d/docker-php-ext-ssh2.ini \
	&& docker-php-ext-enable \
		ds \
		redis \
		xdebug \
		mosquitto \
		memcache \
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
	&& composer self-update --snapshot

RUN apk del \
		autoconf \
		g++ \
		libtool \
		make \
	&& rm -rf /var/cache/apk/* \
	&& rm -rf /tmp/*

RUN mv "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"

WORKDIR /usr/local/app
