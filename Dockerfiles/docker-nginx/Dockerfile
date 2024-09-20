FROM alpine:3.20.3 as build

# Define build argument and default value for version
ARG VERSION=1.26

# Install build tools, libraries, and utilities
RUN apk add --no-cache --virtual .build-deps                          \
        g++                                                           \
        git                                                           \
        make                                                          \
        linux-headers                                                 \
        pcre-dev

# Retrieve, verify and unpact Nginx source
RUN cd /tmp                                                        && \
    git clone -b stable-${VERSION} --single-branch                    \
              https://github.com/nginx/nginx.git

WORKDIR /tmp/nginx

# Build and install nginx
RUN ./auto/configure                                                  \
        --with-ld-opt="-static"                                       \
        --without-http_gzip_module                                    \
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