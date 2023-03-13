.PHONY: help build run clean

# Display help text
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  build      Build the Docker image"
	@echo "  run        Run the Docker container"
	@echo "  clean      Remove the Docker container and image"

# Build the Docker image
build:
	docker build -t web-scraper .

# Run the Docker container
run:
	docker run -i web-scraper

# Remove the Docker container and image
clean:
	docker rm $$(docker ps -a -q) -f
	docker rmi web-scraper -f
