from datetime import datetime

from django.shortcuts import render, redirect
from django.forms import inlineformset_factory

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from pip._vendor import requests

from clients.models import Order
from .forms import *


def login_method(request):
    """Authenticates user information. Only users with staff status can access
    to the staff portal"""
    # If the user is already authenticated, then it will be redirected to staff_home
    if request.user.is_authenticated:
        return redirect('staff_home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            # If the user exists...
            if user is not None:
                login(request, user)
                return redirect('staff_home')
            else:
                messages.info(request, 'User OR Password is incorrect')

        context = {}
        return render(request, 'menus/login.html', context)


def logout_method(request):
    """Log out method"""
    logout(request)
    return redirect('login')


@login_required(login_url='login')  # Just logged users can access to this views
def staff_home(request):
    """When POST request is made, this method verifies if the sent data
    is valid and then saves the new record in the DB"""

    menu_form = MenuForm()

    # dates of the current records are needed to display in the view
    menus = Menu.objects.all()
    dates = []
    for menu in menus:
        dates.append(menu.date)  # Collect all dates with menu records

    # inlineformset_factory allows to insert more than one record at the time to the DB
    OptionFormSet = inlineformset_factory(Menu, Option, fields=('content',), extra=4, can_delete=False)
    option_formset = OptionFormSet(queryset=Option.objects.none(), instance=Menu())

    if request.method == 'POST':
        menu_form = MenuForm(request.POST)
        option_formset = OptionFormSet(request.POST, instance=Menu())

        if option_formset.is_valid() and menu_form.is_valid():
            menu = menu_form.save(commit=False)
            menu.save()

            for option_form in option_formset:
                content = option_form.cleaned_data.get('content')
                if content:
                    option = Option(content=content)  # Creates an Option instance
                    option.menu = menu  # Sets menu of the Option instance
                    option.save()

            return redirect('/staff/slack')

    context = {'menu_form': menu_form, 'option_formset': option_formset, 'dates': dates}

    return render(request, 'menus/staff_home.html', context)


@login_required(login_url='login')
def staff_menus(request):
    """Returns all the records of the menus_menu table"""
    data = {}

    menus = Menu.objects.all()
    for menu in menus:
        data[menu] = menu.join()

    context = {'data': data}

    return render(request, 'menus/staff_menus.html', context)


@login_required(login_url='login')
def edit_menu(request, pk):
    """When POST request is made, this method update the records of menu and options in the DB"""
    menu = Menu.objects.get(id=pk)  # Gets menu by id
    menu_form = MenuForm(instance=menu)  # Creates a form instance with menu info

    options = Option.objects.filter(menu=menu)  # Filters options corresponding to a certain menu

    option_forms = []  # Creates an option form for each option and collect them
    for option in options:
        option_form = OptionForm(instance=option)
        option_forms.append(option_form)

    option_form_is_valid = True

    if request.method == 'POST':
        menu_form = MenuForm(request.POST, instance=menu)

        if menu_form.is_valid():
            menu_form.save()

            option_forms = []
            for option in options:
                option_form = OptionForm(request.POST, instance=option)
                option_forms.append(option_form)

                if not option_form.is_valid():  # If an option form is not valid the loop ends
                    option_form_is_valid = False
                    break

            if option_form_is_valid:
                for option_form in option_forms:
                    option_form.save()

                return redirect('staff_menus')

    context = {'menu_form': menu_form, 'option_forms': option_forms}
    return render(request, 'menus/edit_menus.html', context)


@login_required(login_url='login')
def delete_menu(request, pk):
    """When POST request is made, this method deletes the record in the DB"""
    menus = Menu.objects.all()
    menu = Menu.objects.get(id=pk)

    context = {'menu': menu, 'menus': menus}

    if request.method == 'POST':
        menu.delete()
        menus = Menu.objects.all()
        context = {'menus': menus}
        return redirect('/staff/menus/')

    return render(request, 'menus/staff_menus.html', context)


@login_required(login_url='login')
def show_orders(request):
    """Displays all the orders made a certain day"""
    date_str = request.POST['date']
    date = datetime.strptime(date_str, '%b. %d, %Y')
    orders = Order.objects.filter(date__date=date.date())

    context = {'orders': orders, 'date': date_str}
    return render(request, 'menus/orders.html', context)


@login_required(login_url='login')
def slack_notification(request):
    """Sends a slack notification with today's menu"""
    today_menu = Menu.objects.get(date=datetime.today())
    today_options = Option.objects.filter(menu=today_menu)

    url = 'https://nora.cornershop.io/menu/{}'.format(today_menu.unique_id)
    options = ""
    n = 1
    for option in today_options:
        options = options + "Option {}: {}\n".format(n, option.content)
        n = n + 1

    message = "Hello!\nI share with you today's menu :)\n\n {}\n\n{}".format(options, url)

    # Slack info
    slack_token = 'token'
    slack_channel = '#channel'
    slack_text = message

    if request.method == 'POST':
        requests.post('https://slack.com/api/chat.postMessage', {
            'token': slack_token,
            'channel': slack_channel,
            'text': slack_text
        })
        return redirect('staff_home')

    context = {'message': message}
    return render(request, 'menus/slack.html', context)
