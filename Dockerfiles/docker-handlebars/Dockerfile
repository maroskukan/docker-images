FROM node:current-alpine

LABEL org.opencontainers.image.title="Hello World!" \
      org.opencontainers.image.description="Nodejs Web application" \
      org.opencontainers.image.authors="@maroskukan"

# Create directory in container image for app code
RUN mkdir -p /usr/src/app

# Copy app code (.) to /usr/src/app in container image
COPY . /usr/src/app

# Set working directory context
WORKDIR /usr/src/app

# Install dependencies from packages.json
RUN npm install

# Expose port
EXPOSE 80

# Command for container to execute
ENTRYPOINT [ "node", "app.js" ]