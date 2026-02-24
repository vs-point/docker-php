FROM php:8.5-fpm-alpine

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
        --enable-gd \
        --with-freetype \
        --with-jpeg \
        --with-webp
        
RUN pecl install ds-1.6.0 \
	&& pecl install redis-6.3.0 \	
	&& pecl install xdebug-3.5.0 \
#	&& pecl install Mosquitto-0.4.0 \
	&& pecl install memcache-8.2 \
#	&& pecl install memcached-3.4.0 \
#	&& pecl install amqp-2.2.0 \
#	&& pecl install ssh2-1.4.1 \
#	&& echo "extension=ssh2.so" >> /usr/local/etc/php/conf.d/docker-php-ext-ssh2.ini \
	&& docker-php-ext-enable \
		ds \
		redis \
		xdebug \
#		mosquitto \
		memcache \
#		memcached \
#		amqp \
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
		exif \
		gd \
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

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer


WORKDIR /usr/local/app
