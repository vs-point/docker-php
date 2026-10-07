#!/usr/bin/env bash
# Lokální build a test image podle versions.json (stejně jako GitHub Actions, ale jen pro
# platformu tohoto počítače a bez pushe). Publikování na Docker Hub dělá
# .github/workflows/docker.yml.
#
# Použití: ./build.sh            # všechny verze
#          ./build.sh 8.6        # jen vybrané verze
set -euo pipefail

cd "$(dirname "$0")"

versions=("$@")
if [ ${#versions[@]} -eq 0 ]; then
	mapfile -t versions < <(jq -r '.[].php' versions.json)
fi

for php in "${versions[@]}"; do
	cfg=$(jq -ec --arg php "$php" '.[] | select(.php == $php)' versions.json) || {
		echo "Verze $php není ve versions.json" >&2
		exit 1
	}

	for target in development production; do
		tag="vspoint/php:${php}-fpm-alpine"
		[ "$target" = production ] && tag+="-production"

		echo "==> $tag"
		docker buildx build \
			--pull \
			--load \
			--target "$target" \
			--build-arg PHP_IMAGE="$(jq -r .image <<<"$cfg")" \
			--build-arg DS_VERSION="$(jq -r .ds <<<"$cfg")" \
			--build-arg REDIS_VERSION="$(jq -r .redis <<<"$cfg")" \
			--build-arg XDEBUG_VERSION="$(jq -r .xdebug <<<"$cfg")" \
			-t "$tag" \
			php/fpm-alpine

		docker run --rm "$tag" sh -c 'php -v && php -m && composer --version'
	done
done
