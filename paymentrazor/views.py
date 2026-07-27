from django.shortcuts import render, redirect
from cart.models import Order
from payment.models import Payment
import datetime
from django.db import connection
from django.http import JsonResponse

from django.shortcuts import render, redirect
from cart.models import Order
from payment.models import Payment
import datetime

def get_next_payment_id():
    # Only if you keep IntegerField as primary key
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT MAX(pay_id) FROM payment")
        row = cursor.fetchone()
        return (row[0] or 0) + 1

def payment_form(request, order_id):
    uid = request.session["u_id"]
    ob = Order.objects.get(order_id=order_id)
    amt=str(request.session['gtot'])
    amount = float(amt) * 100
    context = {'razorpay_key': 'rzp_test_Ey8ivDWGODPlAZ', 'amt': str(amount)}

    # Create Payment object
    obj = Payment()
    obj.pay_id = get_next_payment_id()  # only if your pay_id is IntegerField
    obj.order = ob                       # assign the Order object, not integer
    obj.reg_id = uid                      # or obj.reg = RegisterForBuyer.objects.get(pk=uid)
    obj.payment = amt
    obj.date = datetime.datetime.today()
    obj.status = 'pending'
    obj.save()

    request.session['payid'] = str(obj.pay_id)
    return render(request, 'paymentrazor.html', context)
from django.http import JsonResponse
from payment.models import Payment
from cart.models import Order

def update_payment(request):
    pay_id = request.session.get('payid')
    if not pay_id:
        return JsonResponse({'error': 'Payment ID not found'}, status=400)

    # Get Payment object
    payment_obj = Payment.objects.get(pay_id=pay_id)
    payment_obj.status = 'paid'
    payment_obj.save()

    # Update Order status
    order_obj = payment_obj.order  # use the ForeignKey
    order_obj.status = 'paid'
    order_obj.save()

    return JsonResponse({'message': 'Payment completed successfully'})


from django.shortcuts import render, redirect
from cart.models import Order
from payment.models import Payment
import datetime


def get_next_payment_id():
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT MAX(pay_id) FROM payment")
        row = cursor.fetchone()
        return (row[0] or 0) + 1


def payment_page(request, order_id):
    # Get order
    order = Order.objects.get(order_id=order_id)

    # Convert order amount to paise (for Razorpay)
    amount = float(order.amount) * 100  # Razorpay needs amount in paise

    # Create Payment object (pending)
    payment_obj = Payment()
    payment_obj.pay_id = get_next_payment_id()
    payment_obj.order = order
    payment_obj.reg_id = request.session.get("u_id")
    payment_obj.payment = str(order.amount)
    payment_obj.date = datetime.datetime.today()
    payment_obj.status = "pending"
    payment_obj.save()

    # Save payment ID in session
    request.session['payid'] = str(payment_obj.pay_id)

    context = {
        "razorpay_key": "rzp_test_Ey8ivDWGODPlAZ",
        "amt": str(amount),
        "order": order,
    }
    return render(request, "pay.html", context)


def update_pay(request):
    pay_id = request.session.get('payid')
    if not pay_id:
        return JsonResponse({'error': 'Payment ID not found'}, status=400)

    payment_obj = Payment.objects.get(pay_id=pay_id)
    payment_obj.status = 'paid'
    payment_obj.save()

    order_obj = payment_obj.order
    order_obj.status = 'paid'
    order_obj.save()

    return JsonResponse({'message': 'Payment completed successfully'})
