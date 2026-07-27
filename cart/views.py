from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import json

from .models import Cart, Order
from add_product.models import AddProduct
from register_for_buyer.models import RegisterForBuyer
from payment.models import Payment

# -------------------------
# View Cart
# -------------------------
def view_cart(request):
    ss = request.session.get('u_id')
    if not ss:
        return redirect('/login/log/')
        
    carts = Cart.objects.filter(reg_id=ss)
    cart_total = sum(item.pro.product_price for item in carts)

    return render(request, 'cart/cartpost.html', {
        'ca': carts,
        'cart_total': cart_total
    })

# -------------------------
# Place Order
# -------------------------
def order(request):
    # 1 Check if user is logged in
    uid = request.session.get('u_id')
    if not uid:
        messages.error(request, "Please login first")
        return redirect('/login/log/')

    # 2 Get the buyer object
    buyer = get_object_or_404(RegisterForBuyer, reg_id=uid)

    # 3 Get cart data from GET or POST
    cart_data = request.GET.get('cart_data') or request.POST.get('cart_data')
    if not cart_data:
        messages.error(request, "No cart items found")
        return redirect('/cart/v_cart/')

    try:
        cart_items_data = json.loads(cart_data)
    except json.JSONDecodeError:
        messages.error(request, "Invalid cart data")
        return redirect('/cart/v_cart/')

    cart_items = []
    grand_total = 0

    # 4 Prepare cart items and calculate total
    for item in cart_items_data:
        cart_item = get_object_or_404(Cart, cart_id=item['cart_id'], reg_id=uid)
        quantity = int(item.get('quantity', 1))
        amount = cart_item.pro.product_price * quantity
        cart_items.append({
            'pro': cart_item.pro,
            'quantity': quantity,
            'amount': amount,
        })
        grand_total += amount

    request.session['gtot'] = grand_total

    # 5 If POST, process the order
    if request.method == "POST":
        delivery_address = request.POST.get('delivery_address')
        if not delivery_address:
            messages.error(request, "Please enter a delivery address")
            return render(request, 'cart/view_order.html', {'p': cart_items, 'grand_total': grand_total})

        # Save orders
        first_order_id = None
        for p in cart_items:
            order_obj = Order.objects.create(
                pro=p['pro'],
                reg=buyer,
                quantity=p['quantity'],
                amount=p['amount'],
                delivery_address=delivery_address
            )
            if first_order_id is None:
                first_order_id = order_obj.order_id

            # Update product stock
            p['pro'].stock_quantity -= p['quantity']
            p['pro'].save()

        # Clear cart
        for item in cart_items_data:
            ci = get_object_or_404(Cart, cart_id=item['cart_id'], reg_id=uid)
            ci.delete()

        # Redirect to payment page
        return redirect('payment_page', order_id=first_order_id)

    return render(request, 'cart/view_order.html', {'p': cart_items, 'grand_total': grand_total})

def delete(request, idd):
    obj = get_object_or_404(Cart, cart_id=idd)
    obj.delete()
    return redirect('view_cart')

def buy_now(request, pro_id):
    uid = request.session.get('u_id')
    if not uid:
        messages.error(request, "Please login first")
        return redirect('/login/log/')
    
    product = get_object_or_404(AddProduct, pro_id=pro_id)
    buyer = get_object_or_404(RegisterForBuyer, reg_id=uid)
    
    # Create a draft order
    order_obj = Order.objects.create(
        pro=product,
        reg=buyer,
        quantity=1,
        amount=product.product_price,
        delivery_address="" # Will be filled in view_order
    )
    
    return redirect('view_order', idd=order_obj.order_id)

def view_order(request, idd):
    obj = Order.objects.filter(order_id=idd)

    grand_total = sum(item.amount for item in obj)

    if request.method == "POST":
        address = request.POST.get("delivery_address")
        order_obj = get_object_or_404(Order, order_id=idd)
        order_obj.delivery_address = address
        order_obj.save()

        # Redirect to the new payment page
        return redirect('payment_page', order_id=idd)

    return render(request, 'cart/view_order.html', {'p': obj, 'grand_total': grand_total})

def update_quantity(request, idd, action):
    # Get the specific order item
    order_item = get_object_or_404(Order, order_id=idd)
    
    if action == 'plus':
        order_item.quantity += 1
    elif action == 'minus':
        if order_item.quantity > 1:
            order_item.quantity -= 1
    
    # Update the amount for this line item based on the new quantity
    # Assuming amount stored is Total Amount for that line item (Price * Qty)
    # We need the unit price. Since we don't store unit price in Order model explicitly,
    # we can retrieve it from the related Product (pro).
    unit_price = order_item.pro.product_price
    order_item.amount = unit_price * order_item.quantity
    
    order_item.save()
    
    # Redirect back to the view_order page. 
    # We need the order_id. Wait, view_order takes 'idd' which is order_id.
    # But view_order displays a *list* of orders if filtered by order_id? 
    # In views.py: obj = Order.objects.filter(order_id=idd)
    # Usually order_id is unique per line item in this simple schema, or it acts as a Cart/Group ID.
    # Looking at 'order' view: order_obj = Order.objects.create(...) -> each item gets a new unique order_id.
    # So 'view_order' showing filter(order_id=idd) actually shows just ONE item usually.
    # But later in 'order' view: return redirect('payment_page', order_id=first_order_id)
    # And 'view_order' iterates {% for item in p %}.
    # If the user bought multiple items in cart, they created multiple Order objects. 
    # But the 'view_order' view takes a SINGLE 'idd' and filters by it. 
    # This implies 'view_order' might only show ONE item, unless multiple items share the same order_id?
    # Checking 'order' view again:
    # order_obj = Order.objects.create(...) -> new PK for each.
    # so 'view_order(request, idd)' where idd is order_id will only show that ONE item.
    # So if the user ordered 3 items, they got 3 distinct Order objects with 3 distinct IDs.
    # The current 'view_order' implementation seems to only show one item at a time?
    # "obj = Order.objects.filter(order_id=idd)" -> PK filter.
    # Yes. So we just redirect back to view_order with the same idd.
    
    return redirect('view_order', idd=idd)
