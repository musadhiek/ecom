from django.urls import path
from purchase import views

urlpatterns = [
    path('show_cart',views.show_cart,name='show_cart'),

    path('add_to_cart/<int:id>', views.add_to_cart,name='add_to_cart'),
    path('add_one_quantity/<int:id>', views.add_one_quantity,name='add_one_quantity'),
    path('remove_one_quantity/<int:id>', views.remove_one_quantity,name='remove_one_quantity'),
    path('delete_cart_item/<int:id>', views.delete_cart_item,name='delete_cart_item'),
    path('confirm_purchase',views.confirm_purchase,name='confirm_purchase'),

    path('order_history',views.order_history,name="order_history"),
    path('admin_order_history',views.admin_order_history,name="admin_order_history"),
    path('vendor_order',views.vendor_order,name="vendor_order")
]