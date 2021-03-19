# Building Docker Images
- [Building Docker Images](#building-docker-images)
  - [Introduction](#introduction)
  - [Documentation](#documentation)
  - [Building an image](#building-an-image)
  - [Committing container to image](#committing-container-to-image)
    - [Flattening a Docker Image](#flattening-a-docker-image)
  - [Building Docker Images](#building-docker-images-1)
    - [Invoking build process](#invoking-build-process)
    - [Build Context](#build-context)
    - [Dockerfile](#dockerfile)
  - [Authoring Docker Images](#authoring-docker-images)
    - [FROM Instruction](#from-instruction)
    - [ENV Instruction](#env-instruction)
    - [ARG Instruction](#arg-instruction)
    - [RUN Instruction](#run-instruction)
    - [COPY Instruction](#copy-instruction)
    - [CMD Instruction](#cmd-instruction)
    - [ENTRYPOINT Instruction](#entrypoint-instruction)
    - [HEALTHCHECK Instruction](#healthcheck-instruction)
    - [ONBUILD Instruction](#onbuild-instruction)
    - [Metadata Instructions](#metadata-instructions)
  - [Creating Nginx Docker Image](#creating-nginx-docker-image)
    - [Planning](#planning)
    - [Writing Docker File](#writing-docker-file)
    - [Building an Image](#building-an-image-1)
    - [Multi-stage Image Builds](#multi-stage-image-builds)

## Introduction

Docker image provides the following key features:
- Filesystem, containing all application dependencies
- Metadata, such as environment variables, exposed ports
- Command, which process gets executed when starting a new container


## Documentation
- [Format command and log output](https://docs.docker.com/config/formatting/)
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Install python package in Dockerfile](https://stackoverflow.com/questions/50333650/install-python-package-in-docker-file/50339177)
- [View logs for a container or service](https://docs.docker.com/config/containers/logging/)

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


## Committing container to image

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


## Building Docker Images

There are number of ingrediences that are needed to build an authored Docker image:
- Base image
- Dockerfile
- Artifacts

### Invoking build process

Docker image build is invoked by using `docker image build` command. You define the `tag` and the build context `.` (current working directory) which is send as an archive from client to daemon. The first build step in `Dockerfile` references the base image, for example `FROM alpine:latest`.
```bash
# Located Dockerfile
cd examples/lighttpd
# Build process
docker image build -t my_image .
```

Each build step uses image produced by the previous step. A command is executed in a container derived from the image. The container is commited to a new image, before it is removed.

If all steps are successful, the image created in the final step is tagged with the name we provided. Intermediate images are retained to aid future builds.

### Build Context

Docker client initializes the build but Docker daemon performs the build. Ideally, local build contexts should be organizaed into projects. 

Pleace the Dockerfile in the root directory of each project and organize other build artifacts within the project directory.

Use `.dockerignore` file to exclude unnecessary content form being sent to daemon.

### Dockerfile

Dockerfile is a text file. It's default name is `Dockerfile`, and is located at the root of the build context. It provides series of instructions for image build process.

Instructions are executed in containers in order to create:
- Filesystem content
- Active or passive metadata content


## Authoring Docker Images

### FROM Instruction

To author a custom docker image, start by selecing a base image using `FROM` instruction. This must be defined as the first instruction in Dockerfile. 

The argument must define a repository, but tag is optional.
```dockerfile
FROM <repository>[<:tag>]
FROM <repository>[<@digest>]
```

Digest refers to image manifest digest, can can be seen when pull an image from registry and inspecting the image locally.
```bash
# Pulling the image
docker pull debian:latest
latest: Pulling from library/debian
e22122b926a1: Pull complete 
Digest: sha256:9d4ab94af82b2567c272c7f47fa1204cd9b40914704213f1c257c44042f82aac
Status: Downloaded newer image for debian:latest
docker.io/library/debian:latest

# Inspecting the image
docker image inspect --format '{{.RepoDigests}}' debian
[debian@sha256:9d4ab94af82b2567c272c7f47fa1204cd9b40914704213f1c257c44042f82aac]
```

Besides refereing to an base image there is a special keyword, `scratch` that indicates build with no base image.

### ENV Instruction

The `ENV` instruction declares an environment variable. It must be assigned a value and the scope applies from point of declaration. Variable and its value persist into derived container.
```dockerfile
ENV <variable> <value>
ENV <variable=value>
```

The following two declarations have same effect, but latter minizes number of layers in the image.
```dockerfile
ENV MONGO_MAJOR 3.4
ENV MONGO_VERSION 3.4.4
ENV MONGO_PACKAGE mongodb-org
```

```dockerfile
ENV MONGO_MAJOR=3.4           \
    MONG_VERSION=3.4.4        \
    MONGO_PACKAGE=mongodb-org
```

### ARG Instruction

The `ARG` instruction defines variable passed on command line. It can optionally, define a default value. Variable can be consumed from point of definition and is does not persist into derived container. Altered build args break build cache at point consumed.

```dockerfile
ARG <variable[=default value]>
```

### RUN Instruction

The `RUN` instruction executes command inside container. It is the recommended way for adding remote artifacts (Updates, Packages) to image. There are two forms of syntax:
- shell - executes command in shell
- exec - used when filesystem is devoid of shell

Build cache breaks only if instruction alters.
```dockerfile
RUN <command parameter ...>
RUN <["executable", "parameter", ...]>
```

To mitigate excessive layers created by build process form following instructions:
```dockerfile
FROM debian
RUN apt-get update
RUN apt-get install -y wget
RUN rm -rf /var/lib/apt/lists/*
```

Can be optimized by running all three instructions in single layer:
```dockerfile
FROM debian
RUN apt-get update              && \
    apt-get install -y wget     && \
    rm -rf /var/lib/apt/lists/*
```
### COPY Instruction

The `COPY` instruction copies files from build context to image. It is the recommended way for adding local artifacts to image. Multiple sourcess can be specified in one instruction. Sources can contain globbing characters. Destination can be relative or absolute path. Content is added with a UID and GID of 0

```dockerfile
COPY <src> ... <dst>
COPY ["<src>" ... "<dst>"]
```

### CMD Instruction

The `CMD` instruction is used to define a default command. Or provide default parameters to `ENTRYPOINT` instruction. Two forms of syntax: shell and exec (preferred). Exec form used for default parameters. Command line arguments override CMD.

```dockerfile
CMD <command parameter ...> or <parameter parameter ...>
CMD ["<command>", "<parameter>", ...]
```

An example `Dockerfile` that uses `CMD` instructiction is below:
```dockerfile
FROM debian:buster-slim

RUN apt-get update                             && \
    apt-get install -y --no-install-recommends    \
        cowsay                                    \
        screenfetch                            && \
        rm -rf /var/lin/apt/lists/*

ENV PATH "$PATH:/usr/games"

CMD ["cowsay", "To improve is to change; to be perfect is to change often"]
```

Build the image and run a container.
```bash
docker build -t demo .
docker container run --rm demo
 ________________________________________
/ To improve is to change; to be perfect \
\ is to change often                     /
 ----------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

To overide the argument in `CMD` instruction, pass a parameter at the end of docker container run command.
```bash
docker container run --rm demo screenfetch -E
         _,met$$$$$gg.           root@46a5f3cbe996
      ,g$$$$$$$$$$$$$$$P.        OS: Debian 
    ,g$$P""       """Y$$.".      Kernel: x86_64 Linux 4.19.128-microsoft-standard
   ,$$P'              `$$$.      Uptime: 1d 10h 48m
  ',$$P       ,ggs.     `$$b:    Packages: 99
  `d$$'     ,$P"'   .    $$$     Shell: 
   $$P      d$'     ,    $$P     CPU: Intel Core i7-9850H @ 12x 2.592GHz
   $$:      $$.   -    ,d$$'     GPU: 
   $$\;      Y$b._   _,d$P'      RAM: 1992MiB / 25510MiB
   Y$$.    `.`"Y$$$$P"'         
   `$$b      "-.__              
    `Y$$                        
     `Y$$.                      
       `$$b.                    
         `Y$$b.                 
            `"Y$b._             
                `""""           
                              
```

### ENTRYPOINT Instruction

The `ENTRYPOINT` instruction is used to define executable. Employed to constrain what is executed. Command line arguments appended. Two forms of syntax: shell and exec (preferred). Shell form limits control using Linux signals.

```dockerfile
ENTRYPOINT <executable paramater ...>
ENTRYPOINT ["<executable>", "<parameter>", ...]
```

Using the same example from previous section, replace `CMD` instruction with `ENTRYPOINT` instuction.

```dockerfile
FROM debian:buster-slim

RUN apt-get update                             && \
    apt-get install -y --no-install-recommends    \
        cowsay                                    \
        screenfetch                            && \
        rm -rf /var/lin/apt/lists/*

ENV PATH "$PATH:/usr/games"

#CMD ["cowsay", "To improve is to change; to be perfect is to change often"]
ENTRYPOINT ["cowsay"]
```

Rebuild the image and run a container.
```bash
docker build -t demo .
docker container run --rm demo
 __
<  >
 --
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

Lets try some arguments. You can see that we can pass thme to `screenfecth` directly.
```bash
docker container run --rm demo -f tux "If you're going through hell, keep going"
 ____________________________________
/ If you're going through hell, keep \
\ going                              /
 ------------------------------------
   \
    \
        .--.
       |o_o |
       |:_/ |
      //   \ \
     (|     | )
    /'\_   _/`\
    \___)=(___/
```

However, when you try to execute any other program than `cowsay`, you are not able to do so.
```bash
docker container run --rm demo screenfetch -D
 ________________
< screenfetch -D >
 ----------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     || 
```

Instructions like `CMD` and `ENTRYPOINT` can work together, for example, when specifying default arguments for programe defined in entrypoint:
```dockerfile
FROM debian:buster-slim

RUN apt-get update                             && \
    apt-get install -y --no-install-recommends    \
        cowsay                                    \
        screenfetch                            && \
        rm -rf /var/lin/apt/lists/*

ENV PATH "$PATH:/usr/games"

CMD ["-f", "tux", "Default is the easiest choice"]
ENTRYPOINT ["cowsay"]
```

Rebuild the image and run a container.
```bash
docker build -t demo .
docker container run --rm demo
```bash

 _______________________________
< Default is the easiest choice >
 -------------------------------
   \
    \
        .--.
       |o_o |
       |:_/ |
      //   \ \
     (|     | )
    /'\_   _/`\
    \___)=(___/
```

### HEALTHCHECK Instruction

The `HEALTHCHECK` instruction provides a means of defining a check the container process. It defines a command to test container health. Command runs periodically inside container. Options, for interval, timeout and retries. Health status is available via the Docker CLI. 

When a health check fails, an event is raised.

```dockerfile
HEALTHCHECK [options] CMD <command>
HEALTHCHECK NONE
```

The following health check tries to curl a webpage hosted at localhost every 3 seconds. If server does not respond within 2 seconds an exit code 1 is returned, triggering a health checkfail.
```dockerfile
HEALTHCHECK --interval=3s CMD curl --fail -m 2 http://localhost:80/ || exit 1
```

Start a docker container and then simulate a failure of loopback interface
```bash
docker exec -it nginx sh -c "sleep 10; ip link set lo down; sleep 15; ip link set lo up" &
watch -n 1 "docker container ls" 
docker system events --since 30m --filter event=health_status
```

### ONBUILD Instruction

The `ONBUILD` instruction provides a means to impose method on image use. It defers execution of instruction. Triggers is added to te image's metadata. Image is used as base image for similar images. For all instructions except `FROM` and `ONBUILD`.

```dockerfile
ONBUILD <instruction>
```

### Metadata Instructions

There are number of instructions which add additional medata to the image.

| **Instruction** | **Purpose** |
| --------------- | ----------- |
| EXPOSE | Specifies TCP/UDP ports for container |
| LABEL | Adds a static label to the image |
| STOPSIGNAL | Defines the signal to stop the container's process |
| USER | Sets the container's user |
| VOLUME | Specifies a mount point for persistent data |
| WORKDIR | Sets the working directory |


## Creating Nginx Docker Image

### Planning

We need to start by planning the docker image content. The following steps will be involved:
1. Prepare
   1. Flexibility
   2. Dependencies (base image)
2. Acquire
   1. Download source
   2. Verify content
   3. Unpack source
3. Build
   1. Configure
   2. Make
   3. Clean
4. Configure
   1. Logging
   2. Content
   3. Customize
5. Serve
   1. Execution

### Writing Docker File

```dockerfile
FROM alpine:3.13.2

# Define build argument and default value for version
ARG VERSION=1.18.0

# Shell syntax with -x option will display all executed commands and thier parameters
RUN set -x                                                         && \
                                                                      \
# Install build tools, libraries, and utilities                       \
    apk add --no-cache --virtual .build-deps                          \
        build-base                                                    \
        gnupg                                                         \
        pcre-dev                                                      \
        wget                                                          \
        zlib-dev                                                      \
        zlib-static                                                && \
                                                                      \
# Retrieve, verify and unpact Nginx source                            \
    TMP="$(mktemp -d)" && cd "$TMP"                                && \
    gpg --keyserver ha.pool.sks-keyservers.net --recv-keys            \
        B0F4253373F8F6F510D42178520A9993A1C052F8                   && \
    wget -q https://nginx.org/download/nginx-${VERSION}.tar.gz     && \
    wget -q https://nginx.org/download/nginx-${VERSION}.tar.gz.asc && \
    gpg --verify nginx-${VERSION}.tar.gz.asc                       && \
    tar -xf nginx-${VERSION}.tar.gz                                && \
                                                                      \
# Build and install nginx                                             \
    cd nginx-${VERSION}                                            && \
    ./configure                                                       \
        --with-ld-opt="-static"                                       \
        --with-http_sub_module                                     && \
    make install                                                   && \
    strip /usr/local/nginx/sbin/nginx                              && \
                                                                      \
# Clean up                                                            \
    cd / && rm -rf "$TMP"                                          && \
    apk del .build-deps                                            && \
                                                                      \    
# Symlink access and error logs to /dev/stdout and /dev/stderr,       \
# in order to make use of Docker's logging mechanism                  \
    ln -sf /dev/stdout /usr/local/nginx/logs/access.log            && \
    ln -sf /dev/stderr /usr/local/nginx/logs/error.log

# Customise static content, and configuration
COPY index.html /usr/local/nginx/html/
COPY nginx.conf /usr/local/nginx/conf/

# Change default stop signal from SIGTERM to SIGQUIT
STOPSIGNAL SIGQUIT

# Expose port
EXPOSE 80

# Define entrypoint and default parameters
ENTRYPOINT ["/usr/local/nginx/sbin/nginx"]
CMD ["-g", "daemon off;"]
```

### Building an Image

Once you build an image from above Dockerfile, you end up with an image of size 6.89MB.

```bash
docker build -t nginx:1.18.0 .
# Verify the Size
docker image ls nginx:1.18.0
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
nginx        1.18.0    f417cc8f0036   11 minutes ago   6.89MB

# Start container from the image
docker run -d -p 8080:80 nginx:1.18.0
e5def54ebe3610ff93bb006e62de3fdc1861654b03223ed413e68ab3a8880a7d

# Verify application
curl -I localhost:8080
HTTP/1.1 200 OK
Server: nginx/1.18.0
Date: Thu, 18 Mar 2021 18:56:00 GMT
Content-Type: text/html
Connection: keep-alive

# Verify application logs
docker logs $(docker ps -q)
172.17.0.1 - - [18/Mar/2021:18:55:32 +0000] "GET / HTTP/1.1" 200 22951 "-" "curl/7.68.0"
172.17.0.1 - - [18/Mar/2021:18:56:00 +0000] "HEAD / HTTP/1.1" 200 0 "-" "curl/7.68.0"
```

### Multi-stage Image Builds

In summary, the produced Nginx image is very optimal in size and number of layers it uses. If you examine the Dockerfile however, it is hard to maintain and if just one command fails in `RUN` instruction the whole build fails and you need to start over.

Therefore, one solution is use **Multi-stage Image Build** which separates the images by their purpose:
- Build Image - creates the artifacts necessary for the service
- Service Image - serves the service, making use of the build artifacts

Multi-sate builds use multiple `FROM` instructions. `COPY` instructions can reference content from a previous build stage and a build stage is referenced by index, or by a supplied name, for example:

```dockerfile
FROM alpine:3.13.2 as build

# Define build argument for version
ARG VERSION=1.18.0

# Output omitted

FROM scratch

# Cusomize static content and configuration
COPY --from=build /usr/local/nginx /usr/local/nginx
```

We can apply this methodology to the Nginx Dockerfile. Notice how we separated the build from serve and also used separate `RUN` instructions to further divide the build process.

```dockerfile
FROM alpine:3.13.2 as build

# Define build argument and default value for version
ARG VERSION=1.18.0

# Install build tools, libraries, and utilities
RUN apk add --no-cache --virtual .build-deps                          \
        build-base                                                    \
        gnupg                                                         \
        pcre-dev                                                      \
        wget                                                          \
        zlib-dev                                                      \
        zlib-static

# Retrieve, verify and unpact Nginx source
RUN set -x                                                         && \
    cd /tmp                                                        && \
    gpg --keyserver ha.pool.sks-keyservers.net --recv-keys            \
        B0F4253373F8F6F510D42178520A9993A1C052F8                   && \
    wget -q https://nginx.org/download/nginx-${VERSION}.tar.gz     && \
    wget -q https://nginx.org/download/nginx-${VERSION}.tar.gz.asc && \
    gpg --verify nginx-${VERSION}.tar.gz.asc                       && \
    tar -xf nginx-${VERSION}.tar.gz                                

WORKDIR /tmp/nginx-${VERSION}

# Build and install nginx
RUN ./configure                                                       \
        --with-ld-opt="-static"                                       \
        --with-http_sub_module                                     && \
    make install                                                   && \
    strip /usr/local/nginx/sbin/nginx
   
# Symlink access and error logs to /dev/stdout and /dev/stderr,
# in order to make use of Docker's logging mechanism
RUN ln -sf /dev/stdout /usr/local/nginx/logs/access.log            && \
    ln -sf /dev/stderr /usr/local/nginx/logs/error.log

FROM scratch

# Customise static content, and configuration
# passwd and group file are required for Nginx worker processes
COPY --from=build /etc/passwd /etc/group /etc/
COPY --from=build /usr/local/nginx /usr/local/nginx
COPY index.html /usr/local/nginx/html/
COPY nginx.conf /usr/local/nginx/conf/

# Change default stop signal from SIGTERM to SIGQUIT
STOPSIGNAL SIGQUIT

# Expose port
EXPOSE 80

# Define entrypoint and default parameters
ENTRYPOINT ["/usr/local/nginx/sbin/nginx"]
CMD ["-g", "daemon off;"]
```

Once you updated the Dockerfile, initiate the buld process using `docker build` command.
```bash
docker build -t nginx:1.18.0 .
# Output omitted
[+] Building 344.2s (7/14)                                                                               
 => [internal] load build definition from Dockerfile                                                0.0s
 => => transferring dockerfile: 2.30kB                                                              0.0s
 => [internal] load .dockerignore                                                                   0.0s
 => => transferring context: 2B                                                                     0.0s
 => [internal] load metadata for docker.io/library/alpine:3.13.2                                    2.2s
 => [auth] library/alpine:pull token for registry-1.docker.io                                       0.0s
 => [internal] load build context                                                                   0.0s
 => => transferring context: 63B                                                                    0.0s
 => CACHED [build 1/6] FROM docker.io/library/alpine:3.13.2@sha256:a75afd8b57e7f34e4dad8d65e2c7ba2  0.0s
 => [build 2/6] RUN apk add --no-cache --virtual .build-deps                                  bui  26.5s
 => [build 3/6] RUN set -x                                                         &&     cd /tm  315.3s
 => => # gpg:                using RSA key 520A9993A1C052F8                                              
 => => # gpg: Good signature from "Maxim Dounin <mdounin@mdounin.ru>" [unknown]                          
 => => # gpg: WARNING: This key is not certified with a trusted signature!                               
 => => # gpg:          There is no indication that the signature belongs to the owner.                   
 => => # Primary key fingerprint: B0F4 2533 73F8 F6F5 10D4  2178 520A 9993 A1C0 52F8                     
 => => # + tar -xf nginx-1.18.0.tar.gz                                                       
 # Output omitted
```

Now verify image size, run a new container and verify the application.

```bash
# Verify image size
docker image ls nginx:1.18.0
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
nginx        1.18.0    7a3df61de3f8   48 seconds ago   1.25MB
# Run a container
docker container run -d -p 8080:80 nginx:1.18.0
9b6f7e05795883fe6624c23c4e7085470e9d63a7ce9eea06ec3c613c05f9f960
# Verify application
curl -I localhost:8080
HTTP/1.1 200 OK
Server: nginx/1.18.0
Date: Fri, 19 Mar 2021 12:16:06 GMT
Content-Type: text/html
Connection: keep-alive
# Verify container logs
docker logs $(docker ps -q)
172.17.0.1 - - [19/Mar/2021:12:16:06 +0000] "HEAD / HTTP/1.1" 200 0 "-" "curl/7.68.0"
``` 
