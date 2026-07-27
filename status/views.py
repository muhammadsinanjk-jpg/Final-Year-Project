from django.shortcuts import render
from .models import DeliveryStatus
from django.http import HttpResponseRedirect
# Create your views here.
def delivary_status(request,idd):
    ss=request.session['u_id']
    if request.method=='POST':
        obj=DeliveryStatus()
        obj.order_id=idd
        obj.sreg_id=ss
        obj.delivery_status=request.POST.get('sts')
        obj.save()
        return HttpResponseRedirect('/payment/v_pay/')
    return render(request,'status/status.html')

def v_status(request):
    # ss=request.session['u_id']
    obj=DeliveryStatus.objects.all()
    c={
        'ss':obj
    }
    return render(request,'status/statusofproduct.html',c)