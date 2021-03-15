# Building Docker Images
- [Building Docker Images](#building-docker-images)
  - [Introduction](#introduction)
  - [Documentation](#documentation)
  - [Building an image](#building-an-image)
  - [Commiting to a container](#commiting-to-a-container)
    - [Flattening a Docker Image](#flattening-a-docker-image)

## Introduction

Docker image provides the following key features:
- Filesystem, containing all application dependencies
- Metadata, such as environment variables, exposed ports
- Command, which process gets executed when starting a new container

## Documentation
- [Format command and log output](https://docs.docker.com/config/formatting/)

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

## Commiting to a container

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

When it comes to Image size, you can see that we added almost 45 MB of data with our change. In general, it is a good practice, to remove unsessary and temporary artifacts from the image. Lighter containers result in quicker image distribution, less resource consumption and faster start-up times.

To retrieve additional information the image we just created, you can leverage `docker image inspect` command. It display the JSON representation of the image, along with its metadata, configuration for example exposed ports, and references to filesystem objects. The two key objects in this file are `Config` and `RootFS`.

```json
/* Config Object */
docker image inspect my-image:1.0 | jq '.[0].Config'
{
  "Hostname": "0efeb5a8add4",
  "Domainname": "",
  "User": "",
  "AttachStdin": false,
  "AttachStdout": true,
  "AttachStderr": true,
  "Tty": false,
  "OpenStdin": false,
  "StdinOnce": false,
  "Env": [
    "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
  ],
  "Cmd": [
    "apk",
    "add",
    "--no-cache",
    "python3"
  ],
  "Image": "alpine",
  "Volumes": null,
  "WorkingDir": "",
  "Entrypoint": null,
  "OnBuild": null,
  "Labels": {
    "desktop.docker.io/wsl-distro": "Ubuntu-20.04"
  }
}
/* RootFS Object*/
docker image inspect my-image:1.0 | jq '.[0].RootFS'
{
  "Type": "layers",
  "Layers": [
    "sha256:cb381a32b2296e4eb5af3f84092a2e6685e88adbc54ee0768a1a1010ce6376c7",
    "sha256:647425b33688a7431179e3135244c65a30eacc6f098805a8a63ef9a5eca34ab8"
  ]
}
```

If you look careful at `RootFS.Layers` object in above output, you can see that this image shares a layer with the original alpine image displayed below.
```json
/* Alpine Image Layer */
docker image inspect alpine:latest | jq '.[0].RootFS.Layers'
[
  "sha256:cb381a32b2296e4eb5af3f84092a2e6685e88adbc54ee0768a1a1010ce6376c7"
]
```

### Flattening a Docker Image

Often, building an image may involve many intermediate steps which produce layers that may include temporary artifacts, for example build tools. Because of the way how Union file system works (copy on write) it is not enough to delete these files in the top most layer to achieve size reduction. Therefore another approach is needed, which is described below.

A container's filesystem can be dumped to a tar archive using the `docker container export` command. 
```bash
docker container export -o my-image-1.1.tar $(docker container ls -lq)
```

Then it can be imported into a single layer image.
```bash
docker image import my-image-1.1.tar my-image:1.1
sha256:940be2bb1a7346ec93ab1a2612410ee49584781c52891745f979ac9fe5a866c4
```

Verify the new image and its size
```bash
docker image ls --format \
'table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Size}}' my-image:1.1
REPOSITORY   TAG       IMAGE ID       SIZE
my-image     1.1       940be2bb1a73   49.1MB
```

Verify that the new image has single layer.
```json
docker image inspect my-image:1.1 | jq '.[0].RootFS.Layers'
[
  "sha256:fbc957920e2d979d2071859c89daec81a2099d290857e427a10c92be2bf07629"
]
```

This flattening can help reduce the image size, however we also loose visibility into changes that were made to individual layers. You can see this when looking at image history.
```bash
# my-image:1.0
docker image history my-image:1.0
IMAGE          CREATED       CREATED BY                                      SIZE      COMMENT
6986a4cbf1e5   3 hours ago   apk add --no-cache python3                      43.6MB    Added Python3
28f6e2705743   3 weeks ago   /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
<missing>      3 weeks ago   /bin/sh -c #(nop) ADD file:80bf8bd014071345b…   5.61MB
# my-image:1.1
docker image history my-image:1.1
IMAGE          CREATED          CREATED BY   SIZE      COMMENT
940be2bb1a73   26 minutes ago                49.1MB    Imported from -
```



