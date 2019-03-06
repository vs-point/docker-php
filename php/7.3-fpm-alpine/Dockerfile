FROM php:7.3-fpm-alpine

RUN apk update \
	&& apk add --no-cache \
		autoconf \
		curl \
		g++ \
		git \
		icu-dev \
		libpng-dev \
		libtool \
		libzip-dev \
		make \
		postgresql-dev \
		unzip \
		zip \
	&& pecl install ds \
	&& pecl install redis-4.2.0 \
	&& pecl install xdebug-2.7.0 \
	&& docker-php-ext-enable \
		ds \
		redis \
		xdebug \
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
	&& composer global require "hirak/prestissimo:^0.3" \
	&& apk del \
		autoconf \
		g++ \
		libtool \
		make \
	&& rm -rf /var/cache/apk/* \
	&& rm -rf /tmp/*

WORKDIR /usr/local/app
