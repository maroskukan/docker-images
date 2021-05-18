FROM python:3.9.2-alpine

LABEL org.opencontainers.image.title="Observer" \             
      org.opencontainers.image.description="Monitors directory activity" \ 
      org.opencontainers.image.authors="@maroskukan"

# Install dependencies
COPY requirements.txt /tmp/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# Copy application files
COPY src/ /usr/src/app

WORKDIR /usr/src/app
ENTRYPOINT ["python", "-u", "/usr/src/app/app.py"]