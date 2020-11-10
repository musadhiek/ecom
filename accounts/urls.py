from django.urls import path
from accounts import views


urlpatterns = [
    path('',views.home, name='home'),
    path('user_login',views.user_login,name='user_login'),
    path('vendor_login',views.vendor_login,name='vendor_login'),
    path('admin_login',views.admin_login,name='admin_login'),
    
    path('logout_request',views.logout_request,name='logout'),
    
    path('admin_page',views.adminpage,name='admin_page'),
    path('adminusers',views.adminusers,name='adminusers'),
    
    path('user_page', views.userpage,name='user_page'),
    path('vendor_page',views.vendorpage,name='vendor_page'),
    
    path('vendor_signup',views.vendor_signup,name='vendor_signup'),
    path('add_vendor',views.add_vendor,name='add_vendor'),
    
    path('user_signup',views.user_signup,name='user_signup'),
    path('add_user', views.add_user,name='add_user'),
    
    path('delete_user/<int:id>',views.delete_user,name='delete_user'),
    path('edit_user/<int:id>',views.edit_user,name='edit_user'),
]