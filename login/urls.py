from django.urls import path
from login import views

urlpatterns=[
    path('log/',views.login),
    path('forgot_pass/',views.forgotpassword),
    path('logout/', views.logout, name='logout'),
]