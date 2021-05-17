FROM python:alpine

LABEL org.opencontainers.image.title="Flask web app with Redis" \             
      org.opencontainers.image.description="Stores and displays hitcount" \ 
      org.opencontainers.image.authors="@maroskukan"

# Install dependencies
COPY requirements.txt /tmp/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# Copy application files
COPY src/ /usr/src/app

WORKDIR /usr/src/app

# Command to run when container starts
ENTRYPOINT ["python", "app.py"]