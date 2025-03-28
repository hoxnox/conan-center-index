/* src/lib/config.h.  Generated from config.h.in by configure.  */
/* src/lib/config.h.in.  Generated from configure.ac by autoheader.  */

/* Define if building universal (internal helper macro) */
/* #undef AC_APPLE_UNIVERSAL_BUILD */

/* Define to disable built in overflow math */
/* #undef DISABLE_OVERFLOW_BUILTINS */

/* ESAPI versions below 2.2.1 are known to require manual session flag
   management. */
/* #undef ESAPI_MANAGE_FLAGS */

/* Esys3 */
#define ESYS_3 1

/* Defined when building fuzzing tests */
/* #undef FUZZING */

/* Define to 1 if you have the <dlfcn.h> header file. */
#define HAVE_DLFCN_H 1

/* Enabled if FAPI >= 3.0 is found */
#define HAVE_FAPI 1

/* Define to 1 if the system has the `weak' function attribute */
/* #undef HAVE_FUNC_ATTRIBUTE_WEAK */

/* Define to 1 if you have the <inttypes.h> header file. */
#define HAVE_INTTYPES_H 1

/* Define if you have POSIX threads libraries and header files. */
#define HAVE_PTHREAD 1

/* Have PTHREAD_PRIO_INHERIT. */
#define HAVE_PTHREAD_PRIO_INHERIT 1

/* Define to 1 if you have the <stdint.h> header file. */
#define HAVE_STDINT_H 1

/* Define to 1 if you have the <stdio.h> header file. */
#define HAVE_STDIO_H 1

/* Define to 1 if you have the <stdlib.h> header file. */
#define HAVE_STDLIB_H 1

/* Define to 1 if you have the <strings.h> header file. */
#define HAVE_STRINGS_H 1

/* Define to 1 if you have the <string.h> header file. */
#define HAVE_STRING_H 1

/* Define to 1 if you have the <sys/stat.h> header file. */
#define HAVE_SYS_STAT_H 1

/* Define to 1 if you have the <sys/types.h> header file. */
#define HAVE_SYS_TYPES_H 1

/* Define to 1 if you have the <unistd.h> header file. */
#define HAVE_UNISTD_H 1

/* Define to the sub-directory where libtool stores uninstalled libraries. */
#define LT_OBJDIR ".libs/"

/* Define if debugging is disabled */
#define NDEBUG 1

/* Name of package */
#define PACKAGE "tpm2-pkcs11"

/* Define to the address where bug reports for this package should be sent. */
#define PACKAGE_BUGREPORT "https://github.com/tpm2-software/tpm2-pkcs11/issues"

/* Define to the full name of this package. */
#define PACKAGE_NAME "tpm2-pkcs11"

/* Define to the full name and version of this package. */
#define PACKAGE_STRING "tpm2-pkcs11 1.9.1"

/* Define to the one symbol short name of this package. */
#define PACKAGE_TARNAME "tpm2-pkcs11"

/* Define to the home page for this package. */
#define PACKAGE_URL "https://github.com/tpm2-software/tpm2-pkcs11"

/* Define to the version of this package. */
#define PACKAGE_VERSION "1.9.1"

/* Define to enable 1 byte structure packing. Default for Windows builds. */
/* #undef PKCS11_PACK */

/* Define to necessary symbol if this constant uses a non-standard name on
   your system. */
/* #undef PTHREAD_CREATE_JOINABLE */

/* Define to 1 if all of the C90 standard headers exist (not just the ones
   required in a freestanding environment). This macro is provided for
   backward compatibility; new code need not use it. */
#define STDC_HEADERS 1

/* Changes the store directory to search. Defaults to /etc/tpm2_pkcs11 */
/* #undef TPM2_PKCS11_STORE_DIR */

/* Define when unit testing. libtwist uses this to define a debug interface
   for alloc failures */
/* #undef UNIT_TESTING */

/* Version number of package */
#define VERSION "1.9.1"

/* Define WORDS_BIGENDIAN to 1 if your processor stores words with the most
   significant byte first (like Motorola and SPARC, unlike Intel). */
#if defined AC_APPLE_UNIVERSAL_BUILD
# if defined __BIG_ENDIAN__
#  define WORDS_BIGENDIAN 1
# endif
#else
# ifndef WORDS_BIGENDIAN
/* #  undef WORDS_BIGENDIAN */
# endif
#endif
