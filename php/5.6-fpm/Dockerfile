# VYGENEROVÁNO skriptem generate.py z versions.json - needitovat ručně!
# vspoint/php:5.6-fpm

FROM php:5.6-fpm

RUN set -eux \
	&& apt_install() { apt-get update && apt-get install -y --no-install-recommends "$@"; } \
	&& if ! apt_install \
		curl \
		git \
		libimage-exiftool-perl \
		unzip \
		zip; \
	then \
		sed -i -e 's|deb.debian.org|archive.debian.org|g' -e 's|security.debian.org|archive.debian.org|g' -e '/-updates/d' /etc/apt/sources.list; \
		printf '%s\n' 'Acquire::Check-Valid-Until "false";' 'Acquire::AllowInsecureRepositories "true";' 'APT::Get::AllowUnauthenticated "true";' > /etc/apt/apt.conf.d/99archive; \
		apt_install \
		curl \
		git \
		libimage-exiftool-perl \
		unzip \
		zip; \
	fi \
	&& rm -rf /var/lib/apt/lists/*

RUN set -eux \
	&& savedAptMark="$(apt-mark showmanual)" \
	&& apt-get update \
	&& apt-get install -y --no-install-recommends \
		libfreetype6-dev \
		libgmp-dev \
		libicu-dev \
		libjpeg-dev \
		libmemcached-dev \
		libmosquitto-dev \
		libpng-dev \
		libpq-dev \
		librabbitmq-dev \
		libwebp-dev \
		libzip-dev \
		zlib1g-dev \
	&& docker-php-source extract \
	&& mkdir -p /usr/src/php/ext/amqp /usr/src/php/ext/memcache /usr/src/php/ext/memcached /usr/src/php/ext/mosquitto /usr/src/php/ext/redis \
	&& curl -fsSL "https://pecl.php.net/get/amqp-1.10.2.tgz" \
		| tar -xz -C /usr/src/php/ext/amqp --strip-components=1 \
	&& curl -fsSL "https://pecl.php.net/get/memcache-3.0.8.tgz" \
		| tar -xz -C /usr/src/php/ext/memcache --strip-components=1 \
	&& curl -fsSL "https://pecl.php.net/get/memcached-2.2.0.tgz" \
		| tar -xz -C /usr/src/php/ext/memcached --strip-components=1 \
	&& curl -fsSL "https://pecl.php.net/get/Mosquitto-0.4.0.tgz" \
		| tar -xz -C /usr/src/php/ext/mosquitto --strip-components=1 \
	&& curl -fsSL "https://pecl.php.net/get/redis-4.2.0.tgz" \
		| tar -xz -C /usr/src/php/ext/redis --strip-components=1 \
	&& { [ -e /usr/include/gmp.h ] || ln -s "/usr/include/$(dpkg-architecture -qDEB_HOST_MULTIARCH)/gmp.h" /usr/include/gmp.h; } \
	&& docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ --with-png-dir=/usr/include/ \
	&& docker-php-ext-install -j"$(nproc)" \
			amqp \
			bcmath \
			gd \
			gmp \
			intl \
			memcache \
			memcached \
			mosquitto \
			mysqli \
			pdo_mysql \
			pdo_pgsql \
			pgsql \
			redis \
			zip \
	&& docker-php-source delete \
	&& apt-mark auto '.*' > /dev/null \
	&& { [ -z "$savedAptMark" ] || apt-mark manual $savedAptMark > /dev/null; } \
	&& find /usr/local -type f -name '*.so' -exec ldd '{}' ';' \
		| awk '/=>/ { so = $(NF-1); if (index(so, "/usr/local/") == 1) { next }; gsub("^/(usr/)?", "", so); printf "*%s\n", so }' \
		| sort -u \
		| xargs -r dpkg-query --search \
		| cut -d: -f1 \
		| sort -u \
		| xargs -r apt-mark manual \
	&& apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
	&& rm -rf /var/lib/apt/lists/* \
	&& rm -rf /tmp/* \
	&& php -m

COPY --from=composer:2.2 /usr/bin/composer /usr/bin/composer
RUN ln -sf /usr/bin/composer /usr/local/bin/composer

RUN cp "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"

WORKDIR /usr/local/app
