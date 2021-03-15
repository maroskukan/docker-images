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

Start by downloading a base image from Docker Hub. Verify that is available in local cache.
```bash
# Step 1 Pull Image from Docker Hub
docker pull alpine
# Step 2 Verify Image in local cache
docker image ls --format \
'table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Size}}' alpine:latest
REPOSITORY   TAG       IMAGE ID       SIZE
alpine       latest    28f6e2705743   5.61MB
```

Invoke the container with required arguments.
```bash
docker container run alpine apk add --no-cache python3
fetch https://dl-cdn.alpinelinux.org/alpine/v3.13/main/x86_64/APKINDEX.tar.gz
fetch https://dl-cdn.alpinelinux.org/alpine/v3.13/community/x86_64/APKINDEX.tar.gz
(1/10) Installing libbz2 (1.0.8-r1)
(2/10) Installing expat (2.2.10-r1)
(3/10) Installing libffi (3.3-r2)
(4/10) Installing gdbm (1.19-r0)
(5/10) Installing xz-libs (5.2.5-r0)
(6/10) Installing ncurses-terminfo-base (6.2_p20210109-r0)
(7/10) Installing ncurses-libs (6.2_p20210109-r0)
(8/10) Installing readline (8.1.0-r0)
(9/10) Installing sqlite-libs (3.34.1-r0)
(10/10) Installing python3 (3.8.7-r1)
Executing busybox-1.32.1-r3.trigger
OK: 53 MiB in 24 packages
```

Retrieve the container ID.
```bash
docker container ls -l --format 'table {{.ID}}\t{{.Image}}\t{{.Command}}'
CONTAINER ID   IMAGE     COMMAND
0efeb5a8add4   alpine    "apk add --no-cache …"
```

Display changes that were made to the container.
```bash
docker container diff 0efeb5a8add4 | grep python
A /usr/lib/libpython3.so
A /usr/lib/libpython3.8.so.1.0
A /usr/lib/python3.8
A /usr/lib/python3.8/profile.py
A /usr/lib/python3.8/shelve.py
A /usr/lib/python3.8/urllib
A /usr/lib/python3.8/urllib/__init__.py
A /usr/lib/python3.8/urllib/__pycache__
A /usr/lib/python3.8/urllib/__pycache__/request.cpython-38.pyc
A /usr/lib/python3.8/urllib/__pycache__/__init__.cpython-38.opt-1.pyc
```

Once happy with the filesystem changes, commit the change.
```bash
docker container commit -m "Added Python3" 0efeb5a8add4 my-image:1.0
sha256:6986a4cbf1e5b8f77730aaa5aeb3cd736a98c3001b3d0a26dcdf9ac081c9add7
```

The newly created image is prepared for use in local cache.
```bash
docker image ls --format \
'table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Size}}' my-image:1.0
REPOSITORY   TAG       IMAGE ID       SIZE
my-image     1.0       6986a4cbf1e5   49.2MB
```

