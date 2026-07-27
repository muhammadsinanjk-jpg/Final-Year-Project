from django.shortcuts import render
from .models import RegisterForBuyer
from login.models import Login
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
# Create your views here.
# def manage(request):
#     obj = RegisterForBuyer.objects.all()
#     c = {
#         'a': obj
#     }
#
#     return render(request, 'register_for_buyer/Manage buyer.html', c)
#
#
# def accept(request, idd):
#     ob = RegisterForBuyer.objects.get(reg_id=idd)
#     ob.status = 'accepted'
#     ob.save()
#     return manage(request)
#
#
# def reject(request, idd):
#     ob = RegisterForBuyer.objects.get(reg_id=idd)
#     ob.status = 'rejected'
#     ob.save()
#     return manage(request)

def reg(request):
    if request.method=='POST':
        ob=RegisterForBuyer()
        ob.name=request.POST.get('Name')
        ob.email=request.POST.get('Email')
        ob.password=request.POST.get('Password')
        ob.phone=request.POST.get('Phone')
        ob.status='pending'
        my_file=request.FILES['photo']
        fs=FileSystemStorage()
        fs.save(my_file.name,my_file)
        ob.photo=my_file.name
        ob.save()

        o = Login()
        o.username = ob.name
        o.password = ob.password
        o.type = 'buyer'
        o.u_id = ob.reg_id
        o.save()
        return HttpResponseRedirect('/login/log/')
    return render(request,'register_for_buyer/Register.html')

def v_user(request):
    if 'u_id' in request.session:
        ss = request.session['u_id']
        obj = RegisterForBuyer.objects.filter(pk=ss)
        c = {
            'a': obj
        }
        return render(request, 'register_for_buyer/view_buyer.html', c)
    else:
        return HttpResponseRedirect('/login/log/')

def update(request,idd):
    obj = RegisterForBuyer.objects.get(reg_id=idd)
    c = {
        'a': obj
    }
    if request.method=='POST':
        ob=RegisterForBuyer.objects.get(reg_id=idd)
        ob.name=request.POST.get('Name')
        ob.email=request.POST.get('Email')
        ob.password=request.POST.get('Password')
        ob.phone=request.POST.get('Phone')
        ob.status='pending'
        # ob.photo=request.POST.get('photo')
        if 'photo' in request.FILES:
            my_file = request.FILES['photo']
            fs = FileSystemStorage()
            fs.save(my_file.name, my_file)
            ob.photo = my_file.name
        ob.save()
        return v_user(request)
    return render(request, 'register_for_buyer/update.html', c)
