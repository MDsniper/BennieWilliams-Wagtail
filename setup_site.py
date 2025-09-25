from wagtail.models import Site, Page
from home.models import HomePage

# Get or create the home page
home = HomePage.objects.first()
if home:
    print(f"Found HomePage: {home.title}")

    # Check if a site exists
    site = Site.objects.first()
    if not site:
        # Create a site
        site = Site(
            hostname='localhost',
            port=8000,
            root_page=home,
            is_default_site=True
        )
        site.save()
        print(f"Created new site: {site.hostname}:{site.port}")
    else:
        # Update the existing site
        site.root_page = home
        site.hostname = 'localhost'
        site.port = 8000
        site.is_default_site = True
        site.save()
        print(f"Updated site: {site.hostname}:{site.port} -> {site.root_page.title}")
else:
    print("No HomePage found. Please run populate_content.py first.")