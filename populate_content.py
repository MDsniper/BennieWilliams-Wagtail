"""
Script to populate initial content for Bennie Williams site
Run with: python manage.py shell < populate_content.py
"""

from wagtail.models import Site, Page
from home.models import HomePage, BlogIndexPage, BlogPage, ContactPage, ProjectPage

def create_initial_content():
    # Get the root page
    root = Page.objects.get(id=1)

    # Get the default home page that was created or find any HomePage
    home = HomePage.objects.first()

    # If no home page exists, get the first page under root and check if it's the welcome page
    if not home:
        # Get the existing page that's likely the default home
        existing_pages = root.get_children()
        if existing_pages:
            default_page = existing_pages.first()
            # Create a proper HomePage
            home = HomePage(
                title="Bennie Williams Consulting",
                slug="home",
                hero_title = "Strategic Technology Leadership & Innovation",
                hero_subtitle = "Hi, I'm Bennie Williams. I help businesses navigate the complex landscape of modern technology, from AI and automation to cloud infrastructure and digital transformation."
            )
            # Replace the default page
            root.add_child(instance=home)
            home.save()
            print(f"Created new HomePage: {home.title}")
        else:
            print("No existing pages found, creating new home page")
            home = HomePage(
                title="Bennie Williams Consulting",
                slug="home",
                hero_title = "Strategic Technology Leadership & Innovation",
                hero_subtitle = "Hi, I'm Bennie Williams. I help businesses navigate the complex landscape of modern technology, from AI and automation to cloud infrastructure and digital transformation."
            )
            root.add_child(instance=home)
            home.save()
            print(f"Created HomePage: {home.title}")

    if home:
        home.title = "Bennie Williams Consulting"
        home.hero_title = "Strategic Technology Leadership & Innovation"
        home.hero_subtitle = "Hi, I'm Bennie Williams. I help businesses navigate the complex landscape of modern technology, from AI and automation to cloud infrastructure and digital transformation."
        home.save()
        print(f"Updated HomePage: {home.title}")

    # Create Blog Index Page
    try:
        blog_index = BlogIndexPage.objects.get(slug='blog')
    except BlogIndexPage.DoesNotExist:
        blog_index = BlogIndexPage(
            title="Blog & Insights",
            slug="blog",
            intro="<p>Stay informed with practical insights on technology strategy, AI implementation, and digital transformation.</p>"
        )
        home.add_child(instance=blog_index)
        blog_index.save()
        print(f"Created BlogIndexPage: {blog_index.title}")

    # Create sample blog posts
    blog_posts = [
        {
            'title': 'The Future of Enterprise AI: What Leaders Need to Know',
            'slug': 'future-of-enterprise-ai',
            'intro': 'Explore the transformative potential of AI in enterprise environments',
            'date': '2024-01-15',
            'tags': 'AI Strategy, Enterprise, Digital Transformation',
        },
        {
            'title': 'Mastering Prompt Engineering for Business Applications',
            'slug': 'mastering-prompt-engineering',
            'intro': 'Discover advanced techniques for crafting effective prompts',
            'date': '2024-01-10',
            'tags': 'AI Training, Prompt Engineering, LLM',
        },
        {
            'title': 'VMware vSphere 8.0: Key Features for Modern Infrastructure',
            'slug': 'vmware-vsphere-8',
            'intro': 'A comprehensive guide to the latest VMware vSphere features',
            'date': '2024-01-05',
            'tags': 'Infrastructure, VMware, Virtualization',
        }
    ]

    if blog_index:
        for post_data in blog_posts:
            try:
                blog = BlogPage.objects.get(slug=post_data['slug'])
                print(f"BlogPage already exists: {blog.title}")
            except BlogPage.DoesNotExist:
                blog = BlogPage(
                    title=post_data['title'],
                    slug=post_data['slug'],
                    intro=post_data['intro'],
                    date=post_data['date'],
                    tags=post_data['tags'],
                )
                blog_index.add_child(instance=blog)
                blog.save()
                print(f"Created BlogPage: {blog.title}")

    # Create Contact Page
    try:
        contact = ContactPage.objects.get(slug='contact')
    except ContactPage.DoesNotExist:
        contact = ContactPage(
            title="Contact",
            slug="contact",
            intro="<p>Let's discuss how strategic technology solutions can drive your business forward. Schedule a consultation to explore the possibilities.</p>",
            email="consulting@benniewilliams.com",
        )
        home.add_child(instance=contact)
        contact.save()
        print(f"Created ContactPage: {contact.title}")

    # Create sample project pages
    projects = [
        {
            'title': 'Healthcare Infrastructure Modernization',
            'slug': 'healthcare-infrastructure',
            'summary': "Led the modernization of Children's National Hospital's data center infrastructure, improving efficiency by 40% and reducing operational costs.",
            'technologies': 'VMware vSphere, Cloud Architecture, Infrastructure as Code, Automation',
            'client': "Children's National Hospital",
        },
        {
            'title': 'Global Data Center Management at Accenture',
            'slug': 'accenture-global-dc',
            'summary': 'Managed 17 global data centers as VMware Subject Matter Expert, implementing FinOps initiatives that saved Fortune 500 clients millions in operational costs.',
            'technologies': 'VMware, FinOps, Cloud Cost Optimization, Global Team Leadership',
            'client': 'Accenture',
        }
    ]

    for project_data in projects:
        try:
            project = ProjectPage.objects.get(slug=project_data['slug'])
            print(f"ProjectPage already exists: {project.title}")
        except ProjectPage.DoesNotExist:
            project = ProjectPage(
                title=project_data['title'],
                slug=project_data['slug'],
                summary=project_data['summary'],
                technologies=project_data['technologies'],
                client=project_data['client'],
            )
            home.add_child(instance=project)
            project.save()
            print(f"Created ProjectPage: {project.title}")

# Run the population
try:
    create_initial_content()
    print("\nContent population complete!")
except Exception as e:
    print(f"Error populating content: {e}")