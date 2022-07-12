# Flask Web App Image

The `docker-compose.yml` file is prepared to demostrate usage of managing multi container application, a Flask web server with a Redis backend database.

## How to run the application

Start the stack by pointing context to current working directory. The `web-fe` service container will be build according to `Dockerfile`.

```bash
# Build the image and start the containers
docker-compose up -d
```

```bash
for try in {1..3}; do curl localhost:5000; done
Hit refresh. You've only refreshed 1 times.
Hit refresh. You've only refreshed 2 times.
Hit refresh. You've only refreshed 3 times.
```