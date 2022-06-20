FROM jenkins/jenkins:alpine

LABEL org.opencontainers.image.title="Jenkins service" \
      org.opencontainers.image.description="Provides Jenkins service with docker cli" \
      org.opencontainers.image.authors="@maroskukan"

USER root
RUN apk add --no-cache docker-cli
RUN addgroup -g 1001 docker && addgroup jenkins docker