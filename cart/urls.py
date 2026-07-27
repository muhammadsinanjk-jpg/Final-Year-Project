from django.urls import path,re_path
from cart import views as cart_views

urlpatterns = [
    path('v_cart/', cart_views.view_cart, name='view_cart'),
    path('order/', cart_views.order, name='order'),  # no idd, orders all items
    path('delete/<int:idd>/', cart_views.delete, name='delete_cart'),
    path('view_o/<int:idd>/', cart_views.view_order, name='view_order'),
    path('buy_now/<int:pro_id>/', cart_views.buy_now, name='buy_now'),
    path('update_quantity/<int:idd>/<str:action>/', cart_views.update_quantity, name='update_quantity'),
    # re_path('view_o/(?P<idd>\w+)', cart_views.view_order),
]
