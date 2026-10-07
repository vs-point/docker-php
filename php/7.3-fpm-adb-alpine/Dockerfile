# VYGENEROVÁNO skriptem generate.py z versions.json - needitovat ručně!
# vspoint/php:7.3-fpm-adb-alpine

FROM php:7.3-fpm-alpine

RUN apk add --no-cache \
		android-tools \
		curl \
		git \
		perl-image-exiftool \
		unzip \
		zip

RUN set -eux \
	&& apk add --no-cache --virtual .build-deps \
		$PHPIZE_DEPS \
		pax-utils \
		cyrus-sasl-dev \
		freetype-dev \
		gmp-dev \
		icu-dev \
		libjpeg-turbo-dev \
		libmemcached-dev \
		libpng-dev \
		libssh2-dev \
		libwebp-dev \
		libxml2-dev \
		libzip-dev \
		linux-headers \
		mosquitto-dev \
		postgresql-dev \
		rabbitmq-c-dev \
		zlib-dev \
	&& docker-php-source extract \
	&& mkdir -p /usr/src/php/ext/amqp /usr/src/php/ext/ds /usr/src/php/ext/memcache /usr/src/php/ext/memcached /usr/src/php/ext/mosquitto /usr/src/php/ext/redis /usr/src/php/ext/ssh2 /usr/src/php/ext/xdebug \
	&& curl -fsSL "https://pecl.php.net/get/amqp-1.10.2.tgz" \
		| tar -xz -C /usr/src/php/ext/amqp --strip-components=1 \
	&& curl -fsSL "https://pecl.php.net/get/ds-1.3.0.tgz" \
		| tar -xz -C /usr/src/php/ext/ds --strip-components=1 \
	&& curl -fsSL "https://pecl.php.net/get/memcache-4.0.5.2.tgz" \
		| tar -xz -C /usr/src/php/ext/memcache --strip-components=1 \
	&& curl -fsSL "https://pecl.php.net/get/memcached-3.1.5.tgz" \
		| tar -xz -C /usr/src/php/ext/memcached --strip-components=1 \
	&& curl -fsSL "https://pecl.php.net/get/Mosquitto-0.4.0.tgz" \
		| tar -xz -C /usr/src/php/ext/mosquitto --strip-components=1 \
	&& curl -fsSL "https://pecl.php.net/get/redis-5.3.2.tgz" \
		| tar -xz -C /usr/src/php/ext/redis --strip-components=1 \
	&& curl -fsSL "https://pecl.php.net/get/ssh2-1.2.tgz" \
		| tar -xz -C /usr/src/php/ext/ssh2 --strip-components=1 \
	&& curl -fsSL "https://pecl.php.net/get/xdebug-2.7.0.tgz" \
		| tar -xz -C /usr/src/php/ext/xdebug --strip-components=1 \
	&& docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ --with-png-dir=/usr/include/ --with-webp-dir=/usr/include/ \
	&& docker-php-ext-install -j"$(nproc)" \
			amqp \
			bcmath \
			ds \
			gd \
			gmp \
			intl \
			memcache \
			memcached \
			mosquitto \
			pdo_mysql \
			pdo_pgsql \
			pgsql \
			redis \
			soap \
			ssh2 \
			xdebug \
			zip \
	&& docker-php-source delete \
	&& runDeps="$( \
		scanelf --needed --nobanner --format '%n#p' --recursive /usr/local/lib/php/extensions \
			| tr ',' '\n' \
			| sort -u \
			| awk 'system("[ -e /usr/local/lib/" $1 " ]") == 0 { next } { print "so:" $1 }' \
	)" \
	&& apk add --no-cache --virtual .php-ext-rundeps $runDeps \
	&& apk del .build-deps \
	&& rm -rf /tmp/* \
	&& php -m

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer
RUN ln -sf /usr/bin/composer /usr/local/bin/composer

RUN cp "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"

WORKDIR /usr/local/app
