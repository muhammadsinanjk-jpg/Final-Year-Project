from django.urls import path, re_path
from catagory import views

urlpatterns = [
    path('catagory/', views.addc, name='add_catagory'),
    path('vc/', views.v_catagory, name='v_catagory'),

    # update
    re_path(r'^up/(?P<idd>\d+)/$', views.update, name='update_catagory'),

    # delete  ✅ NEW
    re_path(r'^delete/(?P<idd>\d+)/$', views.delete_catagory, name='delete_catagory'),
]
