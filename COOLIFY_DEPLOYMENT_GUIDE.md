# Complete Coolify Deployment Guide for Bennie Williams Wagtail Site

## 🚀 Quick Deployment Summary

**Ready for Production**: ✅ All critical issues fixed
**Estimated Deployment Time**: 15-20 minutes
**Architecture**: Docker Compose with PostgreSQL + Redis + Wagtail/Django

---

## 📋 Pre-Deployment Checklist

### ✅ Repository Status - READY
- [x] **Dockerfile optimized** - Multi-stage build with security best practices
- [x] **Health checks implemented** - `/health/` and `/ready/` endpoints
- [x] **Production settings configured** - Proper Django production settings
- [x] **Static file handling** - WhiteNoise for efficient static serving
- [x] **Security headers** - HTTPS, HSTS, XSS protection enabled
- [x] **Database migrations** - Automatic migration on startup
- [x] **Admin user creation** - Automatic superuser creation
- [x] **Service dependencies** - Proper PostgreSQL and Redis health checks

### 🔧 Fixed Critical Issues
- [x] **Health check endpoint created** - Docker health check now works
- [x] **Proper health check method** - Using curl instead of requests library
- [x] **Coolify-optimized docker-compose** - Resource limits and proper configuration
- [x] **Environment template** - Complete production environment variables

---

## 🎯 Deployment Steps

### Step 1: Prepare Repository for Coolify

1. **Commit the latest changes** (if not already done):
```bash
cd /home/bwilliams/TRAE/BENNIEWILLIAMS/Wagtail/benniewilliams
git add .
git commit -m "Add Coolify deployment configuration and health checks"
git push origin main
```

### Step 2: Configure Coolify Application

1. **Login to your Coolify dashboard**
2. **Create new application**:
   - Click **"New Resource"** → **"Application"**
   - Choose **"Docker Compose"** as deployment type
   - Connect to your GitHub repository: `https://github.com/MDsniper/benniewilliams-wagtail`
   - Set branch to `main`

3. **Configure build settings**:
   - **Docker Compose file**: Use `docker-compose.coolify.yml` (or rename `docker-compose.yml`)
   - **Build pack**: Docker Compose
   - **Port**: 8000

### Step 3: Environment Variables Configuration

**CRITICAL**: Copy these environment variables to Coolify:

```bash
# SECURITY - CHANGE THESE VALUES!
SECRET_KEY=generate-a-50-character-random-string-here
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@benniewilliams.com
DJANGO_SUPERUSER_PASSWORD=your-secure-admin-password
DB_PASSWORD=your-secure-database-password

# DOMAIN CONFIGURATION - UPDATE WITH YOUR DOMAIN
ALLOWED_HOSTS=benniewilliams.com,www.benniewilliams.com
CSRF_TRUSTED_ORIGINS=https://benniewilliams.com,https://www.benniewilliams.com
WAGTAILADMIN_BASE_URL=https://benniewilliams.com

# CORE SETTINGS
DEBUG=False
DJANGO_SETTINGS_MODULE=benniewilliams.settings.production
DATABASE_URL=postgresql://benniewilliams:your-secure-database-password@db:5432/benniewilliams
REDIS_URL=redis://redis:6379/0

# OPTIONAL - EMAIL CONFIGURATION
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@benniewilliams.com
```

**🔐 Generate Secure SECRET_KEY**:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 4: Domain and SSL Configuration

1. **Add your domain** in Coolify:
   - Go to **Domains** tab
   - Add `benniewilliams.com`
   - Add `www.benniewilliams.com` (optional)

2. **Configure SSL/TLS**:
   - Enable **"Generate SSL Certificate"**
   - Choose **"Let's Encrypt"**
   - Enable **"Force HTTPS redirect"**

### Step 5: Storage Configuration

Coolify will automatically create volumes for:
- `postgres_data` - Database persistence
- `redis_data` - Cache persistence
- `media_data` - User uploads (images, documents)
- `static_data` - CSS, JS, images

### Step 6: Deploy Application

1. **Initial deployment**:
   - Click **"Deploy"**
   - Monitor build logs for any errors
   - Wait for all services to become healthy

2. **Verify deployment**:
   - Check service status: All should be "Running"
   - Test health endpoint: `https://your-domain.com/health/`
   - Access admin panel: `https://your-domain.com/admin/`

---

## 🔍 Post-Deployment Verification

### Health Check Endpoints

