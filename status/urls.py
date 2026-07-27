from django.urls import path,re_path
from status import views
urlpatterns = [
    re_path('ds/(?P<idd>\w+)',views.delivary_status),
    path('vds/',views.v_status)

]