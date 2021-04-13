# Docker mergemd Image

The Dockerfile is prepared to follow the installation of merge-md as node package defined in [Chruxin Merge-md](https://github.com/chruxin/merge-md) repository

## How to build this image

Build and tag the image pointing context to current working directory. 

```bash
docker build -t maroskukan/mergemd:latest .
```

Verify that application works by running a container from image.

```bash
docker container run -it --rm -v $(pwd):/workdir maroskukan/mergemd content
```