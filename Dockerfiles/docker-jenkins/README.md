# Docker Jenkins Image

The `Dockerfile` is prepared to add `docker-cli` to upstream `jenkins/jenkins:alpine` image in order to start containers on host machine.

## How to build this image

Build and tag the image pointing to context to current working directory.

```bash
docker build -t maroskukan/jenkins:docker .
```

Verify that the jenkins user can run a docker container on host machine.

```bash
docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock maroskukan/jenkins:docker docker run --rm hello-world
```