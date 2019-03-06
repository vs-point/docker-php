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
	&& pecl install ds \
	&& pecl install redis-4.2.0 \
	&& pecl install xdebug-2.7.0 \
	&& docker-php-ext-configure \
		pgsql -with-pgsql=/usr/local/pgsql \
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
	&& apt-get clean -y \
	&& apt-get autoclean -y \
	&& apt-get autoremove -y \
	&& rm -rf /var/lib/apt/lists/* /var/lib/log/* /tmp/* /var/tmp/*

WORKDIR /usr/local/app
