package main

import (
	"fmt"
	"net/http"
	"os"
)

func handler(w http.ResponseWriter, r *http.Request) {
	// Get the container ID (hostname)
	hostname, err := os.Hostname()
	if err != nil {
		http.Error(w, "Error getting hostname", http.StatusInternalServerError)
		return
	}

	// Return the response
	fmt.Fprintf(w, "Hellow from Container ID: %s", hostname)
}

func main() {
	http.HandleFunc("/", handler)

	// Listen on port 8080
	fmt.Println("Starting server on port 80...")
	err := http.ListenAndServe(":80", nil)
	if err != nil {
		fmt.Println("Error starting server:", err)
	}
}
