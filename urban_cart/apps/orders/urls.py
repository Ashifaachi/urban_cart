from django.urls import path
from . import views

urlpatterns = [
    path('',views.order,name='orders'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),

]
