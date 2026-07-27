from django.urls import path
from payment import views

urlpatterns=[
    path('v_pay/',views.v_order),
    path('v_feed/',views.v_feedback)

]