FROM alpine:3.13.2

# Shell syntax with -x option will display all executed commands and their parameters
RUN set -x                                                         && \
                                                                      \
# Install build tools, libraries, and utilities
    apk add --no-cache --virtual .build-deps                          \
        git                                                           \
        build-base                                                    \
        autoconf                                                   && \
                                                                      \
    apk add --no-cache                                                \
        linux-headers                                                 \
        openssl-dev                                                   \
        libpcap-dev                                                   \
        libdnet-dev                                                && \
                                                                      \
# Retrieve nmap source
    TMP="$(mktemp -d)" && cd "$TMP"                                && \
    git clone https://github.com/nmap/nmap .                       && \
                                                                      \
# Build and install nmap
   ./configure                                                        \
        --without-zenmap                                           && \
    make                                                           && \
    make install                                                   && \
                                                                      \  
# Clean up
    cd / && rm -rf "$TMP"                                          
#   apk del .build-deps

# Define entrypoint and default parameters
ENTRYPOINT ["/usr/local/bin/nmap"]