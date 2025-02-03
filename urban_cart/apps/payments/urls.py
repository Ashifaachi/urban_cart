from django.urls import path
from .views import payment_cancel,payment_success,checkout,add_address,payment_failed

urlpatterns = [
    path("checkout/", checkout, name="checkout"),
    path("success/", payment_success, name="payment_success"),
    path("payment_cancel/", payment_failed, name="payment_failed"),
    path("add_address/", add_address, name="add_address"),
    

]
