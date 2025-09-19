from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from wagtail.models import Site, Page
from home.models import (
    HomePage, BlogIndexPage, BlogPage, Course,
    CoursesPage, ServicesPage, AboutPage, ContactPage
)
from datetime import date, timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with sample data for development'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database with sample data...')

        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('changeme')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        # Get root page
        root_page = Page.objects.get(id=1)

        # Check if home page already exists
        if not HomePage.objects.exists():
            # Delete default home page if it exists
            try:
                default_home = Page.objects.get(id=2)
                default_home.delete()
            except Page.DoesNotExist:
                pass

            # Create Home Page
            home_page = HomePage(
                title='Home',
                slug='home',
                hero_title='Bennie Williams',
                hero_subtitle='AI Consultant & Educator - Transforming Businesses with Artificial Intelligence',
                hero_cta_text='Start Your AI Journey',
                hero_cta_link='/contact/',
                intro='<p>Welcome to my digital space where I share insights on AI implementation, '
                      'machine learning strategies, and practical guides for businesses looking to '
                      'leverage artificial intelligence for growth and innovation.</p>',
            )
            root_page.add_child(instance=home_page)
            home_page.save_revision().publish()

            # Update site root page
            site = Site.objects.get(is_default_site=True)
            site.root_page = home_page
            site.save()

            self.stdout.write(self.style.SUCCESS('Created home page'))
        else:
            home_page = HomePage.objects.first()

        # Create Blog Index Page
        if not BlogIndexPage.objects.exists():
            blog_index = BlogIndexPage(
                title='Blog',
                slug='blog',
                intro='<p>Insights, tutorials, and thoughts on artificial intelligence, '
                      'machine learning, and the future of technology in business.</p>',
            )
            home_page.add_child(instance=blog_index)
            blog_index.save_revision().publish()
            self.stdout.write(self.style.SUCCESS('Created blog index page'))
        else:
            blog_index = BlogIndexPage.objects.first()

        # Create Blog Posts
        blog_posts = [
            {
                'title': 'Getting Started with GPT-4 for Business Applications',
                'intro': 'Learn how to integrate GPT-4 into your business workflows for maximum efficiency.',
                'tags': ['ai', 'gpt-4', 'business', 'automation'],
                'content': '''
                <p>GPT-4 represents a paradigm shift in how businesses can leverage artificial intelligence.
                In this comprehensive guide, we'll explore practical applications and implementation strategies.</p>

                <h3>Understanding GPT-4 Capabilities</h3>
                <p>GPT-4 offers unprecedented natural language understanding and generation capabilities.
                From customer service automation to content creation, the possibilities are vast.</p>

                <h3>Implementation Best Practices</h3>
                <p>Start small with pilot projects, measure ROI carefully, and scale gradually.
                Focus on high-impact, repetitive tasks that benefit from AI augmentation.</p>

                <h3>Common Use Cases</h3>
                <ul>
                <li>Customer support automation</li>
                <li>Content generation and optimization</li>
                <li>Data analysis and insights</li>
                <li>Code generation and review</li>
                </ul>
                '''
            },
            {
                'title': 'Building RAG Systems: A Practical Guide',
                'intro': 'Retrieval-Augmented Generation systems combine the best of search and AI generation.',
                'tags': ['rag', 'ai', 'llm', 'vector-database'],
                'content': '''
                <p>RAG systems are revolutionizing how we build AI applications that need access to
                proprietary or real-time data. Let's dive into the architecture and implementation.</p>

                <h3>Core Components</h3>
                <p>A RAG system consists of three main components: document processing pipeline,
                vector database for similarity search, and an LLM for generation.</p>

                <h3>Vector Databases Compared</h3>
                <p>Choose between Pinecone, Weaviate, or Chroma based on your scale requirements,
                budget constraints, and integration needs.</p>

                <h3>Optimization Strategies</h3>
                <p>Improve retrieval accuracy with hybrid search, implement smart chunking strategies,
                and use reranking models for better results.</p>
                '''
            },
            {
                'title': 'AI Ethics in Production: What You Need to Know',
                'intro': 'Deploying AI responsibly requires understanding ethical implications and best practices.',
                'tags': ['ethics', 'ai', 'compliance', 'responsibility'],
                'content': '''
                <p>As AI becomes more prevalent in business operations, ethical considerations
                become paramount. This guide covers essential ethical frameworks and practices.</p>

                <h3>Key Ethical Principles</h3>
                <p>Transparency, fairness, accountability, and privacy form the foundation
                of ethical AI deployment. Each principle requires specific implementation strategies.</p>

                <h3>Bias Detection and Mitigation</h3>
                <p>Regular audits, diverse training data, and continuous monitoring are essential
                for identifying and addressing algorithmic bias.</p>

                <h3>Regulatory Compliance</h3>
                <p>Stay ahead of evolving regulations like EU AI Act, CCPA, and industry-specific
                guidelines. Build compliance into your AI development lifecycle.</p>
                '''
            },
            {
                'title': 'Fine-Tuning LLMs for Domain-Specific Applications',
                'intro': 'Transform general-purpose models into specialized tools for your industry.',
                'tags': ['fine-tuning', 'llm', 'machine-learning', 'training'],
                'content': '''
                <p>Fine-tuning allows you to adapt pre-trained language models to your specific
                domain, improving accuracy and relevance for specialized tasks.</p>

                <h3>When to Fine-Tune</h3>
                <p>Consider fine-tuning when you need consistent domain-specific outputs,
                have sufficient training data, and require better performance than prompting alone.</p>

                <h3>Data Preparation</h3>
                <p>Quality matters more than quantity. Curate high-quality examples that
                represent your use case well. Plan for at least 500-1000 examples.</p>

                <h3>Training Strategies</h3>
                <p>Use parameter-efficient fine-tuning methods like LoRA for cost-effective
                training. Monitor for overfitting and validate with held-out test sets.</p>
                '''
            },
            {
                'title': 'Vector Embeddings: The Foundation of Modern AI Search',
                'intro': 'Understanding vector embeddings is crucial for building intelligent search systems.',
                'tags': ['embeddings', 'search', 'ai', 'vectors'],
                'content': '''
                <p>Vector embeddings transform text, images, and other data into numerical
                representations that capture semantic meaning, enabling powerful AI applications.</p>

                <h3>How Embeddings Work</h3>
                <p>Modern embedding models use transformer architectures to encode meaning
                into high-dimensional vectors, where similar concepts are geometrically close.</p>

                <h3>Choosing Embedding Models</h3>
                <p>Compare OpenAI's ada-002, Cohere's embed models, and open-source alternatives
                like Sentence Transformers based on your performance and cost requirements.</p>

                <h3>Practical Applications</h3>
                <p>Build semantic search engines, recommendation systems, and similarity
                matching tools using vector embeddings as the core technology.</p>
                '''
            },
            {
                'title': 'Prompt Engineering: Advanced Techniques and Patterns',
                'intro': 'Master the art of prompt engineering to unlock the full potential of language models.',
                'tags': ['prompting', 'ai', 'llm', 'techniques'],
                'content': '''
                <p>Effective prompt engineering can dramatically improve AI model outputs
                without any fine-tuning. Learn advanced techniques and reusable patterns.</p>

                <h3>Chain-of-Thought Prompting</h3>
                <p>Guide models through step-by-step reasoning for complex problems.
                This technique significantly improves accuracy on analytical tasks.</p>

                <h3>Few-Shot Learning Patterns</h3>
                <p>Provide examples in your prompts to demonstrate desired output format
                and style. This in-context learning approach is highly effective.</p>

                <h3>System Prompt Design</h3>
                <p>Craft robust system prompts that define consistent behavior, output
                formatting, and constraints for production applications.</p>
                '''
            }
        ]

        # Create blog posts if they don't exist
        existing_posts = BlogPage.objects.count()
        if existing_posts < len(blog_posts):
            for i, post_data in enumerate(blog_posts[existing_posts:], start=existing_posts):
                blog_post = BlogPage(
                    title=post_data['title'],
                    slug=f'blog-post-{i+1}',
                    date=date.today() - timedelta(days=i*7),
                    author='Bennie Williams',
                    intro=post_data['intro'],
                    body=[
                        ('paragraph', post_data['content']),
                    ],
                )

                blog_index.add_child(instance=blog_post)
                blog_post.save_revision().publish()

                # Add tags
                for tag in post_data['tags']:
                    blog_post.tags.add(tag)
                blog_post.save()

                self.stdout.write(self.style.SUCCESS(f'Created blog post: {blog_post.title}'))

        # Set featured blog post on home page
        if BlogPage.objects.exists() and not home_page.featured_blog_post:
            home_page.featured_blog_post = BlogPage.objects.first()
            home_page.save_revision().publish()

        # Create Courses
        courses_data = [
            {
                'title': 'AI Implementation Masterclass',
                'subtitle': 'From Strategy to Deployment',
                'description': '''<p>A comprehensive 12-week program covering everything you need to know
                about implementing AI in your organization. From strategy development to technical implementation,
                this course provides hands-on experience with real-world projects.</p>

                <p>You'll learn:</p>
                <ul>
                <li>AI strategy development and ROI calculation</li>
                <li>Choosing the right AI technologies for your needs</li>
                <li>Building and training custom models</li>
                <li>Deployment and monitoring best practices</li>
                <li>Team building and change management</li>
                </ul>''',
                'price': 1997.00,
                'youtube_preview_id': 'dQw4w9WgXcQ',
                'featured': True,
                'order': 1
            },
            {
                'title': 'Prompt Engineering for Business',
                'subtitle': 'Maximize AI Productivity',
                'description': '''<p>Master the art and science of prompt engineering to get the most out of
                AI language models. This practical course focuses on business applications and real-world scenarios.</p>

                <p>Course highlights:</p>
                <ul>
                <li>Understanding model capabilities and limitations</li>
                <li>Advanced prompting techniques and patterns</li>
                <li>Building prompt libraries and templates</li>
                <li>Measuring and optimizing prompt performance</li>
                <li>Integration with business workflows</li>
                </ul>''',
                'price': 497.00,
                'youtube_preview_id': 'dQw4w9WgXcQ',
                'featured': True,
                'order': 2
            }
        ]

        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults={
                    'subtitle': course_data['subtitle'],
                    'description': course_data['description'],
                    'price': course_data['price'],
                    'gumroad_link': 'https://gumroad.com/l/placeholder',
                    'youtube_preview_id': course_data['youtube_preview_id'],
                    'featured': course_data['featured'],
                    'order': course_data['order']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created course: {course.title}'))

        # Create Courses Page
        if not CoursesPage.objects.exists():
            courses_page = CoursesPage(
                title='Courses',
                slug='courses',
                intro='<p>Level up your AI skills with comprehensive, practical courses designed for '
                      'business professionals and technical practitioners.</p>',
            )
            home_page.add_child(instance=courses_page)
            courses_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS('Created courses page'))

        # Create Services Page
        if not ServicesPage.objects.exists():
            services_page = ServicesPage(
                title='Services',
                slug='services',
                intro='<p>Transform your business with tailored AI consulting and implementation services.</p>',
                body=[
                    ('heading', 'AI Strategy Consulting'),
                    ('paragraph', '''<p>Develop a comprehensive AI strategy aligned with your business goals.
                    I'll help you identify opportunities, assess readiness, and create a roadmap for success.</p>'''),

                    ('heading', 'Custom AI Development'),
                    ('paragraph', '''<p>Build custom AI solutions tailored to your specific needs. From proof of concept
                    to production deployment, I provide end-to-end development services.</p>'''),

                    ('heading', 'Team Training & Workshops'),
                    ('paragraph', '''<p>Empower your team with the knowledge and skills needed to work effectively
                    with AI technologies. Customized workshops and training programs available.</p>'''),

                    ('heading', 'AI Audit & Optimization'),
                    ('paragraph', '''<p>Evaluate your existing AI initiatives and identify opportunities for improvement.
                    Optimize performance, reduce costs, and enhance ROI.</p>'''),
                ],
                consultation_price='$500/hour'
            )
            home_page.add_child(instance=services_page)
            services_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS('Created services page'))

        # Create About Page
        if not AboutPage.objects.exists():
            about_page = AboutPage(
                title='About',
                slug='about',
                intro='<p><strong>Hi, I\'m Bennie Williams</strong> - AI consultant, educator, and technology enthusiast.</p>',
                body=[
                    ('paragraph', '''<p>With over a decade of experience in technology and artificial intelligence,
                    I help businesses navigate the complex world of AI implementation. My mission is to make
                    AI accessible and practical for organizations of all sizes.</p>'''),

                    ('heading', 'My Background'),
                    ('paragraph', '''<p>I've worked with Fortune 500 companies and startups alike, helping them
                    leverage AI for competitive advantage. My expertise spans machine learning, natural language
                    processing, computer vision, and strategic AI implementation.</p>'''),

                    ('heading', 'My Approach'),
                    ('paragraph', '''<p>I believe in practical, results-driven AI implementation. Rather than chasing
                    the latest trends, I focus on proven technologies that deliver real business value. My approach
                    combines technical expertise with business acumen to ensure successful outcomes.</p>'''),

                    ('heading', 'Why Work With Me'),
                    ('paragraph', '''<p>I bridge the gap between technical complexity and business strategy. Whether
                    you're just starting your AI journey or looking to optimize existing implementations, I provide
                    the guidance and expertise you need to succeed.</p>'''),
                ],
            )
            home_page.add_child(instance=about_page)
            about_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS('Created about page'))

        # Create Contact Page
        if not ContactPage.objects.exists():
            contact_page = ContactPage(
                title='Contact',
                slug='contact',
                intro='<p>Ready to discuss how AI can transform your business? Let\'s connect.</p>',
                email='bennie@benniewilliams.com',
                thank_you_text='<p>Thank you for reaching out! I\'ll get back to you within 24 hours.</p>'
            )
            home_page.add_child(instance=contact_page)
            contact_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS('Created contact page'))

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
        self.stdout.write('Admin login: username=admin, password=changeme')
        self.stdout.write('Access the site at: http://localhost:8000')
        self.stdout.write('Access the admin at: http://localhost:8000/admin')