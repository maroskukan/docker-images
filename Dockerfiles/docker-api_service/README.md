# Docker Flask REST API App Image

The Dockerfile is prepared to demostrate how to Dockerize a Flask REST API Application.

## How to build this image

Build and tag the image pointing context to current working directory. 

```bash
docker build -t maroskukan/bookstore:latest .
```

## How to run this image

Verify that application works by running a container from image.

```bash
docker container run -it --rm -p 8000:80 -e PORT=80 maroskukan/bookstore:latest
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://172.17.0.2:80/ (Press CTRL+C to quit)
```