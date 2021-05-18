FROM python:3.9.5-alpine

LABEL org.opencontainers.image.title="Flask Hello World Web App" \             
      org.opencontainers.image.description="Renders HTML code from template" \ 
      org.opencontainers.image.authors="@maroskukan"

# Install dependencies
COPY requirements.txt /tmp/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

COPY src/ /project

WORKDIR /project
CMD ["python","app.py"]