# Flask Web App Image

The `docker-compose.yml` file is prepared to demostrate usage of managing multi container application, a Flask web server with a Redis backend database.

## How to run the application

Build and tag the image pointing context to current working directory. 

```bash
docker-compose up
Starting docker-webapp_redis_1  ... done
Starting docker-webapp_web-fe_1 ... done
Attaching to docker-webapp_redis_1, docker-webapp_web-fe_1
redis_1   | 1:C 17 May 2021 08:46:13.165 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis_1   | 1:C 17 May 2021 08:46:13.165 # Redis version=6.2.1, bits=64, commit=00000000, modified=0, pid=1, just started
redis_1   | 1:C 17 May 2021 08:46:13.165 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
redis_1   | 1:M 17 May 2021 08:46:13.166 * monotonic clock: POSIX clock_gettime
redis_1   | 1:M 17 May 2021 08:46:13.166 * Running mode=standalone, port=6379.
redis_1   | 1:M 17 May 2021 08:46:13.166 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
redis_1   | 1:M 17 May 2021 08:46:13.166 # Server initialized
redis_1   | 1:M 17 May 2021 08:46:13.167 * Loading RDB produced by version 6.2.1
redis_1   | 1:M 17 May 2021 08:46:13.167 * RDB age 721 seconds
redis_1   | 1:M 17 May 2021 08:46:13.167 * RDB memory usage when created 0.77 Mb
redis_1   | 1:M 17 May 2021 08:46:13.167 * DB loaded from disk: 0.000 seconds
redis_1   | 1:M 17 May 2021 08:46:13.167 * Ready to accept connections
web-fe_1  |  * Serving Flask app "app" (lazy loading)
web-fe_1  |  * Environment: production
web-fe_1  |    WARNING: This is a development server. Do not use it in a production deployment.
web-fe_1  |    Use a production WSGI server instead.
web-fe_1  |  * Debug mode: on
web-fe_1  |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
web-fe_1  |  * Restarting with stat
web-fe_1  |  * Debugger is active!
web-fe_1  |  * Debugger PIN: 416-851-558
```

```bash
for try in {1..3}; do curl localhost:5000; done
Hit refresh if you think Sunderland are the greatest football team in the world. You've only refreshed 1 times. REFRESH MORE!!!
Hit refresh if you think Sunderland are the greatest football team in the world. You've only refreshed 2 times. REFRESH MORE!!!
Hit refresh if you think Sunderland are the greatest football team in the world. You've only refreshed 3 times. REFRESH MORE!!!
```