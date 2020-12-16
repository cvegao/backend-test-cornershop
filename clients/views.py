from datetime import datetime

from django.shortcuts import render, redirect

from django.contrib import messages

from clients.forms import ClientForm, OrderForm
from clients.models import Order


def client_home(request):
    """Shows form to make orders. When POST request is made, it sends the order
    and stores it in the DB"""
    # Info for clients_home
    client_form = ClientForm()
    order_form = OrderForm()

    # Dates definition
    deadline = datetime.now().replace(hour=11, minute=0, second=0, microsecond=0)  # 11:00:00 CLT
    now = datetime.now()
    before_deadline = False
    if now <= deadline:
        before_deadline = True

    # When a POST request is made...
    if request.method == 'POST':
        if before_deadline:  # First it checks if the request was made before 11
            client_form = ClientForm(request.POST)
            order_form = OrderForm(request.POST)

            if client_form.is_valid() and order_form.is_valid():
                client = client_form.save(commit=False)
                client.save()

                option = order_form.cleaned_data.get('option')
                comments = order_form.cleaned_data.get('comments')

                if option and comments:
                    # Instance of Order is made with option and comments from the form
                    order = Order(option=option, comments=comments)
                    order.client = client # Client information is passed to order object
                    order.save()

                messages.success(request, 'Thank you for your preference.')
                return redirect('client_home')
        else:  # If the request was made after 11...
            messages.error(request, 'No orders are allowed after 11 am.')

    context = {'client_form': client_form, 'order_form': order_form}

    return render(request, 'clients/clients_home.html', context)
