# Bennie Williams - Django/Wagtail Site

A production-ready Django + Wagtail site for Bennie Williams (benniewilliams.com), featuring a personal blog and AI consulting landing page with integrated Gumroad course sales.

## Features

- **Blog System**: Full-featured blog with tagging, pagination, and related posts
- **Course Integration**: Gumroad-powered course sales with YouTube previews
- **Navy Theme**: Custom CSS with professional navy color scheme
- **Dockerized**: Complete Docker setup for development and production
- **CI/CD**: GitHub Actions for automated testing and deployment
- **SEO Optimized**: Sitemap, meta tags, and structured data support
- **Responsive Design**: Mobile-first, accessible design

## Tech Stack

- Python 3.12
- Django 5.x
- Wagtail 6.x
- PostgreSQL
- Docker & Docker Compose
- GitHub Actions
- WhiteNoise for static files
- Gunicorn WSGI server

## Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/MDsniper/BennieWilliams-Wagtail.git
cd BennieWilliams-Wagtail
```

2. **Copy environment variables**
```bash
cp .env.example .env
# Edit .env with your settings
```

3. **Start with Docker Compose**
```bash
docker-compose up -d --build
```

4. **Access the site**
- Site: http://localhost:8000
- Admin: http://localhost:8000/admin
- Default credentials: admin/changeme (from .env)

### Manual Setup (without Docker)

1. **Create virtual environment**
```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up database**
```bash
python manage.py migrate
python manage.py createsuperuser
```

4. **Collect static files**
```bash
python manage.py collectstatic
```

5. **Run development server**
```bash
python manage.py runserver
```

## Deployment to Coolify

### Method 1: Using GitHub Repository

1. **In Coolify Dashboard**:
   - Add New Resource → Public Repository
   - Repository URL: `https://github.com/MDsniper/BennieWilliams-Wagtail`
   - Branch: `main`
   - Build Pack: Dockerfile

2. **Configure Environment Variables**:
   ```env
   SECRET_KEY=your-production-secret-key
   DEBUG=0
   DATABASE_URL=postgres://user:pass@host:5432/dbname
   ALLOWED_HOSTS=benniewilliams.com,www.benniewilliams.com
   ```

3. **Deploy**:
   - Click Deploy
   - Coolify will build from Dockerfile and start the container

### Method 2: Using GHCR Image

1. **Configure GitHub Secrets**:
   - Go to Settings → Secrets → Actions
   - Add `COOLIFY_WEBHOOK_URL` with your Coolify webhook

2. **In Coolify**:
   - Add New Resource → Docker Image
   - Image: `ghcr.io/mdsniper/benniewilliams-wagtail:latest`
   - Configure environment variables as above

3. **Set up GHCR Authentication** (if private):
   - Username: Your GitHub username
   - Password: GitHub Personal Access Token with `read:packages` scope

## Managing Content

### Creating Pages

1. Log in to Wagtail admin at `/admin`
2. Navigate to Pages → Add child page
3. Select page type (Blog, Services, About, etc.)
4. Fill in content and publish

### Adding Courses

1. Go to Snippets → Courses in admin
2. Click "Add Course"
3. Enter course details including Gumroad link
4. Set as featured to show on homepage

### Managing Blog Posts

1. Navigate to Blog section in Pages
2. Add child page → Blog Page
3. Add title, content, tags, and featured image
4. Publish or schedule for later

## Database Management

### Backup Database
```bash
docker-compose exec db pg_dump -U postgres postgres > backup.sql
```

### Restore Database
```bash
docker-compose exec -T db psql -U postgres postgres < backup.sql
```

### Run Migrations
```bash
docker-compose exec web python manage.py migrate
```

## Seed Sample Data

```bash
# Using Docker
docker-compose exec web python manage.py seed_data

# Without Docker
python manage.py seed_data
```

This creates:
- Homepage with hero section
- Blog index page with 6 sample posts
- 2 featured courses
- About and Services pages
- Contact page

## Testing

### Run Tests
```bash
# With Docker
docker-compose exec web python manage.py test

# Without Docker
python manage.py test
```

### Run Linting
```bash
# Check code style
flake8 .

# Format code
black .
```

## CI/CD Pipeline

### GitHub Actions Workflows

1. **Docker Build & Push** (`docker.yml`)
   - Triggers on push to main and tags
   - Builds multi-platform images
   - Pushes to GitHub Container Registry
   - Optional Coolify webhook trigger

2. **Django Tests** (`django-tests.yml`)
   - Runs on all PRs and pushes
   - Python compilation check
   - Flake8 linting
   - Django system checks
   - Unit tests with PostgreSQL

### Setting up Deployment Webhook

1. Get webhook URL from Coolify deployment settings
2. Add to GitHub Secrets as `COOLIFY_WEBHOOK_URL`
3. Pushes to main will trigger auto-deployment

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Required in production |
| `DEBUG` | Debug mode | `1` (dev), `0` (prod) |
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | Required |
| `DJANGO_SUPERUSER_*` | Auto-create superuser | Optional |
| `GUMROAD_URL` | Gumroad store URL | Optional |
| `AWS_*` | S3 configuration | Optional |
| `EMAIL_*` | SMTP configuration | Optional |
| `GOOGLE_ANALYTICS_ID` | GA tracking ID | Optional |
| `PLAUSIBLE_DOMAIN` | Plausible analytics | Optional |

## Security Checklist

- [ ] Set `DEBUG=0` in production
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable HTTPS (handle in Coolify/reverse proxy)
- [ ] Set secure headers (HSTS, CSP)
- [ ] Regular dependency updates
- [ ] Database backups configured
- [ ] Error monitoring (Sentry optional)

## Troubleshooting

### Container won't start
- Check logs: `docker-compose logs web`
- Verify .env file exists and is configured
- Ensure ports 8000 and 5432 are available

### Static files not loading
- Run: `docker-compose exec web python manage.py collectstatic --noinput`
- Check STATIC_ROOT and STATIC_URL settings
- Verify WhiteNoise middleware is installed

### Database connection errors
- Verify DATABASE_URL is correct
- Check if database container is running: `docker-compose ps`
- Try recreating database: `docker-compose down -v && docker-compose up -d`

### Admin login not working
- Recreate superuser: `docker-compose exec web python manage.py createsuperuser`
- Check DJANGO_SUPERUSER_* environment variables

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## License

This project is proprietary software for Bennie Williams.

## Contact

- Website: [benniewilliams.com](https://benniewilliams.com)
- Email: bennie@benniewilliams.com
- GitHub: [@benniewilliams](https://github.com/benniewilliams)