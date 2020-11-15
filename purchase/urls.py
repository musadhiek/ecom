from django.urls import path
from purchase import views

urlpatterns = [
    path('show_cart',views.show_cart,name='show_cart'),

    path('add_to_cart/<int:id>', views.add_to_cart,name='add_to_cart'),
    path('confirm_purchase',views.confirm_purchase,name='confirm_purchase'),

    path('order_history',views.order_history,name="order_history")
]