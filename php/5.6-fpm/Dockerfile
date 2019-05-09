FROM php:5.6-fpm

RUN apt-get update \
	&& apt-get install -y \
		git \
		zip \
		unzip \
		libpng-dev \
		libpq-dev \
		libicu-dev \
		libzip-dev \
		libmosquitto-dev \
	&& pecl install redis-4.2.0 \
	&& pecl install Mosquitto-alpha \
	&& docker-php-ext-configure \
		pgsql -with-pgsql=/usr/local/pgsql \
	&& docker-php-ext-enable \
		redis \
		mosquitto \
	&& docker-php-ext-install \
		bcmath \
		gd \
		intl \
		pdo \
		mysqli \
		pdo_mysql \
		pdo_pgsql \
		pgsql \
		zip \
	&& curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
	&& composer global require "hirak/prestissimo:^0.3" \
	&& apt-get clean -y \
	&& apt-get autoclean -y \
	&& apt-get autoremove -y \
	&& rm -rf /var/lib/apt/lists/* /var/lib/log/* /tmp/* /var/tmp/*

RUN mv "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"

WORKDIR /usr/local/app
