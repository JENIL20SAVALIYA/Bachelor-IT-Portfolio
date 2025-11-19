# accounts/urls.py
from django.template.context_processors import static
from django.urls import path

from qr_generator_project import settings
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # User registration page
    path('register/', views.register, name='register'),

    # User login page
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),

    # User logout page
    path('logout/', views.user_logout, name='logout'),

    # User profile page
    path('profile/', views.profile, name='profile'),

    # Upload CSV to generate QR codes (requires user to be logged in)
    path('upload_csv/', views.upload_csv, name='upload_csv'),

    # View generated QR codes (requires user to be logged in)
    path('view_qr_codes/', views.view_qr_codes, name='view_qr_codes'),

    path('display_qr_data/<int:qr_code_id>/', views.display_qr_data, name='display_qr_data'),

    path('download_qr_code/<int:qr_code_id>/', views.download_qr_code, name='download_qr_code'),

    # Download all QR codes as a ZIP file (requires user to be logged in)
    path('download_all_qr_codes/', views.download_all_qr_codes, name='download_all_qr_codes'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    # Password reset views (optional, if you want to include password management)
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)