from home.models import AboutPage

about = AboutPage.objects.first()
if about:
    about.profile_statement = '''Currently serving as Senior Data Center Manager at Children's National Hospital while running an independent AI & Technology consulting practice. I specialize in helping businesses leverage AI, prompt engineering, and digital transformation strategies. My unique perspective combines enterprise infrastructure management with cutting-edge AI implementation, built on a foundation from Navy service through global data center management at Accenture and Oracle.'''
    about.save()
    print('Updated profile statement to include consulting work')
else:
    print('No AboutPage found')