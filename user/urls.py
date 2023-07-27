from django.urls import path, include
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from . import views
from .forms import PasswordSetForm, ResetPasswordForm

app_name = 'user'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/change_password/',
         views.ChangePasswordView.as_view(), name='change_password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset/index.html', subject_template_name='user/password_reset/subject.txt',
         email_template_name='user/password_reset/email.html', success_url=reverse_lazy('user:password_reset_done'), form_class=ResetPasswordForm), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='user/password_reset/done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset/confirm.html',
         success_url=reverse_lazy('user:password_reset_complete'), form_class=PasswordSetForm), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='user/password_reset/complete.html'), name='password_reset_complete'),
    path('profile/change_info/', views.change_user_info, name='change_info'),
    path('profile/change_email/', views.change_email, name='change_email'),
    path('verification/send_code_email/',
         views.send_code_email, name='send_code_email'),
    path('verification/confirm_email/',
         views.confirm_email, name='confirm_email'),
]
