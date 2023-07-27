from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),  # Основная страница.
    path('messages/', views.messages_list, name='messages'),  # Страница со всеми заявками.
    path('messages/<int:pk>/', views.detail_message, name='message_detail'),  # Страница с детальной инфой о заявке.
    path('my_messages/add/', views.add_message, name='add_message'),
    path('my_messages/', views.my_messages, name='my_messages'),  # Заявки, которые относятся к определенному пользователю.
    path('my_messages/<int:pk>/', views.my_message_detail, name='my_message_detail'),  # Детальный просмотр заявки, которая относится к определенному пользователю.
]