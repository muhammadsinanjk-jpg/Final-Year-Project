from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from .models import RegisterForSeller
from login.models import Login


def reg(request):
    """Seller Registration View (registers with status='pending')"""
    if request.method == 'POST':
        obj = RegisterForSeller()
        obj.name = request.POST.get('text')
        obj.address = request.POST.get('address')
        obj.status = 'pending'
        obj.age = request.POST.get('age')
        obj.phone = request.POST.get('phone')
        obj.password = request.POST.get('Password')
        obj.brand_name = request.POST.get('Brand')
        obj.city = request.POST.get('City')
        obj.email = request.POST.get('Email')

        if 'photo' in request.FILES:
            my_file = request.FILES['photo']
            fs = FileSystemStorage()
            filename = fs.save(my_file.name, my_file)
            obj.photo = filename
        else:
            obj.photo = ''

        obj.save()

        # Create corresponding Login entry
        ob = Login()
        ob.username = obj.name
        ob.password = obj.password
        ob.type = 'seller'
        ob.u_id = obj.sreg_id
        ob.save()

        return redirect('/login/log/')

    return render(request, 'register_for_seller/register2.html')


def manage(request):
    """Admin View to manage all registered sellers"""
    sellers = RegisterForSeller.objects.all()
    return render(request, 'register_for_seller/Manage seller.html', {'a': sellers})


def accept(request, idd):
    """Admin Action: Accept seller application"""
    seller = get_object_or_404(RegisterForSeller, sreg_id=idd)
    seller.status = 'accepted'
    seller.save()
    return redirect('/register_for_seller/manage_s/')


def reject(request, idd):
    """Admin Action: Reject seller application"""
    seller = get_object_or_404(RegisterForSeller, sreg_id=idd)
    seller.status = 'rejected'
    seller.save()
    return redirect('/register_for_seller/manage_s/')


def view_seller(request):
    """Seller Dashboard View"""
    seller_id = request.session.get('u_id')
    sellers = RegisterForSeller.objects.filter(sreg_id=seller_id)
    return render(request, 'register_for_seller/view_seller.html', {'a': sellers})


def update(request, idd):
    """Update seller profile"""
    seller = get_object_or_404(RegisterForSeller, sreg_id=idd)
    if request.method == 'POST':
        seller.name = request.POST.get('text')
        seller.address = request.POST.get('address')
        seller.age = request.POST.get('age')
        seller.phone = request.POST.get('phone')
        seller.password = request.POST.get('Password')
        seller.brand_name = request.POST.get('Brand')
        seller.city = request.POST.get('City')
        seller.email = request.POST.get('Email')

        if 'photo' in request.FILES:
            my_file = request.FILES['photo']
            fs = FileSystemStorage()
            filename = fs.save(my_file.name, my_file)
            seller.photo = filename

        seller.save()

        # Keep login credentials synced
        login_obj = Login.objects.filter(type='seller', u_id=idd).first()
        if login_obj:
            login_obj.username = seller.name
            login_obj.password = seller.password
            login_obj.save()

        return redirect('/register_for_seller/v_seller/')

    return render(request, 'register_for_seller/update.html', {'a': seller})