import datetime
from blog.models import Category


def shared_context(request):
    context = {
        "year": datetime.datetime.today().year,
        "categories": Category.objects.all()
    }

    return context
