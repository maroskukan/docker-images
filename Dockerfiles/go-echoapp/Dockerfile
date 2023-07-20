# Stage 1: Build the Go binary
FROM golang:1.20.6 AS builder

WORKDIR /app
COPY src/main.go ./

# Initialize Go modules
RUN go mod init example/echoapp

# Build the Go binary
RUN CGO_ENABLED=0 GOOS=linux go build -o app

# Stage 2: Create the final container
FROM scratch

WORKDIR /app

# Copy the Go binary from the previous stage
COPY --from=builder /app/app . 

# Expose port 80 to access the Go web application
EXPOSE 80

# Start the Go web application
CMD ["./app"]
