package main

import (
	"fmt"
	"log"
	"net/http"
	"time"
	"github.com/redis/go-redis/v9"
	"golang.org/x/net/context"
)

var redisClient *redis.Client

func main() {
	// Redis client setup
	redisHost := "db" // Assuming Redis is running as a container with the name "db"
	redisPort := "6379"
	redisAddr := fmt.Sprintf("%s:%s", redisHost, redisPort)
	redisClient = redis.NewClient(&redis.Options{
		Addr:     redisAddr,
		Password: "", // No password if running locally
		DB:       0,  // Default DB
	})

	// Check if Redis is reachable
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	_, err := redisClient.Ping(ctx).Result()
	if err != nil {
		log.Fatalf("Error connecting to Redis: %s", err)
	}

	// HTTP request handling
	http.HandleFunc("/", handleRoot)

	// Start the HTTP server
	port := "80"
	log.Printf("Starting server on port %s...", port)
	err = http.ListenAndServe(":"+port, nil)
	if err != nil {
		log.Fatalf("Error starting server: %s", err)
	}
}

func handleRoot(w http.ResponseWriter, r *http.Request) {
	ctx := context.Background()

	// Increment hit count in Redis
	hitCountKey := "hit_count"
	err := redisClient.Incr(ctx, hitCountKey).Err()
	if err != nil {
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	// Get current hit count from Redis
	hitCount, err := redisClient.Get(ctx, hitCountKey).Result()
	if err != nil {
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	// Respond to the client with the hit count
	w.Header().Set("Content-Type", "text/plain")
	fmt.Fprintf(w, "Hello! You are visitor number %s", hitCount)
}
