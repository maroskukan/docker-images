# Stage 1: Build the Go binary
FROM golang:1.20.6 AS builder

# Install necessary system dependencies (ca-certificates)
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates

WORKDIR /app
COPY src/main.go src/go.mod ./

# Download dependencies
RUN go mod tidy

# Build the Go binary
RUN CGO_ENABLED=0 GOOS=linux go build -o app

# Stage 2: Create the final container
FROM scratch

# Copy the certificates from the first stage
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

WORKDIR /app

# Copy the Go binary from the previous stage
COPY --from=builder /app/app . 

# Expose port 80 to access the Go web application
EXPOSE 80

# Set environment variables to connect to the Redis database
ENV REDIS_HOST db
ENV REDIS_PORT 6379

# Set the non-root user to run the container
USER 1000:1000

# Start the Go web application
CMD ["./app"]
