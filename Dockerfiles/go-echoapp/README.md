# Docker Go Web App Image

The `Dockerfile` is prepared to demostrate how to Dockerize a Go Web Application.

## Building

Build and tag the image pointing context to current working directory. 

```bash
docker build -t maroskukan/go-echoapp:latest .
```

## Run

Verify that application works by running a container from image.

```bash
docker container run -d -p 8000:80 maroskukan/go-echoapp:latest
```

## Test

Request:

```bash
# Test the application
curl localhost:8000/Hello%20World
```

Response:

```html
Hello, "/Hello World"
```