from django.urls import path,re_path
from feedback_and_rating import views

urlpatterns=[
    re_path('far/(?P<idd>\w+)',views.feedb),
    path('far_vi/',views.feed_view)
]