cmake_minimum_required(VERSION 3.22)

########################################################################
# deps

find_package(tpm2-tss REQUIRED)
find_package(OpenSSL REQUIRED)
find_package(SQLite3 REQUIRED)
find_package(yaml REQUIRED)

########################################################################
# deps

add_library(tpm2-pkcs11
	src/pkcs11.c
	src/lib/parser.c
	src/lib/tpm.c
	src/lib/mutex.c
	src/lib/session_table.c
	src/lib/ssl_util.c
	src/lib/typed_memory.c
	src/lib/twist.c
	src/lib/derive.c
	src/lib/general.c
	src/lib/backend_fapi.c
	src/lib/token.c
	src/lib/key.c
	src/lib/slot.c
	src/lib/random.c
	src/lib/backend.c
	src/lib/encrypt.c
	src/lib/object.c
	src/lib/attrs.c
	src/lib/db.c
	src/lib/utils.c
	src/lib/mech.c
	src/lib/digest.c
	src/lib/session.c
	src/lib/backend_esysdb.c
	src/lib/sign.c
	src/lib/emitter.c
	src/lib/session_ctx.c
)
target_link_libraries(tpm2-pkcs11)
target_include_directories(tpm2-pkcs11 PRIVATE src/lib src)

