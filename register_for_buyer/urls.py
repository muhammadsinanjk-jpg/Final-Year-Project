from django.urls import  path,re_path
from register_for_buyer import views
urlpatterns=[
    path('reg/',views.reg),
    # path('manage_b/', views.manage),
    # re_path('accept/(?P<idd>\w+)', views.accept),
    # re_path('reject/(?P<idd>\w+)', views.reject),
    path('vu/', views.v_user),
    re_path('up/(?P<idd>\w+)', views.update),

]