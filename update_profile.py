from home.models import AboutPage

about = AboutPage.objects.first()
if about:
    about.profile_statement = '''Currently serving as Senior Data Center Manager at Children's National Hospital (direct employment since 2023), managing data center and system management teams. Previously held the same role through Oracle contract (2018-2023). My journey from Navy service through Accenture's global infrastructure management has given me a unique perspective on solving complex technology challenges.'''
    about.save()
    print('Updated profile statement')
else:
    print('No AboutPage found')