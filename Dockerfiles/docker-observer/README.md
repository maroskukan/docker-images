# Docker Observer Image

The Dockerfile is prepared to demostrate usage of passing environment variables to docker container. This image build was inpired by [Adam Cyber's Turn your Python Script into a Real Program with Docker](https://python.plainenglish.io/turn-your-python-script-into-a-real-program-with-docker-c200e15d5265)

## How to build this image

Build and tag the image pointing context to current working directory. 

```bash
docker build -t maroskukan/observer:latest .
```

Verify that application works by running a container from image.

```bash
# Create a test directory
mkdir -p /tmp/test

# Start the image in background
docker run -d --restart=always -e DIRECTORY='/tmp/test' -v /tmp/:/tmp/ observer
d85ddec4fc6c25163a3b6c77c5288544477e0a07df03ad33e045b8e28abb2eb6

# Create a test file
touch /tmp/test/testfile.txt

# Display container logs
docker logs d85d
INFO:root:Created file: /tmp/test/testfile.txt
INFO:root:Modified directory: /tmp/test
INFO:root:Modified file: /tmp/test/testfile.txt
INFO:root:Modified directory: /tmp/test
```