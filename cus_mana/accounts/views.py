from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user, allowed_users
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter


# Create your views here.
@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'pending': pending,
        'delivered': delivered
    }

    return render(request, 'accounts/dashboard.html', context=context)


@login_required(login_url='accounts:login')
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', context={'products': products})


@login_required(login_url='accounts:login')
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    total_orders = customer.order_set.all().count()
    orders = customer.order_set.all()
    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs

    context = {
        'customer': customer,
        'total_orders': total_orders,
        'orders': orders,
        'my_filter': my_filter,
    }
    return render(request, 'accounts/customer.html', context=context)


@login_required(login_url='accounts:login')
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == "POST":
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('accounts:user')

    context = {
        'form': formset,
    }
    return render(request, 'accounts/order_form.html', context=context)


@login_required(login_url='accounts:login')
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('accounts:home')

    context = {
        'form': form
    }
    return render(request, 'accounts/order_form.html', context=context)


@login_required(login_url='accounts:login')
def delete_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect('accounts:home')

    context = {
        'order': order,

    }
    return render(request, 'accounts/delete.html', context=context)


@unauthenticated_user
def register_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
            )
            messages.success(request, 'Account was created for ' + user)
            return redirect('accounts:login')
    context = {'form': form}

    return render(request, 'accounts/register_page.html', context=context)


# @unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:user')
        else:
            messages.info(request, 'Username or password is wrong')

    context = {}

    return render(request, 'accounts/login.html', context=context)


def logout_page(request):
    logout(request)
    return redirect('accounts:login')


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['customer', 'admin'])
def user_page(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    print('orders', orders)
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }
    return render(request, 'accounts/user.html', context=context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['customer', 'admin'])
def account_settings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {
        'form': form

    }
    return render(request, 'accounts/account_settings.html', context=context)