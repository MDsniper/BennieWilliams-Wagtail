# Deploying Bennie Williams Wagtail Site with Coolify

## Prerequisites

- Coolify instance running and accessible
- Domain name configured (benniewilliams.com)
- SSL certificates (Coolify can handle this with Let's Encrypt)

## Deployment Steps

### 1. Prepare the Repository

Push your code to a Git repository (GitHub, GitLab, etc.):

```bash
cd /home/bwilliams/TRAE/BENNIEWILLIAMS/Wagtail/benniewilliams
git init
git add .
git commit -m "Initial commit for Coolify deployment"
git remote add origin YOUR_GIT_REPO_URL
git push -u origin main
```

### 2. Configure Coolify

1. **Login to Coolify Dashboard**
   - Navigate to your Coolify instance
   - Create a new project or use existing

2. **Add New Application**
   - Click "Add Service" → "Application"
   - Choose "Docker Compose" deployment type
   - Connect your Git repository

3. **Configure Environment Variables**

   In Coolify's environment variables section, add:

   ```env
   # Django
   SECRET_KEY=<generate-secure-key>
   DEBUG=False
   DJANGO_SETTINGS_MODULE=benniewilliams.settings.production

   # Database
   DATABASE_URL=postgresql://benniewilliams:secure-password@postgres:5432/benniewilliams
   DB_NAME=benniewilliams
   DB_USER=benniewilliams
   DB_PASSWORD=secure-password
   DB_HOST=postgres
   DB_PORT=5432

   # Redis
   REDIS_URL=redis://redis:6379/0

   # Domains
   ALLOWED_HOSTS=benniewilliams.com,www.benniewilliams.com
   CSRF_TRUSTED_ORIGINS=https://benniewilliams.com,https://www.benniewilliams.com

   # Admin Account
   DJANGO_SUPERUSER_USERNAME=admin
   DJANGO_SUPERUSER_EMAIL=admin@benniewilliams.com
   DJANGO_SUPERUSER_PASSWORD=secure-admin-password

   # Email (Optional)
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

4. **Configure Docker Compose**

   Coolify should automatically detect the `docker-compose.yml` file.

   If needed, you can override with:
   ```yaml
   version: '3.8'
   services:
     web:
       build: .
       environment:
         - DATABASE_URL
         - SECRET_KEY
         - ALLOWED_HOSTS
         # ... other env vars
   ```

5. **Configure Domain & SSL**
   - Add your domain: benniewilliams.com
   - Enable SSL/TLS with Let's Encrypt
   - Configure www redirect if needed

### 3. Database Setup

Coolify can automatically provision PostgreSQL. Alternatively:

1. **Option A: Use Coolify's Database Service**
   - Add PostgreSQL service in Coolify
   - Note the connection details
   - Update DATABASE_URL accordingly

2. **Option B: Use External Database**
   - Configure DATABASE_URL with external DB credentials

### 4. Storage Configuration

For persistent storage of media files:

1. **Configure Volumes in Coolify**
   ```yaml
   volumes:
     - media:/app/media
     - static:/app/static
   ```

2. **Or use S3-compatible storage** (recommended for production):
   - Add django-storages to requirements.txt
   - Configure AWS S3 or compatible service

### 5. Deploy

1. **Initial Deployment**
   - Click "Deploy" in Coolify
   - Monitor build logs
   - Check deployment status

2. **Verify Deployment**
   - Visit https://benniewilliams.com
   - Check admin panel at /admin
   - Test all pages and functionality

### 6. Post-Deployment

1. **Create/Update Content**
   - Login to admin panel
   - Create pages if needed
   - Upload images and media

2. **Configure Backups**
   - Set up database backups in Coolify
   - Configure media file backups

3. **Monitor Application**
   - Set up health checks
   - Configure alerts
   - Monitor logs

## Coolify-Specific Configuration

### Health Check

Coolify supports health checks. Configure in docker-compose.yml:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### Resource Limits

Set appropriate resource limits:

```yaml
deploy:
  resources:
    limits:
      cpus: '1'
      memory: 1G
    reservations:
      cpus: '0.5'
      memory: 512M
```

### Scaling

For horizontal scaling:

```yaml
deploy:
  replicas: 2
```

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check DATABASE_URL format
   - Verify network connectivity between services
   - Check database credentials

2. **Static Files Not Loading**
   - Ensure STATIC_ROOT is set correctly
   - Verify whitenoise is installed
   - Check ALLOWED_HOSTS setting

3. **CSRF Token Issues**
   - Update CSRF_TRUSTED_ORIGINS
   - Ensure HTTPS is properly configured
   - Check SECURE_PROXY_SSL_HEADER

4. **Media Files Not Persisting**
   - Configure proper volumes
   - Check file permissions (user: wagtail)
   - Consider S3 storage for production

### Debug Commands

SSH into container via Coolify:

```bash
# Check migrations
python manage.py showmigrations

# Create cache table
python manage.py createcachetable

# Collect static files manually
python manage.py collectstatic --noinput

# Create superuser manually
python manage.py createsuperuser

# Check database connection
python manage.py dbshell
```

## Security Checklist

- [ ] Generate strong SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS properly
- [ ] Enable SSL/HTTPS
- [ ] Set secure passwords for database and admin
- [ ] Configure CSRF_TRUSTED_ORIGINS
- [ ] Enable security headers (HSTS, XSS, etc.)
- [ ] Set up regular backups
- [ ] Configure error tracking (Sentry)
- [ ] Implement rate limiting

## Performance Optimization

1. **Enable Redis Cache**
   - Improves page load times
   - Reduces database queries

2. **Configure CDN for Static Files**
   - Use Cloudflare or similar
   - Cache static assets

3. **Optimize Images**
   - Wagtail automatically creates responsive images
   - Consider using WebP format

4. **Database Optimization**
   - Add appropriate indexes
   - Use connection pooling
   - Regular VACUUM (PostgreSQL)

## Maintenance

### Regular Updates

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Run migrations
python manage.py migrate

# Rebuild search index
python manage.py update_index
```

### Monitoring

- Use Coolify's built-in monitoring
- Set up external monitoring (UptimeRobot, etc.)
- Configure error tracking (Sentry)
- Monitor resource usage

## Support

For issues specific to:
- **Wagtail**: https://docs.wagtail.org/
- **Coolify**: https://coolify.io/docs
- **Django**: https://docs.djangoproject.com/

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| SECRET_KEY | Django secret key | `generate-50-char-random-string` |
| DATABASE_URL | PostgreSQL connection | `postgresql://user:pass@host:5432/db` |
| ALLOWED_HOSTS | Comma-separated domains | `example.com,www.example.com` |
| DEBUG | Debug mode | `False` for production |
| REDIS_URL | Redis connection | `redis://redis:6379/0` |