from django.shortcuts import render
from .models import CompalintAndReplay
import datetime
# Create your views here.
def viecom(request):
    ob=CompalintAndReplay.objects.all()
    c={
        'a':ob
    }
    return render(request,'complait_and_replay/complaintview.html',c)

def post(request):
    ss=request.session['u_id']
    if request.method=='POST':
        ob=CompalintAndReplay()
        ob.complaint=request.POST.get('com')
        ob.replay='Pending'
        ob.reg_id=ss
        ob.date=datetime.datetime.today()
        ob.save()
    return render(request,'complait_and_replay/complintpost.html')

def repost(request,idd):
    if request.method=='POST':
        ob=CompalintAndReplay.objects.get(com_id=idd)
        ob.replay=request.POST.get('re')
        ob.save()
        return viecom(request)
    return render(request,'complait_and_replay/replay.html')

def reviw(request):
    ss=request.session['u_id']
    ob = CompalintAndReplay.objects.filter(reg_id=ss)
    c = {
        'a': ob
    }
    return render(request,'complait_and_replay/replayview.html',c)
