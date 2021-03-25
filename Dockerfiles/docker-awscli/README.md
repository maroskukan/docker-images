# Docker AWS CLI Image

The Dockerfile is prepared to follow the official installation of AWS CLI v2 for Linux defined in [AWS Documenation](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html#cliv2-linux-install)

## How to build this image

Start by retrieving the latest AWS CLI binaries from AWS.

```bash
wget "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"
```

Build and tag the image pointing context to current working directory. 

```bash
docker build -t maroskukan/aws-cli:latest .
```

Verify that application works by running a container from image.

```bash
docker container run -it --rm maroskukan/aws-cli:latest --version
aws-cli/2.1.32 Python/3.8.8 Linux/4.19.128-microsoft-standard exe/x86_64.amzn.2 prompt/off
```