from django.shortcuts import render
from payment.models import Payment
from cart.models import Order
# Create your views here.
def v_order(request):
    obj=Payment.objects.all()
    c={
        'vp':obj
    }
    return render(request,'payment/view_order.html',c)

def v_feedback(request):
    ss=request.session['u_id']
    obj=Order.objects.filter(reg_id=ss)
    c={
        'vf':obj
    }
    return render(request,'payment/v_feedback.html',c)

