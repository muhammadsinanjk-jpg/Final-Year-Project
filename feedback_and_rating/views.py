from django.shortcuts import render
from feedback_and_rating.models import FeedbackAndRating
from django.http import HttpResponseRedirect
from register_for_buyer.models import RegisterForBuyer
from payment.models import Payment
# Create your views here.
def feedb(request, idd):
    ss = request.session['u_id']
    if request.method == 'POST':
        obj = FeedbackAndRating()
        obj.feed_back = request.POST.get('feed')
        obj.rating = request.POST.get('rating')
        obj.reg_id = ss
        obj.order_id = idd  # This now works
        obj.save()
        return HttpResponseRedirect('/payment/v_feed/')
    return render(request, 'feedback_and_rating/feedback.html')


def feed_view(request):
    ob=FeedbackAndRating.objects.all()
    c={
        'a':ob
    }
    return render(request, 'feedback_and_rating/feedbackview.html',c)