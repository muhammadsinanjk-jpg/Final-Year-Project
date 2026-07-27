from django.urls import path,re_path
from add_product import views

urlpatterns=[
    path('product/',views.add),
    path('shop/', views.view_public, name='public_shop'),
    path('v_product/',views.view),
    path('up_view/',views.view_up),
    re_path('update/(?P<idd>\w+)',views.update, name='update_product'),
    re_path('del/(?P<idd>\w+)', views.delete, name='delete_product'),
    path('ajax_add_to_cart/', views.ajax_add_to_cart, name='ajax_add_to_cart'),
]