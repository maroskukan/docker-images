FROM alpine:3.13.2 as build

# Install build tools, libraries, and utilities
RUN apk add --no-cache --virtual .build-deps                          \
        git                                                           \
        build-base                                                    \
        linux-headers                                                 \
        autoconf                                                      \
        openssl-dev                                                   \
        libpcap-dev                                                   \
        libdnet-dev

# Retrieve nmap source
RUN set -x                                                         && \
    cd /tmp                                                        && \
    git clone https://github.com/nmap/nmap

WORKDIR /tmp/nmap

# Build and install nmap
RUN ./configure                                                       \
        --without-zenmap                                           && \
    make                                                           && \
    make install                                                   && \
    strip /usr/local/bin/nmap                                      && \
    strip /usr/local/bin/ncat                                      && \
    strip /usr/local/bin/nping


FROM scratch

COPY --from=build /usr/local/bin/nmap /usr/local/bin/nmap
COPY --from=build /usr/local/bin/ncat /usr/local/bin/ncat
COPY --from=build /usr/local/bin/nping /usr/local/bin/nping

# Define entrypoint and default parameters
ENTRYPOINT ["/usr/local/bin/nmap"]