from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('decrease_quantity/<int:pk>/', views.decrease_quantity, name='decrease_quantity'),
    path('increase/<int:pk>/', views.increase_quantity, name='increase_quantity'),
    path('cart/', views.cart_view, name='cart'),
    # path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('payment/', views.payment_view, name='payment'),
    path('process-payment/', views.process_payment, name='process_payment'),
]