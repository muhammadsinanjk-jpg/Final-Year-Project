from django.urls import path
from register_for_seller import views

urlpatterns = [
    path('add/', views.reg, name='register_seller'),
    path('manage_s/', views.manage, name='manage_seller'),
    path('accept/<int:idd>/', views.accept, name='accept_seller'),
    path('reject/<int:idd>/', views.reject, name='reject_seller'),
    path('v_seller/', views.view_seller, name='view_seller'),
    path('up/<int:idd>/', views.update, name='update_seller'),
]