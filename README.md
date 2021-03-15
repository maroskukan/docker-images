# Building Docker Images

## Introduction

Docker image provides the following key features:
- Filesystem, containing all application dependencies
- Metadata, such as environment variables, exposed ports
- Command, which process gets executed when starting a new container

## Building an image

In general, there are two main approaches when it comes to building a new docker image.

Commiting to a container
- Ad hoc technique
- Used for experimenting
- Makes use of docker commit command
- Often produces sub-optimal images

Docker instructions
- Considered approach
- Used for authoring images
- Makes use of docker build command
- Can produce highly optimized images

### Commiting to a container

Start by downloading a base image from Docker Hub.
```bash
docker pull alpine
```

Invoke the container with required arguments.
```bash
docker container run alpine apk add --no-cache python
```

Retrieve the container ID.
```bash
docker container ls -l --format 'table {{.ID}}\t{{.Image}}\t{{.Command}}'
```

Display changes that were made to the container.
```bash
docker container diff <IMAGE_ID> | less
```

Once happy with the filesystem changes, commit the change.
```bash
docker container commit -m "Added Python" <IMAGE_ID> my-image:1.0
```

The newly created image is prepared for use in local cache.
```bash
docker image ls --format \
'table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Size}}' my-image:1.0
```
