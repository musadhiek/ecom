from django.urls import path
from product import views

urlpatterns=[
    path('add_product',views.add_product,name='add_product'),
    path('vendor_add_catagory',views.vendor_add_catagory,name='vendor_add_catagory'),
    path('show_products',views.show_products,name='show_products'),
    path('delete_product/<int:id>',views.delete_product,name='delete_product'),
    path('edit_product/<int:id>',views.edit_product,name='edit_product'),
    
    path('view_product_details/<int:id>',views.view_product_details,name='view_product_details'),
]