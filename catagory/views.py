from django.shortcuts import render
from catagory.models import Catagory
from django.core.files.storage import FileSystemStorage
# Create your views here.
def addc(request):
    if request.method=='POST':
        ob=Catagory()
        ob.catagory=request.POST.get('catagory')
        my_file = request.FILES.get('image')
        fs = FileSystemStorage()
        fs.save(my_file.name, my_file)
        ob.image = my_file.name
        ob.save()
    return render(request, 'catagory/catagorypost.html')

def v_catagory(request):
    obj=Catagory.objects.all()
    c={
        'g':obj
    }
    return render(request,'catagory/v_category.html',c)

def update(request,idd):
    obj = Catagory.objects.get(cat_id=idd)
    c = {
        'h': obj
    }
    if request.method == 'POST':
        ob = Catagory.objects.get(cat_id=idd)
        ob.catagory = request.POST.get('catagory')
        my_file = request.FILES.get('image')
        fs = FileSystemStorage()
        fs.save(my_file.name, my_file)
        ob.image = my_file.name
        ob.save()
        return v_catagory(request)
    return render(request, 'catagory/edit.html', c)



from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST

@require_POST
def delete_catagory(request, idd):
    obj = get_object_or_404(Catagory, cat_id=idd)
    obj.delete()
    return redirect('v_catagory')
