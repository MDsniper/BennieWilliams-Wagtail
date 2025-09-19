from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.snippets.models import register_snippet
from .models import Course


class CourseViewSet(SnippetViewSet):
    model = Course
    menu_label = "Courses"
    icon = "graduation-cap"
    menu_order = 300
    add_to_settings_menu = False
    list_display = ("title", "featured", "price", "order")
    list_filter = ("featured",)
    search_fields = ("title", "description")


register_snippet(CourseViewSet)