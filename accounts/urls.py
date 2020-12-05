from django.urls import path
from accounts import views


urlpatterns = [
    path('',views.home, name='home'),
    path('user_login',views.user_login,name='user_login'),
    path('admin_login',views.admin_login,name='admin_login'),
    path('login_with_otp',views.login_with_otp,name='login_with_otp'),
    path('send_otp',views.send_otp,name='send_otp'),
    path('enter_otp',views.enter_otp,name='enter_otp'),
    
    
    path('logout_request',views.logout_request,name='logout'),
    
    path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('admin_sale_report',views.admin_sale_report,name='admin_sale_report'),
    path('admin_cancelled_report',views.admin_cancelled_report,name='admin_cancelled_report'),
    path('admin_monthly_report',views.admin_monthly_report,name='admin_monthly_report'),
    path('adminusers',views.admin_user_page,name='adminusers'),
    
    path('user_page', views.userpage,name='user_page'),
    path('user_profile',views.user_profile, name='user_profile'),
    path('edit_user_profile',views.edit_user_profile,name='edit_user_profile'),
    
    path('user_signup',views.user_signup,name='user_signup'),
    path('add_user', views.add_user,name='add_user'),
    
    path('delete_user/<int:id>',views.delete_user,name='delete_user'),
    path('edit_user/<int:id>',views.edit_user,name='edit_user'),
    path('block_user/<int:id>',views.block_user,name='block_user'),
    path('unblock_user/<int:id>',views.unblock_user,name='unblock_user'),

]