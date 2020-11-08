from django.urls import path
from product import views

urlpatterns=[
    path('add_product',views.add_product,name='add_product'),
    path('show_products',views.show_products,name='show_products'),
    path('delete_product/<int:id>',views.delete_product,name='delete_product'),
    path('edit_product/<int:id>',views.edit_product,name='edit_product'),
    path('edited_product/<int:id>',views.edited_product,name='edited_product'),

]