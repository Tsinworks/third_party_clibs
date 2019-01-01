
if( BUILD_SHARED_LIBS )
add_definitions ( -DOPENSSL_BUILD_SHLIBSSL )
endif()

set (LIBSRC
pqueue.c
statem/statem_srvr.c statem/statem_clnt.c  s3_lib.c  s3_enc.c record/rec_layer_s3.c
statem/statem_lib.c s3_cbc.c s3_msg.c
methods.c   t1_lib.c  t1_enc.c t1_ext.c
d1_lib.c  record/rec_layer_d1.c d1_msg.c
statem/statem_dtls.c d1_srtp.c
ssl_lib.c ssl_cert.c ssl_sess.c
ssl_ciph.c ssl_stat.c ssl_rsa.c
ssl_asn1.c ssl_txt.c ssl_init.c ssl_conf.c  ssl_mcnf.c
bio_ssl.c ssl_err.c t1_reneg.c tls_srp.c t1_trce.c ssl_utst.c
record/ssl3_buffer.c record/ssl3_record.c record/dtls1_bitmap.c
statem/statem.c
)

if(BUILD_OBJECT_LIBRARY_ONLY)
  add_library( ssl OBJECT ${LIBSRC} ${LIBHDR} )
else()
add_library( ssl ${LIBSRC} )
target_link_libraries( ssl crypto )

#install( FILES ssl.h ssl2.h ssl3.h ssl23.h tls1.h dtls1.h kssl.h
#  DESTINATION include/openssl )

install( TARGETS ssl
  RUNTIME DESTINATION bin
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib )
endif()