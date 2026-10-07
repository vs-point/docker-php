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
- `.github/workflows/docker.yml` – postaví všechny image nativně na amd64 i arm64, otestuje je
  a pushne na Docker Hub. Spouští se při pushi do `master`, automaticky 1. den v měsíci
  (načisto bez cache, aby se natáhla nejnovější patch verze PHP a bezpečnostní opravy) a ručně
  přes Actions → Docker → Run workflow. Pull requesty se jen staví a testují.
- `build.sh` – lokální build a test (bez pushe), např. `./build.sh 8.6`.

## Napojení na Docker Hub

1. Na https://app.docker.com/accounts/vitek499/settings/personal-access-tokens → **Generate new token**,
   access permissions **Read & Write** (účet musí mít právo zápisu do organizace `vspoint`).
2. V GitHubu Settings → Secrets and variables → Actions nastav secrets
   `DOCKERHUB_USERNAME` (Docker Hub uživatel) a `DOCKERHUB_TOKEN` (vygenerovaný token),
   nebo z terminálu `gh secret set DOCKERHUB_TOKEN -R vs-point/docker-php`.

Nová verze PHP = nová položka ve `versions.json`.

Adresáře `php/5.6-*` až `php/8.0-*` jsou staré, už se nestaví.
