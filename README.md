# vspoint/php

PHP-FPM image na Alpine pro `linux/amd64` i `linux/arm64` (Apple Silicon).

| Tag                                   | php.ini     | Xdebug |
|---------------------------------------|-------------|--------|
| `vspoint/php:8.5-fpm-alpine`          | development | ano    |
| `vspoint/php:8.5-fpm-alpine-production` | production  | ne     |
| `vspoint/php:8.6-fpm-alpine`          | development | ano    |
| `vspoint/php:8.6-fpm-alpine-production` | production  | ne     |

Rozšíření: bcmath, ds, exif, gd (freetype, jpeg, webp), gmp, intl (plná ICU data), pdo_mysql,
pdo_pgsql, pgsql, redis, zip. Dále composer 2, git, curl, zip/unzip a exiftool.

## Jak to funguje

- `php/fpm-alpine/Dockerfile` – jeden Dockerfile pro všechny verze, targety `production` a `development`.
- `versions.json` – verze PHP a připnuté verze (git ref) rozšíření ds, redis a xdebug.
- `.github/workflows/docker.yml` – při pushi do `master`, každé pondělí a ručně (Run workflow)
  postaví všechny image nativně na amd64 i arm64, otestuje je a pushne na Docker Hub.
  Pull requesty se jen staví a testují.
  Potřebuje v repozitáři secrets `DOCKERHUB_USERNAME` a `DOCKERHUB_TOKEN`.
- `build.sh` – lokální build a test (bez pushe), např. `./build.sh 8.6`.

Nová verze PHP = nová položka ve `versions.json`.

Adresáře `php/5.6-*` až `php/8.0-*` jsou staré, už se nestaví.
