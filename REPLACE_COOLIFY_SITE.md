# Replace Your Current Coolify BennieWilliams Site

Follow these steps to replace your existing Coolify site with the new Wagtail version:

## Step 1: Stop Current Site in Coolify

1. Log into your Coolify dashboard
2. Navigate to your current `benniewilliams` project
3. Click **Stop** to stop the current deployment
4. **DO NOT DELETE YET** - We'll keep it as backup

## Step 2: Create New Deployment

### Option A: Deploy from GitHub (Recommended)

1. In Coolify, click **New Project** or **Add Application**
2. Select **GitHub** as source
3. Repository: `https://github.com/MDsniper/benniewilliams-wagtail`
4. Branch: `main`
5. Build Pack: Select **Dockerfile**

### Option B: Deploy with Docker Compose

1. In Coolify, click **New Project**
2. Select **Docker Compose**
3. Paste the contents of `coolify-deploy.yml`

## Step 3: Configure Environment Variables

In Coolify's environment variables section, add:

```env
# REQUIRED - Generate a secure key
SECRET_KEY=your-very-secure-secret-key-here-minimum-50-chars

# Domain Configuration
ALLOWED_HOSTS=benniewilliams.com,www.benniewilliams.com

# Database (if not using Coolify's PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Optional but recommended
REDIS_URL=redis://redis:6379/0
```

### Generate Secret Key:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

## Step 4: Configure Coolify Settings

1. **Port Configuration**: Set application port to `8000`
2. **Health Check Path**: `/`
3. **Domains**:
   - Add `benniewilliams.com`
   - Add `www.benniewilliams.com`
4. **SSL**: Enable Let's Encrypt SSL

## Step 5: Configure Persistent Storage

Add these volumes in Coolify:

```yaml
Volumes:
- /media -> Container: /app/media
- /static -> Container: /app/static
- /postgres_data -> Container: /var/lib/postgresql/data (if using built-in DB)
```

## Step 6: Deploy and Test

1. Click **Deploy** in Coolify
2. Watch the deployment logs
3. Once deployed, the app will:
   - Run database migrations automatically
   - Collect static files
   - Create superuser if needed
   - Start Gunicorn server

## Step 7: Verify Deployment

1. Visit your site at `https://benniewilliams.com`
2. Check that navigation, breadcrumbs work
3. Verify About page shows your Gravatar image
4. Test all pages (Home, About, Services, Blog, Contact)

## Step 8: Create Admin User

If you need to access Wagtail admin:

```bash
# Via Coolify terminal or SSH
docker exec -it [container-id] python manage.py createsuperuser
```

Or use Coolify's terminal feature to run:
```bash
python manage.py createsuperuser
```

## Step 9: Switch DNS (if needed)

If your domain currently points to the old site:

1. Update DNS A records to point to new Coolify app
2. Or update Coolify's proxy to route to new container
3. Wait for DNS propagation (5-15 minutes)

## Step 10: Cleanup Old Deployment

Once verified working:

1. Keep old deployment stopped for 24-48 hours as backup
2. After confirmation, delete old deployment
3. Remove old Docker images to save space

## Troubleshooting

### Database Connection Issues
- Ensure DATABASE_URL is correctly formatted
- Check if Coolify's PostgreSQL addon is enabled

### Static Files Not Loading
- Verify volumes are mounted correctly
- Check that `collectstatic` ran during deployment
- Ensure `whitenoise` is handling static files

### 500 Errors
- Check SECRET_KEY is set
- Verify ALLOWED_HOSTS includes your domain
- Review logs in Coolify dashboard

### Migration Issues
- Use Coolify terminal to run manually:
  ```bash
  python manage.py migrate
  python manage.py collectstatic --noinput
  ```

## Rollback Plan

If something goes wrong:

1. Stop new deployment
2. Start old deployment
3. Revert DNS if changed
4. Debug issues with new deployment

## Support Files

- Docker configuration: `Dockerfile`, `docker-compose.yml`
- Environment template: `.env.production`
- Deployment config: `coolify-deploy.yml`
- This guide: `REPLACE_COOLIFY_SITE.md`

## Next Steps After Deployment

1. Set up regular backups in Coolify
2. Configure monitoring/alerts
3. Set up CI/CD pipeline for automatic updates
4. Add content through Wagtail admin at `/admin`