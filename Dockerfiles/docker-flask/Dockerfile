FROM python:3.9.2-alpine

WORKDIR /project
COPY . /project
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python","app.py"]