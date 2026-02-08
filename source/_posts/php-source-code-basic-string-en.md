---
lang: en
title: PHP Source Code Appreciation (Macro)
date: 2018-05-01
description: 'zend Basic Type - Macro zend底层 has quite a few macros, especially php7 series, source code has quite a few structural changes compared to php 5. So won't study php5's zend, directly looking at latest php-src for future source code research. zend series macros are mainly distributed in zend_API.h, zend_types.h, zend_operators.h.'
tags: [PHP]
categories:
---

[](#zend-Basic-Type-Macro)zend Basic Type - Macro
zend底层 has quite a few macros, especially php7 series, source code has quite a few structural changes compared to php 5. So won't study php5's zend, directly looking at latest **php-src** for future source code research. zend series macros are mainly distributed in zend_API.h, zend_types.h, zend_operators.h.

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
typedef struct _zend_object_handlers zend_object_handlers;
typedef struct _zend_class_entry     zend_class_entry;
typedef union  _zend_function        zend_function;
typedef struct _zend_execute_data    zend_execute_data;

typedef struct _zval_struct     zval;

typedef struct _zend_refcounted zend_refcounted;
typedef struct _zend_string     zend_string;
typedef struct _zend_array      zend_array;
typedef struct _zend_object     zend_object;
typedef struct _zend_resource   zend_resource;
typedef struct _zend_reference  zend_reference;
typedef struct _zend_ast_ref    zend_ast_ref;
typedef struct _zend_ast        zend_ast;

Looking around, seems familiar swallows returning!

[](#zval)zval
Isn't zval the famous PHP variable container! Very high frequency of use in source code. Search php-src, appears over 9999 times!
Think about it, zval must be very important.
Uncovering this structure, found it looks like this:

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
struct _zval_struct {
	zend_value        value;			/* value */
	union {
		struct {
			ZEND_ENDIAN_LOHI_4(
				zend_uchar    type,			/* active type */
				zend_uchar    type_flags,
				zend_uchar    const_flags,
				zend_uchar    reserved)	    /* call info for EX(This) */
		} v;
		uint32_t type_info;
	} u1;
	union {
		uint32_t     next;                 /* hash collision chain */
		uint32_t     cache_slot;           /* literal cache slot */
		uint32_t     lineno;               /* line number (for ast nodes) */
		uint32_t     num_args;             /* arguments number for EX(This) */
		uint32_t     fe_pos;               /* foreach position */
		uint32_t     fe_iter_idx;          /* foreach iterator index */
		uint32_t     access_flags;         /* class constant access flags */
		uint32_t     property_guard;       /* single property guard */
		uint32_t     extra;                /* not further specified */
	} u2;
};

Divided into three parts, zend_value, u1, u2 three unions.
Track zend_value to see,

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
typedef union _zend_value {
	zend_long         lval;				/* long value */
	double            dval;				/* double value */
	zend_refcounted  *counted;
	zend_string      *str;
	zend_array       *arr;
	zend_object      *obj;
	zend_resource    *res;
	zend_reference   *ref;
	zend_ast_ref     *ast;
	zval             *zv;
	void             *ptr;
	zend_class_entry *ce;
	zend_function    *func;
	struct {
		uint32_t w1;
		uint32_t w2;
	} ww;
} zend_value;

After跋山涉水, zend_value this union can store all possible PHP data type data. Numerical parts: long or double floating point. Rest are basically pointer values. Have counter pointer, string pointer, array pointer, object pointer, resource pointer, reference pointer, null pointer, class pointer, function pointer.

And what's inside u1? ZEND_ENDIAN_LOHI_4() this thing,

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
#ifdef WORDS_BIGENDIAN
# define ZEND_ENDIAN_LOHI(lo, hi)          hi; lo;
# define ZEND_ENDIAN_LOHI_3(lo, mi, hi)    hi; mi; lo;
# define ZEND_ENDIAN_LOHI_4(a, b, c, d)    d; c; b; a;
# define ZEND_ENDIAN_LOHI_C(lo, hi)        hi, lo
# define ZEND_ENDIAN_LOHI_C_3(lo, mi, hi)  hi, mi, lo,
# define ZEND_ENDIAN_LOHI_C_4(a, b, c, d)  d, c, b, a
#else
# define ZEND_ENDIAN_LOHI(lo, hi)          lo; hi;
# define ZEND_ENDIAN_LOHI_3(lo, mi, hi)    lo; mi; hi;
# define ZEND_ENDIAN_LOHI_4(a, b, c, d)    a; b; c; d;
# define ZEND_ENDIAN_LOHI_C(lo, hi)        lo, hi
# define ZEND_ENDIAN_LOHI_C_3(lo, mi, hi)  lo, mi, hi,
# define ZEND_ENDIAN_LOHI_C_4(a, b, c, d)  a, b, c, d
#endif

These many 哆瑞咪发嗦啦, temporarily don't know what they're for. But type, type_flags, const_flags, reserved by literal meaning should contain active type, type flags, const flags, reserved value. So u1 actually stores type-related information values.

u2 stores an extra data, some say it's normally unused? This [blog](http://nikic.github.io/) says.

Several questions here remain undetermined:

Is zend_ast_ref type data?
Another zval appears! Why is this? Is this effect like: my value can still store any type of data! Is this how PHP implements storing data?
PHP official documentation gives basic types as Boolean boolean, Integer integer, Float floating point, String string, Array array, Object object, Resource resource type, NULL, CallBack/Callable type.
What's the ww structure for? Could it be for storing CallBack/Callable type data?

[](#Summary)Summary
PHP底层 isn't as simple as it looks. Some constructions might be clever, but currently can't appreciate them.
