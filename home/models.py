from django.db import models
from django.core.paginator import Paginator
from django import forms

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock


class StandardStreamBlock(blocks.StreamBlock):
    """Standard content blocks for pages"""
    heading = blocks.CharBlock(
        classname="full title",
        icon="title",
        template="blocks/heading.html"
    )
    paragraph = blocks.RichTextBlock(
        icon="pilcrow",
        template="blocks/paragraph.html"
    )
    image = ImageChooserBlock(
        icon="image",
        template="blocks/image.html"
    )
    block_quote = blocks.BlockQuoteBlock(
        icon="openquote",
        template="blocks/blockquote.html"
    )
    embed = EmbedBlock(
        icon="media",
        template="blocks/embed.html"
    )
    raw_html = blocks.RawHTMLBlock(
        icon="code",
        template="blocks/raw_html.html"
    )
    code = blocks.StructBlock([
        ('language', blocks.ChoiceBlock(choices=[
            ('python', 'Python'),
            ('javascript', 'JavaScript'),
            ('html', 'HTML'),
            ('css', 'CSS'),
            ('bash', 'Bash'),
        ], default='python')),
        ('code', blocks.TextBlock()),
    ], icon="code", template="blocks/code.html")


class HomePage(Page):
    """Home page model"""
    hero_title = models.CharField(
        max_length=255,
        default="Bennie Williams",
        help_text="Hero section title"
    )
    hero_subtitle = models.CharField(
        max_length=500,
        default="AI Consultant & Educator",
        help_text="Hero section subtitle"
    )
    hero_cta_text = models.CharField(
        max_length=100,
        default="Work With Me",
        help_text="Hero CTA button text"
    )
    hero_cta_link = models.URLField(
        blank=True,
        help_text="Hero CTA button link"
    )

    intro = RichTextField(blank=True)

    body = StreamField(
        StandardStreamBlock(),
        blank=True,
        use_json_field=True
    )

    featured_blog_post = models.ForeignKey(
        'home.BlogPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_cta_text'),
            FieldPanel('hero_cta_link'),
        ], heading="Hero Section"),
        FieldPanel('intro'),
        FieldPanel('body'),
        PageChooserPanel('featured_blog_post', 'home.BlogPage'),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        # Get recent blog posts
        blog_pages = BlogPage.objects.live().order_by('-first_published_at')[:3]
        context['recent_posts'] = blog_pages

        # Get featured courses
        courses = Course.objects.filter(featured=True)[:3]
        context['featured_courses'] = courses

        return context


class BlogIndexPage(Page):
    """Blog index page model"""
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        # Get all blog posts
        blogpages = self.get_children().live().order_by('-first_published_at')

        # Paginate
        paginator = Paginator(blogpages, 12)
        page_number = request.GET.get("page")
        blog_pages = paginator.get_page(page_number)

        context['blog_pages'] = blog_pages

        # Get tags for sidebar
        all_tags = BlogPageTag.objects.all()
        tag_counts = {}
        for tag in all_tags:
            if tag.tag.name in tag_counts:
                tag_counts[tag.tag.name] += 1
            else:
                tag_counts[tag.tag.name] = 1
        context['tags'] = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogPage(Page):
    """Blog post page model"""
    date = models.DateField("Post date")
    author = models.CharField(max_length=255, default="Bennie Williams")

    intro = models.CharField(max_length=500)
    body = StreamField(
        StandardStreamBlock(),
        use_json_field=True
    )

    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
        index.SearchField('author'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('author'),
            FieldPanel('tags'),
        ], heading="Blog information"),
        FieldPanel('featured_image'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        # Get related posts (same tags)
        if self.tags.all():
            related_posts = BlogPage.objects.live().exclude(id=self.id).filter(
                tags__in=self.tags.all()
            ).distinct().order_by('-first_published_at')[:3]
        else:
            related_posts = BlogPage.objects.live().exclude(
                id=self.id
            ).order_by('-first_published_at')[:3]

        context['related_posts'] = related_posts
        return context


class Course(models.Model):
    """Course snippet for courses listing"""
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=500, blank=True)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    gumroad_link = models.URLField(help_text="Gumroad purchase link")
    youtube_preview_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="YouTube video ID for preview (unlisted)"
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    panels = [
        FieldPanel('title'),
        FieldPanel('subtitle'),
        FieldPanel('description'),
        FieldPanel('price'),
        FieldPanel('gumroad_link'),
        FieldPanel('youtube_preview_id'),
        FieldPanel('image'),
        FieldPanel('featured'),
        FieldPanel('order'),
    ]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', 'title']


class CoursesPage(Page):
    """Courses listing page"""
    intro = RichTextField(blank=True)
    body = StreamField(
        StandardStreamBlock(),
        blank=True,
        use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        courses = Course.objects.all().order_by('order', 'title')
        context['courses'] = courses
        return context


class ServicesPage(Page):
    """Services page"""
    intro = RichTextField(blank=True)
    body = StreamField(
        StandardStreamBlock(),
        blank=True,
        use_json_field=True
    )

    consultation_price = models.CharField(
        max_length=100,
        default="$250/hour",
        help_text="Consultation pricing"
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('consultation_price'),
    ]


class AboutPage(Page):
    """About page"""
    intro = RichTextField(blank=True)
    body = StreamField(
        StandardStreamBlock(),
        blank=True,
        use_json_field=True
    )

    profile_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('profile_image'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]


class ContactPage(Page):
    """Contact page"""
    intro = RichTextField(blank=True)
    email = models.EmailField(default="bennie@benniewilliams.com")
    thank_you_text = RichTextField(
        blank=True,
        help_text="Text to display after form submission"
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('email'),
        FieldPanel('thank_you_text'),
    ]