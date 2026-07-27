from django.urls import path
from temp import views

urlpatterns = [
    path('admin/', views.admin),
    path('buyer/', views.buyer),
    path('home/', views.home),
    path('seller/', views.seller),

    # Show products by catagory
    path('catagory/<str:cat_name>/', views.products_by_category, name='products_by_category'),

    # Show single product
    path('product/<int:pro_id>/', views.product_detail, name='product_detail'),
]
