# 🚨 IMMEDIATE COOLIFY DEPLOYMENT GUIDE

Your Coolify instance is showing "no available server" - you need to configure a server first or use the UI.

## Option 1: Fix Coolify Server Configuration (REQUIRED FIRST)

1. **Login to Coolify Dashboard**: https://coolify.benniewilliams.com
2. **Go to Settings → Servers**
3. **Add or Configure a Server**:
   - If no server exists, click "Add Server"
   - If server exists but offline, check its connection

## Option 2: Deploy via Coolify UI (RECOMMENDED)

### Step 1: Login to Coolify
- URL: https://coolify.benniewilliams.com
- Use your admin credentials

### Step 2: Create New Application
1. Click **"+ New Resource"** or **"+ New"**
2. Select **"Public Repository"**
3. Enter Repository Details:
   ```
   Repository: https://github.com/MDsniper/benniewilliams-wagtail
   Branch: main
   Build Pack: Dockerfile
   ```

### Step 3: Configure Application
**Basic Settings:**
- Name: `benniewilliams`
- Port: `8000`

### Step 4: Environment Variables
Click "Environment Variables" and add these EXACTLY:

```env
SECRET_KEY=d3laOyzMtn9l#6xd25j!8yJ1tPS_OVSB5glnsSk-!N*GQ8v26J
DJANGO_SETTINGS_MODULE=benniewilliams.settings.production
ALLOWED_HOSTS=benniewilliams.com,www.benniewilliams.com,localhost
DEBUG=False
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Step 5: Configure Domains
- Primary: `benniewilliams.com`
- Secondary: `www.benniewilliams.com`
- ✅ Enable SSL Certificate
- ✅ Force HTTPS

### Step 6: Health Check
- Path: `/health/`
- Interval: `30`
- Timeout: `5`

### Step 7: Deploy
- Click **"Deploy"**
- Watch logs for "Starting gunicorn"

## Option 3: Use Docker Compose Directly (Alternative)

If Coolify isn't working, deploy directly on your server:

```bash
# SSH to your server
cd /opt
git clone https://github.com/MDsniper/benniewilliams-wagtail
cd benniewilliams-wagtail

# Create .env file
cat > .env << 'EOF'
SECRET_KEY=d3laOyzMtn9l#6xd25j!8yJ1tPS_OVSB5glnsSk-!N*GQ8v26J
DJANGO_SETTINGS_MODULE=benniewilliams.settings.production
ALLOWED_HOSTS=benniewilliams.com,www.benniewilliams.com
DEBUG=False
EOF

# Deploy with Docker Compose
docker-compose -f docker-compose.coolify.yml up -d

# Check logs
docker-compose -f docker-compose.coolify.yml logs -f
```

## Troubleshooting Coolify

### "No Available Server" Error
This means:
1. No server is configured in Coolify
2. Server is offline/disconnected
3. Server resources are exhausted

**Fix:**
1. Go to Coolify Settings → Servers
2. Add your server or fix the existing one
3. Ensure Docker is running on the server
4. Check server has enough resources

### API Token Issues
Your token appears valid but the server isn't configured. The token is:
```
2|t9fZhI2hBBsGnqrcV5hFlSu5QS1iZM0btF5dCDivecf3d74a
```

## Quick Verification After Deployment

```bash
# Check if site is running
curl https://benniewilliams.com/health/

# Expected response:
# {"status": "healthy", "checks": {...}}
```

## Your Repository is Ready

✅ Repository: https://github.com/MDsniper/benniewilliams-wagtail
✅ Health checks implemented
✅ Production-ready Dockerfile
✅ All fixes applied

**Just need to:**
1. Fix Coolify server configuration
2. Deploy via UI using settings above