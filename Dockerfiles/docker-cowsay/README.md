# Docker Cowsay Image

The Dockerfile is prepared to demostrate usage of `CMD` and `ENTRYPOINT` instructions.

## How to build this image

Build and tag the image pointing context to current working directory. 

```bash
docker build -t maroskukan/cowsay:latest .
```

Verify that application works by running a container from image.

```bash
docker container run -it --rm maroskukan/cowsay:latest
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