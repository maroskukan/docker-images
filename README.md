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

