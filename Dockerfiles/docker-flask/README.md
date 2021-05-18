# Docker Flask Web App Image

The Dockerfile is prepared to demostrate how to Dockerize a Flask Web Application.

## How to build this image

Build and tag the image pointing context to current working directory. 

```bash
docker build -t maroskukan/welcome_flask:latest .
```

## How to run this image

Verify that application works by running a container from image.

```bash
docker container run -it --rm -p 8000:80 -e PORT=80 maroskukan/welcome_flask:latest
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://172.17.0.2:80/ (Press CTRL+C to quit)
```

```html
curl localhost:8000
<!DOCTYPE thml>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Flask Web App</title>
    <link rel="stylesheet" type= "text/css" href= "/css/main.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Ubuntu:300" >
</head>
<body>
    <div class="main">
        <img src="/images/image.png"/>
        <div class="content">
        <div id="message">
            Welcome to Flask Web App!
        </div>
        <div id="info">
            <table>
            <tr>
                <th>Pod/container/host that serviced this request:</th>
                <td>d7eb93396496</td>
            </tr>
            </table>
        </div>
    </div>
</body>
</html>
```