FROM php:7.3-fpm

RUN apt-get update \
	&& apt-get install -y \
		git \
		zip \
		unzip \
		libpng-dev \
		libpq-dev \
		libicu-dev \
		libzip-dev \
		libgmp-dev \
		libmemcached-dev \
		libmosquitto-dev \
		librabbitmq-dev \
	&& ln -s /usr/include/x86_64-linux-gnu/gmp.h /usr/include/gmp.h \
	&& pecl install ds-1.3.0 \
	&& pecl install redis-4.2.0 \
	&& pecl install Mosquitto-alpha \
#	&& pecl install memcache \
	&& pecl install memcached \
	&& pecl install amqp \
	&& docker-php-ext-configure \
		pgsql -with-pgsql=/usr/local/pgsql \
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
		opcache \
		pdo \
		pdo_mysql \
		pdo_pgsql \
		pgsql \
		gmp \
		zip \
	&& curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
	&& composer global require "hirak/prestissimo:^0.3" \
	&& apt-get clean -y \
	&& apt-get autoclean -y \
	&& apt-get autoremove -y \
	&& rm -rf /var/lib/apt/lists/* /var/lib/log/* /tmp/* /var/tmp/*

RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

WORKDIR /usr/local/app
