#!/usr/bin/env bash
# Lokální build a test image (stejně jako GitHub Actions, ale jen pro platformu tohoto
# počítače a bez pushe). Publikování na Docker Hub dělá .github/workflows/docker.yml.
#
# Použití: ./build.sh                    # podporované verze (ne eol)
#          ./build.sh all                # všechny image
#          ./build.sh 8.6-fpm-alpine ... # vybrané tagy
set -euo pipefail

cd "$(dirname "$0")"

./generate.py > /dev/null

images=$(./generate.py --list)
case "${1:-}" in
	"")  mapfile -t tags < <(jq -r '.[] | select(.eol | not) | .tag' <<<"$images") ;;
	all) mapfile -t tags < <(jq -r '.[].tag' <<<"$images") ;;
	*)   tags=("$@") ;;
esac

for tag in "${tags[@]}"; do
	[ -f "php/$tag/Dockerfile" ] || { echo "Neznámý tag $tag (viz ./generate.py --list)" >&2; exit 1; }

	echo "==> vspoint/php:$tag"
	docker buildx build --pull --load -t "vspoint/php:$tag" "php/$tag"
	docker run --rm "vspoint/php:$tag" sh -c 'php -v && php -m && composer --version'
done
