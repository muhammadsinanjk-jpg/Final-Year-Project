from django.urls import path,re_path
from compalint_and_replay import views

urlpatterns=[
    re_path('add/',views.post),
    re_path('postreply/(?P<idd>\w+)', views.repost),
    path('viewreply/', views.reviw),
    path('viecompl/', views.viecom),
]