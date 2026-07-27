from .models import Catagory

def categories_processor(request):
    return {
        'categories': Catagory.objects.all()
    }
