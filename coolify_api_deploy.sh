#!/bin/bash

# Coolify API Deployment Script
COOLIFY_TOKEN="2|t9fZhI2hBBsGnqrcV5hFlSu5QS1iZM0btF5dCDivecf3d74a"
COOLIFY_URL="https://coolify.benniewilliams.com"

# Generate secure secret key
SECRET_KEY=$(python3 -c "import secrets; import string; chars = string.ascii_letters + string.digits + '!@#%^&*(-_=+)'; print(''.join(secrets.choice(chars) for _ in range(50)))" 2>/dev/null || echo "d3laOyzMtn9l#6xd25j!8yJ1tPS_OVSB5glnsSk-!N*GQ8v26J")

echo "🚀 Deploying to Coolify via API..."
echo "================================="

# First, let's check what endpoints are available
echo "Checking API endpoints..."

# Try to get team info
echo "Checking teams..."
curl -s -H "Authorization: Bearer ${COOLIFY_TOKEN}" \
     -H "Accept: application/json" \
     "${COOLIFY_URL}/api/v1/teams" | jq '.' || echo "Teams endpoint not accessible"

# Try to get servers
echo "Checking servers..."
curl -s -H "Authorization: Bearer ${COOLIFY_TOKEN}" \
     -H "Accept: application/json" \
     "${COOLIFY_URL}/api/v1/servers" | jq '.' || echo "Servers endpoint not accessible"

# Create application deployment payload
cat > /tmp/coolify_deploy.json << EOF
{
  "name": "benniewilliams-wagtail",
  "type": "public",
  "git_repository": "https://github.com/MDsniper/benniewilliams-wagtail",
  "git_branch": "main",
  "build_pack": "dockerfile",
  "ports_exposes": "8000",
  "health_check_enabled": true,
  "health_check_path": "/health/",
  "health_check_port": 8000,
  "health_check_interval": 30,
  "domains": [
    {"domain": "benniewilliams.com", "force_https": true},
    {"domain": "www.benniewilliams.com", "force_https": true}
  ],
  "environment_variables": [
    {"key": "SECRET_KEY", "value": "${SECRET_KEY}", "is_build_time": false},
    {"key": "DJANGO_SETTINGS_MODULE", "value": "benniewilliams.settings.production", "is_build_time": false},
    {"key": "ALLOWED_HOSTS", "value": "benniewilliams.com,www.benniewilliams.com,localhost", "is_build_time": false},
    {"key": "DEBUG", "value": "False", "is_build_time": false},
    {"key": "SECURE_SSL_REDIRECT", "value": "True", "is_build_time": false},
    {"key": "SESSION_COOKIE_SECURE", "value": "True", "is_build_time": false},
    {"key": "CSRF_COOKIE_SECURE", "value": "True", "is_build_time": false}
  ],
  "volumes": [
    {"mount_path": "/app/media", "volume_name": "media"},
    {"mount_path": "/app/static", "volume_name": "static"}
  ],
  "limits_memory": "1024",
  "limits_cpu": "1"
}
EOF

echo ""
echo "Deployment configuration created."
echo ""
echo "Trying to create application..."

# Try to create the application
curl -X POST \
     -H "Authorization: Bearer ${COOLIFY_TOKEN}" \
     -H "Accept: application/json" \
     -H "Content-Type: application/json" \
     -d @/tmp/coolify_deploy.json \
     "${COOLIFY_URL}/api/v1/applications" \
     -v

echo ""
echo "If the above didn't work, trying alternative endpoints..."

# Try alternative deployment endpoint
curl -X POST \
     -H "Authorization: Bearer ${COOLIFY_TOKEN}" \
     -H "Accept: application/json" \
     -H "Content-Type: application/json" \
     -d @/tmp/coolify_deploy.json \
     "${COOLIFY_URL}/api/v1/projects/1/applications" \
     -v

echo ""
echo "Checking for existing applications..."

# List applications
curl -H "Authorization: Bearer ${COOLIFY_TOKEN}" \
     -H "Accept: application/json" \
     "${COOLIFY_URL}/api/v1/applications" | jq '.'