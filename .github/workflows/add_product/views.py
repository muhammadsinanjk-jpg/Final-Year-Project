from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import json

from add_product.models import AddProduct
from catagory.models import Catagory
from cart.models import Cart

# Create your views here.
def add(request):
    o = Catagory.objects.all()
    c = {
        'ca': o
    }
    if request.method == 'POST':
        ob = AddProduct()
        ob.product_name = request.POST.get('product')
        ob.description = request.POST.get('disc')
        ob.cat_id = request.POST.get('ok')
        
        if 'Image' in request.FILES:
            my_file = request.FILES['Image']
            fs = FileSystemStorage()
            fs.save(my_file.name, my_file)
            ob.image_of_product = my_file.name
            
        ob.product_price = request.POST.get('price')
        ob.stock_quantity = request.POST.get('qty')
        ob.save()

    return render(request, 'add_product/Product.html', c)

def view_up(request):
    obj = AddProduct.objects.all()
    c = {
        'a': obj
    }
    return render(request, 'add_product/manage_products.html', c)

def view(request):
    # Get all categories for filter dropdown
    categories = Catagory.objects.all()

    # Get GET parameters
    selected_category = request.GET.get('category', '')
    selected_sort = request.GET.get('sort', '')

    # Start with all products
    products = AddProduct.objects.all()

    # Filter by category if selected
    if selected_category:
        products = products.filter(cat__catagory=selected_category)

    # Sort by price
    if selected_sort == 'low':
        products = products.order_by('product_price')
    elif selected_sort == 'high':
        products = products.order_by('-product_price')

    context = {
        'a': products,
        'categories': categories,
        'selected_category': selected_category,
        'selected_sort': selected_sort,
    }
    return render(request, 'add_product/viewproduct.html', context)

def view_public(request):
    # Get all categories for filter dropdown
    categories = Catagory.objects.all()

    # Get GET parameters
    selected_category = request.GET.get('category', '')
    selected_sort = request.GET.get('sort', '')

    # Start with all products
    products = AddProduct.objects.all()

    # Filter by category if selected
    if selected_category:
        products = products.filter(cat__catagory=selected_category)

    # Sort by price
    if selected_sort == 'low':
        products = products.order_by('product_price')
    elif selected_sort == 'high':
        products = products.order_by('-product_price')

    context = {
        'a': products,
        'categories': categories,
        'selected_category': selected_category,
        'selected_sort': selected_sort,
    }
    return render(request, 'add_product/viewproduct_public.html', context)

def update(request, idd):
    ob = AddProduct.objects.get(pro_id=idd)
    o = Catagory.objects.all()
    c = {
        'ca': o,
        'up': ob
    }
    if request.method == 'POST':
        ob.product_name = request.POST.get('product')
        ob.description = request.POST.get('disc')
        ob.cat_id = request.POST.get('ok')
        
        if 'Image' in request.FILES:
            my_file = request.FILES['Image']
            fs = FileSystemStorage()
            fs.save(my_file.name, my_file)
            ob.image_of_product = my_file.name
            
        ob.product_price = request.POST.get('price')
        ob.stock_quantity = request.POST.get('qty')
        ob.save()
        return redirect('/add_product/up_view/')

    return render(request, 'add_product/edit.html', c)

def delete(request, idd):
    obj = AddProduct.objects.get(pro_id=idd)
    obj.delete()
    return view_up(request)

def ajax_add_to_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            uid = request.session.get('u_id')

            if not uid:
                return JsonResponse({'error': 'You must be logged in to add to cart.'}, status=403)

            product = AddProduct.objects.get(pro_id=product_id)

            # Check if already in cart
            if Cart.objects.filter(pro=product, reg_id=uid).exists():
                return JsonResponse({'error': 'This product is already in your cart!'})

            # Add to cart
            obj = Cart(pro=product, reg_id=uid)
            obj.save()

            return JsonResponse({'success': True})

        except AddProduct.DoesNotExist:
            return JsonResponse({'error': 'Product does not exist.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)
