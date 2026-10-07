# vspoint/php

PHP-FPM image pro `linux/amd64` i `linux/arm64` (Apple Silicon).

| Tag | Základ | Podpora |
|-----|--------|---------|
| `8.6-fpm-alpine`, `8.6-fpm-alpine-production` | `php:8.6-rc-fpm-alpine` | ano (RC) |
| `8.5-fpm-alpine`, `8.5-fpm-alpine-production` | `php:8.5-fpm-alpine` | ano |
| `8.0-fpm-alpine`, `8.0-fpm-alpine-production` | `php:8.0-fpm-alpine` | eol |
| `7.4-fpm-alpine`, `7.4-fpm-alpine-production` | `php:7.4-fpm-alpine` | eol |
| `7.3-fpm-alpine`, `7.3-fpm-alpine-production`, `7.3-fpm-adb-alpine` | `php:7.3-fpm-alpine` | eol |
| `7.3-fpm`, `7.3-fpm-production` | `php:7.3-fpm` (Debian) | eol |
| `7.2-fpm-alpine`, `7.2-fpm` | `php:7.2-fpm(-alpine)` | eol |
| `7.1-fpm-alpine` | `php:7.1-fpm-alpine` | eol |
| `5.6-fpm-alpine`, `5.6-fpm` | `php:5.6-fpm(-alpine)` | eol |

Varianty:
- bez přípony – `php.ini-development` + xdebug
- `-production` – `php.ini-production` + opcache, bez xdebugu
- `-adb` – jako development + `adb` (android-tools)

Rozšíření jednotlivých tagů vypíše `./generate.py --list`. Ve všech je navíc composer 2,
git, curl, zip/unzip a exiftool.

## Jak to funguje

- `versions.json` – jediné místo, kde se mění verze PHP, varianty a rozšíření (a jejich verze).
- `generate.py` – z `versions.json` vygeneruje `php/<tag>/Dockerfile`. Ty se needitují ručně;
  po změně `versions.json` spusť `./generate.py` a commitni i vygenerované soubory.
  Popis všech položek je na začátku `generate.py`.
- `.github/workflows/docker.yml` – postaví image nativně na amd64 i arm64, otestuje je
  a pushne na Docker Hub:
  - po pushi do `master` ty image, jejichž Dockerfile se změnil,
  - automaticky 1. den v měsíci podporované (ne `eol`) verze načisto bez cache,
    aby měly nejnovější patch verzi PHP a bezpečnostní opravy,
  - ručně přes Actions → Docker → Run workflow (prázdné = podporované, `all` = vše,
    nebo konkrétní tagy).

  Pull requesty se jen staví a testují.
- `build.sh` – lokální build a test bez pushe, např. `./build.sh 8.6-fpm-alpine`.
- `patch-ds.sh` – úprava rozšíření ds 1.x pro PHP 8.6.

Nová verze PHP = nová položka ve `versions.json` + `./generate.py`.
