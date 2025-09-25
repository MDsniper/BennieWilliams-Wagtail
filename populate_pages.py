"""
Script to populate About and Services pages
Run with: python manage.py shell < populate_pages.py
"""

from wagtail.models import Page
from home.models import HomePage, AboutPage, ServicesPage

def create_pages():
    # Get the home page
    home = HomePage.objects.first()

    if not home:
        print("No HomePage found. Please run populate_content.py first.")
        return

    # Create About Page
    try:
        about = AboutPage.objects.get(slug='about')
        print(f"AboutPage already exists: {about.title}")
    except AboutPage.DoesNotExist:
        about = AboutPage(
            title="About",
            slug="about",
            intro="<p>Learn about Bennie Williams, a technology consultant with a unique background in the Navy, healthcare IT, and a passion for helping businesses succeed through strategic technology.</p>",
            profile_statement="Currently providing senior infrastructure consulting through Oracle at Children's National Hospital. Previously served as IT Manager at CNH from 2018-2023, managing data center and system management teams. My journey from Navy service through Accenture's global infrastructure management has given me a unique perspective on solving complex technology challenges.",
        )
        home.add_child(instance=about)
        about.save()
        print(f"Created AboutPage: {about.title}")

    # Create Services Page
    try:
        services = ServicesPage.objects.get(slug='services')
        print(f"ServicesPage already exists: {services.title}")
    except ServicesPage.DoesNotExist:
        services = ServicesPage(
            title="Services",
            slug="services",
            intro="<p>From strategic planning to implementation, I provide end-to-end technology solutions tailored to your unique business needs.</p>",
        )
        home.add_child(instance=services)
        services.save()
        print(f"Created ServicesPage: {services.title}")

    print("\nPages created successfully!")

# Run the population
try:
    create_pages()
except Exception as e:
    print(f"Error creating pages: {e}")