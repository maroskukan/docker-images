FROM node:current-alpine

LABEL org.opencontainers.image.title="Merge MD" \
      org.opencontainers.image.description="Nodejs Merge-md application" \
      org.opencontainers.image.authors="@maroskukan"

# Create directory in container image for app code
RUN mkdir -p /workdir

# Set working directory context
WORKDIR /workdir

# Install dependencies from packages.json
RUN npm install -g merge-md

# Command for container to execute
ENTRYPOINT ["merge"]