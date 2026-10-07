#!/usr/bin/env python3
"""Vygeneruje php/<tag>/Dockerfile pro všechny image z versions.json.

Použití: ./generate.py          vygeneruje php/*/
         ./generate.py --list   vypíše seznam tagů jako JSON (pro GitHub Actions)

Ručně se needitují vygenerované Dockerfily, ale versions.json (verze, rozšíření)
nebo tento skript (jak se image staví). Po změně spusť ./generate.py a commitni i výstup.

Položka ve versions.json:
  php         verze PHP, např. "8.5"
  distro      "alpine" nebo "debian"
  image       základní image, např. "php:8.5-fpm-alpine"
  eol         true = verze bez podpory; plánovaný měsíční build ji přeskočí
  variants    "development" (php.ini-development + xdebug), "production" (php.ini-production
              + opcache), "adb" (development + android-tools)
  composer    tag image composer, ze kterého se kopíruje binárka ("2", pro PHP < 7.2.5 "2.2")
  packages    další balíčky distribuce navíc
  extensions  rozšíření ze zdrojáků PHP (docker-php-ext-install)
  pecl        PECL rozšíření: {"název": "verze z PECL" nebo "URL tarballu se zdrojáky"}
  xdebug      verze z PECL nebo URL tarballu (jen development a adb)
  patches     skripty z kořene repa, které se spustí nad zdrojáky rozšíření před buildem
"""

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "php"
HEADER = "# VYGENEROVÁNO skriptem generate.py z versions.json - needitovat ručně!"

# Název balíčku na PECL, pokud se liší od názvu rozšíření
PECL_NAMES = {"mosquitto": "Mosquitto"}

TOOLS = {
	"alpine": ["curl", "git", "perl-image-exiftool", "unzip", "zip"],
	"debian": ["curl", "git", "libimage-exiftool-perl", "unzip", "zip"],
}

# Knihovny potřebné ke kompilaci rozšíření (po buildu se smažou, runtime knihovny zůstanou)
BUILD_DEPS = {
	"alpine": {
		"amqp": ["rabbitmq-c-dev"],
		"gd": ["freetype-dev", "libjpeg-turbo-dev", "libpng-dev", "libwebp-dev"],
		"gmp": ["gmp-dev"],
		"intl": ["icu-dev"],
		"memcache": ["zlib-dev"],
		"memcached": ["cyrus-sasl-dev", "libmemcached-dev", "zlib-dev"],
		"mosquitto": ["mosquitto-dev"],
		"pdo_pgsql": ["postgresql-dev"],
		"pgsql": ["postgresql-dev"],
		"soap": ["libxml2-dev"],
		"ssh2": ["libssh2-dev"],
		"xdebug": ["linux-headers"],
		"zip": ["libzip-dev", "zlib-dev"],
	},
	"debian": {
		"amqp": ["librabbitmq-dev"],
		"gd": ["libfreetype6-dev", "libjpeg-dev", "libpng-dev", "libwebp-dev"],
		"gmp": ["libgmp-dev"],
		"intl": ["libicu-dev"],
		"memcache": ["zlib1g-dev"],
		"memcached": ["libmemcached-dev", "zlib1g-dev"],
		"mosquitto": ["libmosquitto-dev"],
		"pdo_pgsql": ["libpq-dev"],
		"pgsql": ["libpq-dev"],
		"soap": ["libxml2-dev"],
		"ssh2": ["libssh2-1-dev"],
		"zip": ["libzip-dev", "zlib1g-dev"],
	},
}


def ver(v):
	return tuple(int(x) for x in v.split("."))


def tag_name(e, variant):
	tag = f"{e['php']}-fpm"
	if variant == "adb":
		tag += "-adb"
	if e["distro"] == "alpine":
		tag += "-alpine"
	if variant == "production":
		tag += "-production"
	return tag


def source_url(name, value):
	if value.startswith("https://"):
		return value
	return f"https://pecl.php.net/get/{PECL_NAMES.get(name, name)}-{value}.tgz"


