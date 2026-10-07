# VYGENEROVÁNO skriptem generate.py z versions.json - needitovat ručně!
# vspoint/php:8.6-fpm-alpine

FROM php:8.6-rc-fpm-alpine

RUN apk add --no-cache \
		curl \
		git \
		icu-data-full \
		perl-image-exiftool \
		unzip \
		zip

COPY patch-ds.sh /usr/local/bin/patch-ds.sh

RUN set -eux \
	&& apk add --no-cache --virtual .build-deps \
		$PHPIZE_DEPS \
		pax-utils \
		freetype-dev \
		gmp-dev \
		icu-dev \
		libjpeg-turbo-dev \
		libpng-dev \
		libwebp-dev \
		libzip-dev \
		linux-headers \
		postgresql-dev \
		zlib-dev \
	&& docker-php-source extract \
	&& mkdir -p /usr/src/php/ext/ds /usr/src/php/ext/redis /usr/src/php/ext/xdebug \
	&& curl -fsSL "https://pecl.php.net/get/ds-1.6.0.tgz" \
		| tar -xz -C /usr/src/php/ext/ds --strip-components=1 \
	&& curl -fsSL "https://github.com/phpredis/phpredis/archive/57b584f676a504842d86c4dafb6b8f9abaf21ba2.tar.gz" \
		| tar -xz -C /usr/src/php/ext/redis --strip-components=1 \
	&& curl -fsSL "https://github.com/xdebug/xdebug/archive/3.6.0alpha1.tar.gz" \
		| tar -xz -C /usr/src/php/ext/xdebug --strip-components=1 \
	&& /usr/local/bin/patch-ds.sh \
	&& docker-php-ext-configure gd --with-freetype --with-jpeg --with-webp \
	&& docker-php-ext-install -j"$(nproc)" \
			bcmath \
			ds \
			exif \
			gd \
			gmp \
			intl \
			pdo_mysql \
			pdo_pgsql \
			pgsql \
			redis \
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
	&& rm -rf /tmp/* /usr/local/bin/patch-ds.sh \
	&& php -m

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer
RUN ln -sf /usr/bin/composer /usr/local/bin/composer

RUN cp "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"

WORKDIR /usr/local/app
