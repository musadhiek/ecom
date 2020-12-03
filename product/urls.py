from django.urls import path
from product import views

urlpatterns=[
    path('add_product',views.add_product,name='add_product'),
    path('add_catagory',views.add_catagory,name='add_catagory'),
    path('show_catagory',views.show_catagory,name='show_catagory'),
    path('edit_catagory/<int:id>',views.edit_catagory,name='edit_catagory'),
    path('delete_catagory/<int:id>',views.delete_catagory,name='delete_catagory'),
    path('delete_catagory_all/<int:id>',views.delete_catagory_all,name='delete_catagory_all'),


    
    
    path('show_products',views.show_products,name='show_products'),
    path('delete_product/<int:id>',views.delete_product,name='delete_product'),
    path('edit_product/<int:id>',views.edit_product,name='edit_product'),
    
    path('view_product_details/<int:id>',views.view_product_details,name='view_product_details'),
    path('catagory_items/<int:id>',views.catagory_items,name='catagory_items'),
]