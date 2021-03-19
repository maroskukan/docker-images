FROM alpine:3.13.2 as build

# Define build argument and default value for version
ARG VERSION=1.18.0

# Install build tools, libraries, and utilities
RUN apk add --no-cache --virtual .build-deps                          \
        build-base                                                    \
        gnupg                                                         \
        pcre-dev                                                      \
        wget                                                          \
        zlib-dev                                                      \
        zlib-static

# Retrieve, verify and unpact Nginx source
RUN set -x                                                         && \
    cd /tmp                                                        && \
    gpg --keyserver ha.pool.sks-keyservers.net --recv-keys            \
        B0F4253373F8F6F510D42178520A9993A1C052F8                   && \
    wget -q https://nginx.org/download/nginx-${VERSION}.tar.gz     && \
    wget -q https://nginx.org/download/nginx-${VERSION}.tar.gz.asc && \
    gpg --verify nginx-${VERSION}.tar.gz.asc                       && \
    tar -xf nginx-${VERSION}.tar.gz                                && \
    rm -f nginx-${VERSION}.tar.*

WORKDIR /tmp/nginx-${VERSION}

# Build and install nginx
RUN ./configure                                                       \
        --with-ld-opt="-static"                                       \
        --with-http_sub_module                                     && \
    make install                                                   && \
    strip /usr/local/nginx/sbin/nginx
   
# Symlink access and error logs to /dev/stdout and /dev/stderr,
# in order to make use of Docker's logging mechanism
RUN ln -sf /dev/stdout /usr/local/nginx/logs/access.log            && \
    ln -sf /dev/stderr /usr/local/nginx/logs/error.log

FROM scratch

# Customise static content, and configuration
# passwd and group file are required for Nginx worker processes
COPY --from=build /etc/passwd /etc/group /etc/
COPY --from=build /usr/local/nginx /usr/local/nginx
COPY index.html /usr/local/nginx/html/
COPY nginx.conf /usr/local/nginx/conf/

# Change default stop signal from SIGTERM to SIGQUIT
STOPSIGNAL SIGQUIT

# Expose port
EXPOSE 80

# Define entrypoint and default parameters
ENTRYPOINT ["/usr/local/nginx/sbin/nginx"]
CMD ["-g", "daemon off;"]