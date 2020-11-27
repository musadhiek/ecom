from django.urls import path
from purchase import views

urlpatterns = [
    path('show_cart',views.show_cart,name='show_cart'),
    path('add_shipping_address',views.add_shipping_address,name='add_shipping_address'),
    path('save_address',views.save_address,name='save_address'),
    path('delete_address/<int:id>',views.delete_address,name='delete_address'),
    path('make_primary/<int:id>',views.make_primary,name='make_primary'),
    path('change_address',views.change_address,name='change_address'),
    
    

    path('add_to_cart/<int:id>', views.add_to_cart,name='add_to_cart'),
    path('add_one_quantity/<int:id>', views.add_one_quantity,name='add_one_quantity'),
    path('remove_one_quantity/<int:id>', views.remove_one_quantity,name='remove_one_quantity'),
    path('delete_cart_item/<int:id>', views.delete_cart_item,name='delete_cart_item'),
    path('confirm_purchase',views.confirm_purchase,name='confirm_purchase'),
    path('process_order', views.process_order,name='process_order'),

    path('order_history',views.order_history,name="order_history"),
    path('admin_order_history',views.admin_order_history,name="admin_order_history"),
    path('admin_order_delete/<int:id>',views.admin_order_delete,name='admin_order_delete'),
    path('vendor_order',views.vendor_order,name="vendor_order")
]