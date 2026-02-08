---
title: PHP Source Code Appreciation ~ First Set of Broadcast Exercises (string篇)
date: 2018-05-01
description: 'PHP Source Code Appreciation ~ First Set of Broadcast Exercises (string篇) Seek the Root Recently when seeing some PHP functions, kept thinking, how are they implemented behind the scenes? If not carefully digging into their details, prone to misuse. And feels like using a black box. Can't tell when a snake might pop out inside. So, found source code, pondered the underlying implementation logic.'
tags: [PHP]
categories:
---

[](#PHP-Source-Code-Appreciation-~-First-Set-of-Broadcast-Exercises-string-篇)PHP Source Code Appreciation ~ First Set of Broadcast Exercises (string篇)[](#Seek-the-Root)Seek the Root
Recently when seeing some PHP functions, kept thinking, how are they implemented behind the scenes? If not carefully digging into their details, prone to misuse. And feels like using a black box. Can't tell when a snake might pop out inside. So, found source code, pondered the underlying implementation logic.

[](#First-Section-Stretching-Exercise-strpos)First Section: Stretching Exercise [strpos](https://github.com/php/php-src/blob/master/ext/standard/string.c)
First let's show its entire implementation appearance, looks beautiful as a flower:

[](#strpos-Source-Code)strpos Source Code1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
PHP_FUNCTION(strpos)
{
	zval *needle;
	zend_string *haystack;
	char *found = NULL;
	char  needle_char[2];
	zend_long  offset = 0;

	ZEND_PARSE_PARAMETERS_START(2, 3)
		Z_PARAM_STR(haystack)
		Z_PARAM_ZVAL(needle)
		Z_PARAM_OPTIONAL
		Z_PARAM_LONG(offset)
	ZEND_PARSE_PARAMETERS_END();

	if (offset < 0) {
		offset += (zend_long)ZSTR_LEN(haystack);
	}
	if (offset < 0 || (size_t)offset > ZSTR_LEN(haystack)) {
		php_error_docref(NULL, E_WARNING, "Offset not contained in string");
		RETURN_FALSE;
	}

	if (Z_TYPE_P(needle) == IS_STRING) {
		if (!Z_STRLEN_P(needle)) {
			php_error_docref(NULL, E_WARNING, "Empty needle");
			RETURN_FALSE;
		}

		found = (char*)php_memnstr(ZSTR_VAL(haystack) + offset,
		                Z_STRVAL_P(needle),
		                Z_STRLEN_P(needle),
		                ZSTR_VAL(haystack) + ZSTR_LEN(haystack));
	} else {
		if (php_needle_char(needle, needle_char) != SUCCESS) {
			RETURN_FALSE;
		}
		needle_char[1] = 0;

		found = (char*)php_memnstr(ZSTR_VAL(haystack) + offset,
						needle_char,
						1,
	                    ZSTR_VAL(haystack) + ZSTR_LEN(haystack));
	}

	if (found) {
		RETURN_LONG(found - ZSTR_VAL(haystack));
	} else {
		RETURN_FALSE;
	}
}

[](#First-Glance)First Glance
At first glance, didn't let me down, a bit confused: what what what? First glance only understood if, else. Haven't systematically learned C language, reading it really strains the eyes, heh.
Let's go through it once:

1
2
3
4
5
zval *needle;
zend_string *haystack;
char *found = NULL;
char  needle_char[2];
zend_long  offset = 0;

This pile defines some variables.

Then
1
2
3
4
5
6
ZEND_PARSE_PARAMETERS_START(2, 3)
	Z_PARAM_STR(haystack)
	Z_PARAM_ZVAL(needle)
	Z_PARAM_OPTIONAL
	Z_PARAM_LONG(offset)
ZEND_PARSE_PARAMETERS_END();

Didn't understand, should be initializing parameters, (2, 3) means this **strpos** function has between 2-3 parameters.

Next, judgment for the third parameter offset begins.

1
2
3
4
5
6
7
if (offset < 0) {
	offset += (zend_long)ZSTR_LEN(haystack);
}
if (offset < 0 || (size_t)offset > ZSTR_LEN(haystack)) {
	php_error_docref(NULL, E_WARNING, "Offset not contained in string");
	RETURN_FALSE;
}

Guess when the third parameter offset is negative, it's a reverse search. If negative number is too small, like reverse searching 's' in 'test', strpos('test', 't', -10), will error.

1
2
3
4
➜   php -r "echo strpos('test', 's', -10);"
PHP Warning:  strpos(): Offset not contained in string in Command line code on line 1

Warning: strpos(): Offset not contained in string in Command line code on line 1

Indeed.

Won't pursue details for now, keep moving.

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
if (Z_TYPE_P(needle) == IS_STRING) {
	if (!Z_STRLEN_P(needle)) {
		php_error_docref(NULL, E_WARNING, "Empty needle");
		RETURN_FALSE;
	}

	found = (char*)php_memnstr(ZSTR_VAL(haystack) + offset,
		                Z_STRVAL_P(needle),
		                Z_STRLEN_P(needle),
		                ZSTR_VAL(haystack) + ZSTR_LEN(haystack));
} else {
	if (php_needle_char(needle, needle_char) != SUCCESS) {
		RETURN_FALSE;
	}
	needle_char[1] = 0;

	found = (char*)php_memnstr(ZSTR_VAL(haystack) + offset,
						needle_char,
						1,
	                    ZSTR_VAL(haystack) + ZSTR_LEN(haystack));
}

An if(){} else{}, oh my god, seems very simple, just judge whether the search parameter needle is string type, then so and so, finally return a found.

And found's core is a function **php_memnstr** that truly finds this character's position, this function's entity is actually **zend_memnstr** this function.

Continue tracing down to see

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
static zend_always_inline const char *
zend_memnstr(const char *haystack, const char *needle, size_t needle_len, const char *end)
{
	const char *p = haystack;
	const char ne = needle[needle_len-1];
	ptrdiff_t off_p;
	size_t off_s;

	if (needle_len == 1) {
		return (const char *)memchr(p, *needle, (end-p));
	}

	off_p = end - haystack;
	off_s = (off_p > 0) ? (size_t)off_p : 0;

	if (needle_len > off_s) {
		return NULL;
	}

	if (EXPECTED(off_s < 1024 || needle_len < 9)) {	/* glibc memchr is faster when needle is too short */
		end -= needle_len;

		while (p <= end) {
			if ((p = (const char *)memchr(p, *needle, (end-p+1))) && ne == p[needle_len-1]) {
				if (!memcmp(needle, p, needle_len-1)) {
					return p;
				}
			}

			if (p == NULL) {
				return NULL;
			}

			p++;
		}

		return NULL;
	} else {
		return zend_memnstr_ex(haystack, needle, needle_len, end);
	}
}

Here zend_memnstr(), receives four passed parameters. Here can see, when判断出 searched string is very short, search range is also very short, (why off_s < 1024 or needle_len < 9 these two thresholds, don't know) calls glibc library, this library is linux's lowest level api, otherwise runs to call **zend_operators.h** file below **ZEND_FASTCALL** type **zend_memnstr_ex**, comments say glibc is faster.

ptrdiff_t is actually a zend_long, defined in /intl/collator/collator_sort.c file below.

1
2
3
#if !defined(HAVE_PTRDIFF_T) && !defined(_PTRDIFF_T_DEFINED)
typedef zend_long ptrdiff_t;
#endif

Jumping off to do other things again

/ext/standard/file.c

```lisp
#define FPUTCSV_FLD_CHK(c) memchr(ZSTR_VAL(field_str), c, ZSTR_LEN(field_str))
```

Others not quite understood.

In the non-string type search branch judgment, also did detailed judgment. In summary: character to search should be string or numeric type.

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
static int php_needle_char(zval *needle, char *target)
{
	switch (Z_TYPE_P(needle)) {
		case IS_LONG:
			*target = (char)Z_LVAL_P(needle);
			return SUCCESS;
		case IS_NULL:
		case IS_FALSE:
			*target = '\0';
			return SUCCESS;
		case IS_TRUE:
			*target = '\1';
			return SUCCESS;
		case IS_DOUBLE:
			*target = (char)(int)Z_DVAL_P(needle);
			return SUCCESS;
		case IS_OBJECT:
			*target = (char) zval_get_long(needle);
			return SUCCESS;
		default:
			php_error_docref(NULL, E_WARNING, "needle is not a string or an integer");
			return FAILURE;
	}
}

Then saw the world's end:

1
2
3
4
5
if (found) {
	RETURN_LONG(found - ZSTR_VAL(haystack));
} else {
	RETURN_FALSE;
}

Found, return a position, not found return FALSE.
Stretching exercise done.
Now looking back, seems not that simple. Many macros don't know what they're for, several methods too.

[](#Detailed-Investigation)Detailed Investigation
First need to understand ZSTR_LEN(haystack) what this macro is for. Found its definition in zend_string.h:

1
2
3
4
#define ZSTR_VAL(zstr)  (zstr)->val
#define ZSTR_LEN(zstr)  (zstr)->len
#define ZSTR_H(zstr)    (zstr)->h
#define ZSTR_HASH(zstr) zend_string_hash_val(zstr)

This explanation in a PHP string extension [article](https://juejin.im/entry/583e8f36ac502e006c3605ee) writes:
"**ZSTR_** prefixed macro methods are **zend_string** structure专属 methods **ZSTR_VAL**, **ZSTR_LEN**, **ZSTR_H** macro methods correspond to **zend_string** structure members.
**ZSTR_HASH** gets string hash value, if doesn't exist, calls hash function to generate one".

[](#strpos's-Implementation-Idea)strpos's Implementation Idea[](#Summary)Summary
Headache

[](#Got-Inspired?)Got Inspired?
No, feel底层写的很难懂. Because always getting stuck. Various macro definitions, various pointers children and grandchildren endless.
