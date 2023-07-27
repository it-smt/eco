from django.contrib import messages
from django.http import Http404, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail

from .models import Message
from .forms import AddMessageForm

import config


def page_not_found(request: HttpRequest, exception):
    """Функция-обработчик страницы 404.

    Args:
        request (HttpRequest): Принимает запрос.
        exception (Exception): Принимает исключения.
    """
    print(exception.__class__.__name__)
    return render(request, '404.html')


def index(request):
    """Функция-представление главной страницы."""
    return render(request, 'main/index.html')


@login_required
def messages_list(request):
    if request.user.status != 'Работник':
        raise Http404
    messages = Message.objects.filter(is_complited=False,
                                      worker=None)  # Заявки, которые не выполнены и не находятся в обработке исполнителем.
    paginator = Paginator(messages, 6)
    page_number = request.GET.get('page', 1)
    try:
        messages = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то выдать первую страницу.
        messages = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапазона, то выдать последнюю страницу.
        messages = paginator.page(paginator.num_pages)
    context = {'messages': messages}
    return render(request, 'main/message/index.html', context)


@login_required
def detail_message(request, pk):
    user = request.user
    if not user.is_worker():
        raise Http404
    message = get_object_or_404(Message, pk=pk, worker=None,
                                is_complited=False)  # Заявка, которая не выполнена и не находится в обработке исполнителем.
    if request.method == 'POST':
        if not user.is_email_confirmed:
            messages.error(request, 'Для того чтобы добавить заявку, нужно подтвердить вашу почту!')
            return redirect('user:profile')
        message.worker = user
        message.save()
        send_mail('Заявка в обработке',
                  f'Здравствуйте, {message.author.get_full_name()}!\n\nВашу заявку выполнит наш сотрудник - {message.worker.get_full_name()} с {message.time_s} до {message.time_b} по МСК+2.',
                  config.EMAIL_HOST_USER, [message.author.email])
        return redirect('main:my_messages')
    context = {'message': message}
    return render(request, 'main/message/detail.html', context)


@login_required
def my_messages(request):
    """Функция-представление страницы с заявками, которые имеют какое-то отношение к пользователю."""
    user = request.user
    if user.is_worker():
        messages = Message.objects.filter(is_complited=False,
                                          worker=user)  # Заявки, которые не выполнены и те, что находятся в обработке у конкретного пользователя.
    elif user.is_customer():
        messages = Message.objects.filter(is_complited=False,
                                          author=user)  # Заявки, которые не выполнены и принадлежат конкретному пользователю.
    # Постраничная разбивка с 6 заявками на страницу.
    paginator = Paginator(messages, 6)
    page_number = request.GET.get('page', 1)
    try:
        messages = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то выдать первую страницу.
        messages = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапазона, то выдать последнюю страницу.
        messages = paginator.page(paginator.num_pages)
    context = {'messages': messages}
    return render(request, 'main/message/my/index.html', context)


@login_required
def my_message_detail(request: HttpRequest, pk):
    """Функция-представление страницы с детальной информацией заявки, которая имеет какое-то отношение к пользователю.

    Args:
        request (HttpRequest): Принимает запрос.
        pk (int): Принимает первичный ключ по которому извлекается заявка.

    Returns:
        _type_: _description_
    """
    user = request.user
    if user.is_worker():
        message = Message.objects.get(pk=pk,
                                      worker=user)  # Заявки, которые не выполнены и которые находятся в обработке у конкретного пользователя.
    elif user.is_customer():
        message = Message.objects.get(pk=pk,
                                      author=user)  # Заявки, которые не выполнены и принадлежат конкретному пользователю.
    context = {'message': message}
    return render(request, 'main/message/my/detail.html', context)


@login_required
def add_message(request):
    """Функция-представление добавления заявки."""
    user = request.user
    if not user.is_email_confirmed:
        messages.error(request, 'Для того чтобы добавить заявку, нужно подтвердить вашу почту!')
        return redirect('user:profile')
    if request.method == 'POST':
        form = AddMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = user
            message.save()
            return redirect('main:my_messages')
    else:
        form = AddMessageForm()
    context = {
        'form': form
    }
    return render(request, 'main/message/add_message.html', context)


@login_required
def complited_messages(request):
    if not request.user.is_staff:
        raise Http404
    return render(request, 'main/message/complited/index.html')


@login_required
def complited_messages_detail(request):
    if not request.user.is_staff:
        raise Http404
    return render(request, 'main/message/complited/detail.html')
