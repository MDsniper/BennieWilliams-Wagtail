#!/bin/bash

# FaceSwap Container Management Script
# This script manages the FaceSwap container deployment

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/docker-compose.faceswap.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

# Function to start FaceSwap
start_faceswap() {
    print_status "Starting FaceSwap container..."
    cd "$SCRIPT_DIR"
    docker compose -f "$COMPOSE_FILE" up -d

    if [ $? -eq 0 ]; then
        print_status "FaceSwap container started successfully!"
        print_status "Web interface will be available at: http://localhost:7861"
        print_status "Please wait 30-60 seconds for the application to fully initialize."
    else
        print_error "Failed to start FaceSwap container."
        exit 1
    fi
}

# Function to stop FaceSwap
stop_faceswap() {
    print_status "Stopping FaceSwap container..."
    cd "$SCRIPT_DIR"
    docker compose -f "$COMPOSE_FILE" down

    if [ $? -eq 0 ]; then
        print_status "FaceSwap container stopped successfully!"
    else
        print_error "Failed to stop FaceSwap container."
        exit 1
    fi
}

# Function to show status
show_status() {
    print_status "FaceSwap Container Status:"
    docker ps --filter "name=faceswap-app" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

    # Show logs if container is running
    if docker ps --filter "name=faceswap-app" --format "{{.Names}}" | grep -q faceswap-app; then
        echo
        print_status "Recent logs:"
        docker logs faceswap-app --tail 10
    fi
}

# Function to show logs
show_logs() {
    docker logs faceswap-app -f
}

# Function to restart FaceSwap
restart_faceswap() {
    print_status "Restarting FaceSwap container..."
    stop_faceswap
    sleep 3
    start_faceswap
}

# Main script logic
case "${1:-start}" in
    start)
        start_faceswap
        ;;
    stop)
        stop_faceswap
        ;;
    restart)
        restart_faceswap
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        echo
        echo "Commands:"
        echo "  start   - Start the FaceSwap container (default)"
        echo "  stop    - Stop the FaceSwap container"
        echo "  restart - Restart the FaceSwap container"
        echo "  status  - Show container status and recent logs"
        echo "  logs    - Follow container logs in real-time"
        exit 1
        ;;
esac