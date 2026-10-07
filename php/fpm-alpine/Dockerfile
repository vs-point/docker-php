# Společný Dockerfile pro vspoint/php:<verze>-fpm-alpine(-production).
#
# Targety:
#   production  -> vspoint/php:<verze>-fpm-alpine-production (php.ini-production, bez xdebugu)
#   development -> vspoint/php:<verze>-fpm-alpine            (php.ini-development + xdebug), výchozí
#
# Verze PHP a rozšíření se předávají přes build-args (viz .github/workflows/docker.yml a build.sh).

ARG PHP_IMAGE=php:8.5-fpm-alpine

FROM ${PHP_IMAGE} AS base

# Git ref (tag nebo commit) rozšíření na GitHubu
ARG DS_VERSION=v1.6.0
ARG REDIS_VERSION=6.3.0

# Nástroje dostupné i v běžícím kontejneru
RUN apk add --no-cache \
		curl \
		git \
		icu-data-full \
		perl-image-exiftool \
		unzip \
		zip

COPY patch-ds.sh /usr/local/bin/patch-ds.sh

# PECL rozšíření se stahují jako zdrojáky z GitHubu a staví přes docker-php-ext-install,
# protože od PHP 8.6 už oficiální image neobsahuje pecl/PEAR. Zároveň tak jde použít
# i commit, který ještě není vydaný na PECL.
RUN set -eux \
	&& apk add --no-cache --virtual .build-deps \
		$PHPIZE_DEPS \
		freetype-dev \
		gmp-dev \
		icu-dev \
		libjpeg-turbo-dev \
		libpng-dev \
		libwebp-dev \
		libzip-dev \
		linux-headers \
		postgresql-dev \
	&& docker-php-source extract \
	&& mkdir -p /usr/src/php/ext/ds /usr/src/php/ext/redis \
	&& curl -fsSL "https://github.com/php-ds/ext-ds/archive/${DS_VERSION}.tar.gz" \
		| tar -xz -C /usr/src/php/ext/ds --strip-components=1 \
	&& curl -fsSL "https://github.com/phpredis/phpredis/archive/${REDIS_VERSION}.tar.gz" \
		| tar -xz -C /usr/src/php/ext/redis --strip-components=1 \
	&& /usr/local/bin/patch-ds.sh /usr/src/php/ext/ds \
	&& docker-php-ext-configure gd \
		--with-freetype \
		--with-jpeg \
		--with-webp \
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
		zip \
	&& docker-php-source delete \
	&& runDeps="$( \
		scanelf --needed --nobanner --format '%n#p' --recursive /usr/local/lib/php/extensions \
			| tr ',' '\n' \
			| sort -u \
			| awk 'system("[ -e /usr/local/lib/" $1 " ]") == 0 { next } { print "so:" $1 }' \
	)" \
	&& apk add --no-cache --virtual .php-ext-rundeps $runDeps \
	&& apk del --no-network .build-deps \
	&& rm -rf /tmp/* /usr/local/bin/patch-ds.sh \
	&& php -m

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer
RUN ln -s /usr/bin/composer /usr/local/bin/composer

WORKDIR /usr/local/app


FROM base AS production

RUN cp "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"


FROM base AS development

# Git ref (tag nebo commit) Xdebugu na GitHubu
ARG XDEBUG_VERSION=3.5.3

RUN set -eux \
	&& apk add --no-cache --virtual .build-deps $PHPIZE_DEPS linux-headers \
	&& docker-php-source extract \
	&& mkdir -p /usr/src/php/ext/xdebug \
	&& curl -fsSL "https://github.com/xdebug/xdebug/archive/${XDEBUG_VERSION}.tar.gz" \
		| tar -xz -C /usr/src/php/ext/xdebug --strip-components=1 \
	&& docker-php-ext-install -j"$(nproc)" xdebug \
	&& docker-php-source delete \
	&& apk del --no-network .build-deps \
	&& rm -rf /tmp/* \
	&& php -m | grep -qi xdebug

RUN cp "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"