```bash
# Basic health check
curl https://benniewilliams.com/health/
# Should return: {"status":"healthy","database":"healthy","cache":"healthy","application":"benniewilliams-wagtail"}

# Detailed readiness check
curl https://benniewilliams.com/ready/
# Should return: {"status":"ready","checks":{"database":"ready","static_files":"ready","cache":"ready"},"application":"benniewilliams-wagtail"}
```

### Access Points

- **Main site**: https://benniewilliams.com
- **Admin panel**: https://benniewilliams.com/admin/
- **Django admin**: https://benniewilliams.com/django-admin/
- **Health check**: https://benniewilliams.com/health/
- **Search**: https://benniewilliams.com/search/

### Initial Setup

1. **Login to admin**: Use credentials from `DJANGO_SUPERUSER_*` environment variables
2. **Configure Wagtail site**: Go to Settings → Sites, update the site domain
3. **Create content**: Add pages, upload images, configure site structure

---

## 📊 Monitoring & Maintenance

### Resource Usage
- **CPU**: 0.5-2.0 cores (configured with limits)
- **RAM**: 512MB-2GB (web app), 256MB-1GB (database), 128MB-512MB (Redis)
- **Storage**: Persistent volumes for data, media, and static files

### Backup Configuration
1. **Database backups**: Configure in Coolify dashboard
2. **Media files**: Consider S3 integration for production
3. **Application code**: Maintained in Git repository

### Log Monitoring
```bash
# Via Coolify dashboard
- Application logs: Real-time container logs
- Build logs: Deployment and build information
- System metrics: CPU, memory, network usage

# Health monitoring
- Built-in health checks every 30 seconds
- Automatic restart on health check failures
- Integration with Coolify alerting
```

---

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. Health Check Failures
**Symptom**: Container keeps restarting, health check fails
```bash
# Check logs for errors
# Verify database connectivity
# Ensure all environment variables are set
```

#### 2. Static Files Not Loading
**Solution**:
- Verify `ALLOWED_HOSTS` includes your domain
- Check that `whitenoise` is properly configured
- Ensure static files were collected during build

#### 3. Database Connection Errors
**Check**:
- `DATABASE_URL` format is correct
- Database service is healthy
- Network connectivity between services

#### 4. CSRF Token Errors
**Fix**:
- Update `CSRF_TRUSTED_ORIGINS` with HTTPS URLs
- Ensure SSL is properly configured
- Verify domain matches exactly

#### 5. Admin Login Issues
**Verify**:
- Superuser was created (check logs)
- Credentials match environment variables
- Database migrations completed successfully

---

## 🔧 Advanced Configuration

### Performance Optimization

1. **Enable Redis caching** (already configured):
```python
# In production.py - already set
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379/0',
    }
}
```

2. **Database connection pooling** (already configured):
```python
# In production.py - already set
DATABASES = {
    'default': dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    )
}
```

3. **Static file compression** (already configured):
```python
# WhiteNoise with compression - already set
STORAGES["staticfiles"]["BACKEND"] = "whitenoise.storage.CompressedManifestStaticFilesStorage"
```

### Security Enhancements

All security settings are already configured:
- ✅ HTTPS redirect
- ✅ Secure cookies
- ✅ HSTS headers
- ✅ XSS protection
- ✅ Content type sniffing protection
- ✅ Frame options (clickjacking protection)

### Scaling Options

**Horizontal scaling** (multiple instances):
```yaml
# In docker-compose.coolify.yml
deploy:
  replicas: 2  # Run 2 instances of the web service
```

**Vertical scaling** (more resources):
```yaml
# Already configured with resource limits
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 2G
```

---

## 🎉 Deployment Complete!

Your Wagtail site is now ready for production with:

- ✅ **High Availability**: Health checks and automatic restarts
- ✅ **Security**: HTTPS, secure headers, and production hardening
- ✅ **Performance**: Redis caching, static file optimization
- ✅ **Monitoring**: Health endpoints and logging
- ✅ **Scalability**: Resource limits and scaling options
- ✅ **Maintenance**: Automated migrations and admin user creation

**Next Steps**:
1. Add content through the admin panel
2. Configure backups in Coolify
3. Set up monitoring alerts
4. Consider CDN for static assets (optional)

---

## 📞 Support Resources

- **Wagtail Documentation**: https://docs.wagtail.org/
- **Django Documentation**: https://docs.djangoproject.com/
- **Coolify Documentation**: https://coolify.io/docs
- **PostgreSQL Guide**: https://www.postgresql.org/docs/
- **Redis Documentation**: https://redis.io/docs/

For deployment-specific issues, check the Coolify logs and container health status first.