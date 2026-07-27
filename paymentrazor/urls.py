from django.urls import path
from paymentrazor import views

urlpatterns = [
    path('payment-form/<int:order_id>/', views.payment_form, name="payment"),
    path('post_pay/', views.update_payment, name="update_payment"),
    path('payment/<int:order_id>/', views.payment_page, name='payment_page'),

    # AJAX handler for updating payment after Razorpay success
    path('paymentrazor/post_pay/', views.update_pay, name='update_pay'),
]