def gd_configure(php):
	if ver(php) >= (7, 4):
		return "--with-freetype --with-jpeg --with-webp"
	flags = "--with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ --with-png-dir=/usr/include/"
	if ver(php) >= (7, 0):
		flags += " --with-webp-dir=/usr/include/"
	return flags


def lines(items, indent="\t\t"):
	return " \\\n".join(f"{indent}{i}" for i in items)


def pecl_list(e, variant):
	pecl = dict(e.get("pecl", {}))
	if variant != "production" and e.get("xdebug"):
		pecl["xdebug"] = e["xdebug"]
	return pecl


def ext_list(e, variant):
	exts = set(e["extensions"]) | set(pecl_list(e, variant))
	if variant == "production" and ver(e["php"]) < (8, 5):
		exts.add("opcache")  # od 8.5 je opcache vždy součástí PHP
	return sorted(exts)


def render(e, variant):
	php, distro = e["php"], e["distro"]
	dev = variant != "production"
	pecl = pecl_list(e, variant)
	exts = ext_list(e, variant)

	deps = sorted({d for x in exts for d in BUILD_DEPS[distro].get(x, [])})
	tools = sorted(set(TOOLS[distro]) | set(e.get("packages", [])) | ({"android-tools"} if variant == "adb" else set()))

	steps = ["docker-php-source extract"]
	if pecl:
		steps.append("mkdir -p " + " ".join(f"/usr/src/php/ext/{n}" for n in sorted(pecl)))
		for n in sorted(pecl):
			steps.append(
				f'curl -fsSL "{source_url(n, pecl[n])}" \\\n'
				f"\t\t| tar -xz -C /usr/src/php/ext/{n} --strip-components=1"
			)
	for p in e.get("patches", []):
		steps.append(f"/usr/local/bin/{p}")
	if distro == "debian" and "gmp" in exts:
		steps.append(
			'{ [ -e /usr/include/gmp.h ] || ln -s "/usr/include/$(dpkg-architecture -qDEB_HOST_MULTIARCH)/gmp.h" /usr/include/gmp.h; }'
		)
	if "gd" in exts:
		steps.append(f"docker-php-ext-configure gd {gd_configure(php)}")
	steps.append(f'docker-php-ext-install -j"$(nproc)" \\\n{lines(exts, chr(9) * 3)}')
	steps.append("docker-php-source delete")

	out = [
		HEADER,
		f"# vspoint/php:{tag_name(e, variant)}",
		"",
		f"FROM {e['image']}",
		"",
	]

	if distro == "alpine":
		out += [
			"RUN apk add --no-cache \\",
			lines(tools),
			"",
		]
	else:
		# Staré Debiany (stretch, buster, ...) jsou už jen na archive.debian.org a jejich podpisové
		# klíče vypršely. Když instalace z běžných zrcadel selže, přepne se na archiv a podpisy
		# repozitáře se neověřují.
		out += [
			"RUN set -eux \\",
			"\t&& apt_install() { apt-get update && apt-get install -y --no-install-recommends \"$@\"; } \\",
			"\t&& if ! apt_install \\",
			lines(tools) + "; \\",
			"\tthen \\",
			"\t\tsed -i -e 's|deb.debian.org|archive.debian.org|g' -e 's|security.debian.org|archive.debian.org|g' -e '/-updates/d' /etc/apt/sources.list; \\",
			"\t\tprintf '%s\\n' 'Acquire::Check-Valid-Until \"false\";' 'Acquire::AllowInsecureRepositories \"true\";' 'APT::Get::AllowUnauthenticated \"true\";' > /etc/apt/apt.conf.d/99archive; \\",
			"\t\tapt_install \\",
			lines(tools) + "; \\",
			"\tfi \\",
			"\t&& rm -rf /var/lib/apt/lists/*",
			"",
		]

	for p in e.get("patches", []):
		out += [f"COPY {p} /usr/local/bin/{p}", ""]

	if distro == "alpine":
		out += [
			"RUN set -eux \\",
			"\t&& apk add --no-cache --virtual .build-deps \\",
			lines(["$PHPIZE_DEPS", "pax-utils"] + deps) + " \\",
			*[f"\t&& {s}" + " \\" for s in steps],
			"\t&& runDeps=\"$( \\",
			"\t\tscanelf --needed --nobanner --format '%n#p' --recursive /usr/local/lib/php/extensions \\",
			"\t\t\t| tr ',' '\\n' \\",
			"\t\t\t| sort -u \\",
			"\t\t\t| awk 'system(\"[ -e /usr/local/lib/\" $1 \" ]\") == 0 { next } { print \"so:\" $1 }' \\",
			"\t)\" \\",
			"\t&& apk add --no-cache --virtual .php-ext-rundeps $runDeps \\",
			"\t&& apk del .build-deps \\",
		]
	else:
		out += [
			"RUN set -eux \\",
			"\t&& savedAptMark=\"$(apt-mark showmanual)\" \\",
			"\t&& apt-get update \\",
			"\t&& apt-get install -y --no-install-recommends \\",
			lines(deps) + " \\",
			*[f"\t&& {s}" + " \\" for s in steps],
			"\t&& apt-mark auto '.*' > /dev/null \\",
			"\t&& { [ -z \"$savedAptMark\" ] || apt-mark manual $savedAptMark > /dev/null; } \\",
			"\t&& find /usr/local -type f -name '*.so' -exec ldd '{}' ';' \\",
			"\t\t| awk '/=>/ { so = $(NF-1); if (index(so, \"/usr/local/\") == 1) { next }; gsub(\"^/(usr/)?\", \"\", so); printf \"*%s\\n\", so }' \\",
			"\t\t| sort -u \\",
			"\t\t| xargs -r dpkg-query --search \\",
			"\t\t| cut -d: -f1 \\",
			"\t\t| sort -u \\",
			"\t\t| xargs -r apt-mark manual \\",
			"\t&& apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \\",
			"\t&& rm -rf /var/lib/apt/lists/* \\",
		]

	cleanup = ["/tmp/*"] + [f"/usr/local/bin/{p}" for p in e.get("patches", [])]
	out += [
		f"\t&& rm -rf {' '.join(cleanup)} \\",
		"\t&& php -m",
		"",
		f"COPY --from=composer:{e['composer']} /usr/bin/composer /usr/bin/composer",
		"RUN ln -sf /usr/bin/composer /usr/local/bin/composer",
		"",
		f'RUN cp "$PHP_INI_DIR/php.ini-{"development" if dev else "production"}" "$PHP_INI_DIR/php.ini"',
		"",
		"WORKDIR /usr/local/app",
		"",
	]
	return "\n".join(out)


def images(entries):
	"""Seznam image pro GitHub Actions: [{"tag": ..., "eol": ..., "extensions": ...}]"""
	return [
		{"tag": tag_name(e, v), "eol": bool(e.get("eol")), "extensions": " ".join(ext_list(e, v))}
		for e in entries
		for v in e["variants"]
	]


def main():
	entries = json.loads((ROOT / "versions.json").read_text())

	if "--list" in sys.argv:
		print(json.dumps(images(entries)))
		return

	# smazat dříve vygenerované adresáře (kvůli odebraným verzím)
	for f in OUT.glob("*/Dockerfile"):
		if f.read_text().startswith(HEADER):
			shutil.rmtree(f.parent)

	for e in entries:
		for variant in e["variants"]:
			tag = tag_name(e, variant)
			d = OUT / tag
			if d.exists():
				shutil.rmtree(d)
			d.mkdir(parents=True)
			(d / "Dockerfile").write_text(render(e, variant))
			for p in e.get("patches", []):
				shutil.copy2(ROOT / p, d / p)
			print(f"php/{tag}/Dockerfile")


if __name__ == "__main__":
	main()
