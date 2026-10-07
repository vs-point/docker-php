#!/bin/sh
# Úprava zdrojáků ext-ds 1.x pro PHP 8.6+.
#
# PHP 8.6 odstranilo makro XtOffsetOf a funkci zend_parse_parameter(). Upstream to opravil
# jen ve větvi 2.0 (BC break), viz https://github.com/php-ds/ext-ds/pull/230, takže pro 1.x
# provedeme stejnou úpravu tady. Patch se aplikuje jen pokud ho dané PHP potřebuje.
set -eu

src="${1:-/usr/src/php/ext/ds}"
zend=/usr/local/include/php/Zend

if ! grep -q 'define XtOffsetOf' "$zend/zend_portability.h"; then
	echo "patch-ds: XtOffsetOf -> offsetof"
	grep -rl XtOffsetOf "$src" | xargs -r sed -i 's/XtOffsetOf/offsetof/g'
fi

if ! grep -q 'zend_parse_parameter(' "$zend/zend_API.h"; then
	echo "patch-ds: zend_parse_parameter -> zend_parse_arg_long"
	for f in "$src/src/php/handlers/php_vector_handlers.c" "$src/src/php/handlers/php_deque_handlers.c"; do
		perl -0pi -e 's/zend_parse_parameter\(ZEND_PARSE_PARAMS_QUIET, 1, offset, "l", &index\) == FAILURE/!zend_parse_arg_long(offset, &index, NULL, false, 1)/g' "$f"
	done
	if grep -rq 'zend_parse_parameter(' "$src/src"; then
		echo "patch-ds: zbylo volání zend_parse_parameter()" >&2
		exit 1
	fi
fi
