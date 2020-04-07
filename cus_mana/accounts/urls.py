from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),

    path('register/', views.register_page, name='register_page'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),

    path('user/', views.user_page, name='user'),
    path('account_settings/', views.account_settings, name='account_settings'),
    path('customer/<str:pk>', views.customer, name='customer'),

    path('create_order/<str:pk>', views.create_order, name='create_order'),
    path('update_order/<str:pk>', views.update_order, name='update_order'),
    path('delete_order/<str:pk>', views.delete_order, name='delete_order'),

    # path('reset_password/',
    #      auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html', email_template_name='accounts/email_reset.html'),
    #      name='reset_password'),
    # path('reset_password_sent/',
    #      auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'),
    #      name='password_reset_done'),
    # path('reset/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'),
    #      name='password_reset_confirm'),
    # path('reset_password_complete/',
    #      auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'),
    #      name='password_reset_complete'),
]