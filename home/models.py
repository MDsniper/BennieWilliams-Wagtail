from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.models import Image
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


# StreamField blocks for flexible content
class HeroBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=200)
    subheading = blocks.CharBlock(max_length=500, required=False)
    image = ImageChooserBlock(required=False)
    cta_text = blocks.CharBlock(max_length=100, required=False)
    cta_link = blocks.URLBlock(required=False)

    class Meta:
        template = 'blocks/hero.html'
        icon = 'image'
        label = 'Hero Section'


class PortfolioItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=200)
    description = blocks.RichTextBlock()
    image = ImageChooserBlock()
    project_link = blocks.URLBlock(required=False)
    github_link = blocks.URLBlock(required=False)
    technologies = blocks.ListBlock(blocks.CharBlock(max_length=50))

    class Meta:
        template = 'blocks/portfolio_item.html'
        icon = 'folder-inverse'
        label = 'Portfolio Item'


class AboutBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=200)
    content = blocks.RichTextBlock()
    image = ImageChooserBlock(required=False)
    skills = blocks.ListBlock(
        blocks.StructBlock([
            ('name', blocks.CharBlock(max_length=100)),
            ('level', blocks.IntegerBlock(min_value=0, max_value=100)),
        ])
    )

    class Meta:
        template = 'blocks/about.html'
        icon = 'user'
        label = 'About Section'


class HomePage(Page):
    """Landing page with hero, portfolio, and about sections"""

    hero_title = models.CharField(
        max_length=255,
        default="Bennie Williams",
        help_text="Main heading for the hero section"
    )
    hero_subtitle = models.CharField(
        max_length=500,
        blank=True,
        help_text="Subtitle or tagline"
    )

    content = StreamField([
        ('hero', HeroBlock()),
        ('about', AboutBlock()),
        ('portfolio', blocks.ListBlock(PortfolioItemBlock())),
        ('rich_text', blocks.RichTextBlock()),
        ('raw_html', blocks.RawHTMLBlock()),
    ], null=True, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
        ], heading="Hero Section"),
        FieldPanel('content'),
    ]

    class Meta:
        verbose_name = "Homepage"


class BlogIndexPage(Page):
    """Index page for blog posts"""

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        blog_posts = self.get_children().live().order_by('-first_published_at')
        context['blog_posts'] = blog_posts
        return context

    class Meta:
        verbose_name = "Blog Index"


class BlogPage(Page):
    """Individual blog post page"""

    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('code', blocks.TextBlock()),
        ('quote', blocks.BlockQuoteBlock()),
        ('embed', blocks.URLBlock()),
    ], use_json_field=True)

    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")

    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('featured_image'),
        FieldPanel('body'),
        FieldPanel('tags'),
    ]

    class Meta:
        verbose_name = "Blog Post"


class ProjectPage(Page):
    """Detailed project page"""

    summary = models.CharField(max_length=500)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    client = models.CharField(max_length=255, blank=True)

    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    technologies = models.TextField(
        help_text="Technologies used (comma-separated)",
        blank=True
    )

    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content = StreamField([
        ('overview', blocks.RichTextBlock()),
        ('features', blocks.ListBlock(blocks.CharBlock(max_length=255))),
        ('gallery', blocks.ListBlock(ImageChooserBlock())),
        ('code_snippet', blocks.StructBlock([
            ('language', blocks.ChoiceBlock(choices=[
                ('python', 'Python'),
                ('javascript', 'JavaScript'),
                ('html', 'HTML/CSS'),
                ('bash', 'Bash'),
            ])),
            ('code', blocks.TextBlock()),
        ])),
        ('testimonial', blocks.StructBlock([
            ('quote', blocks.TextBlock()),
            ('author', blocks.CharBlock(max_length=255)),
            ('role', blocks.CharBlock(max_length=255, required=False)),
        ])),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('summary'),
        MultiFieldPanel([
            FieldPanel('start_date'),
            FieldPanel('end_date'),
            FieldPanel('client'),
        ], heading="Project Details"),
        MultiFieldPanel([
            FieldPanel('project_url'),
            FieldPanel('github_url'),
        ], heading="Links"),
        FieldPanel('technologies'),
        FieldPanel('featured_image'),
        FieldPanel('content'),
    ]

    class Meta:
        verbose_name = "Project"


class AboutPage(Page):
    """About page with career timeline and expertise"""

    intro = RichTextField(blank=True)
    profile_statement = models.TextField(
        help_text="Main profile/introduction statement",
        blank=True
    )

    career_timeline = StreamField([
        ('milestone', blocks.StructBlock([
            ('year', blocks.CharBlock(max_length=50)),
            ('title', blocks.CharBlock(max_length=255)),
            ('organization', blocks.CharBlock(max_length=255, required=False)),
            ('description', blocks.TextBlock()),
        ])),
    ], blank=True, use_json_field=True)

    expertise_areas = StreamField([
        ('skill', blocks.StructBlock([
            ('area', blocks.CharBlock(max_length=100)),
            ('level', blocks.IntegerBlock(min_value=0, max_value=100)),
        ])),
    ], blank=True, use_json_field=True)

    values = StreamField([
        ('value', blocks.StructBlock([
            ('icon', blocks.CharBlock(max_length=5)),
            ('title', blocks.CharBlock(max_length=100)),
            ('description', blocks.TextBlock()),
        ])),
    ], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('profile_statement'),
        FieldPanel('career_timeline'),
        FieldPanel('expertise_areas'),
        FieldPanel('values'),
    ]

    class Meta:
        verbose_name = "About Page"


class ServicesPage(Page):
    """Services overview page"""

    intro = RichTextField(blank=True)

    services = StreamField([
        ('service', blocks.StructBlock([
            ('icon', blocks.CharBlock(max_length=5)),
            ('title', blocks.CharBlock(max_length=200)),
            ('description', blocks.RichTextBlock()),
            ('features', blocks.ListBlock(blocks.CharBlock(max_length=255))),
        ])),
    ], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('services'),
    ]

    class Meta:
        verbose_name = "Services Page"


class ContactPage(Page):
    """Contact page with form"""

    intro = RichTextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    social_links = StreamField([
        ('social', blocks.StructBlock([
            ('platform', blocks.ChoiceBlock(choices=[
                ('github', 'GitHub'),
                ('linkedin', 'LinkedIn'),
                ('twitter', 'Twitter'),
                ('instagram', 'Instagram'),
                ('youtube', 'YouTube'),
            ])),
            ('url', blocks.URLBlock()),
        ])),
    ], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        MultiFieldPanel([
            FieldPanel('email'),
            FieldPanel('phone'),
            FieldPanel('address'),
        ], heading="Contact Information"),
        FieldPanel('social_links'),
    ]

    class Meta:
        verbose_name = "Contact Page"
