from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .forms import OrderForm
from .filters import OrderFilter
from .models import *


# Create your views here.
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


def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', context={'products': products})


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


def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == "POST":
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('accounts:home')

    context = {
        'form': formset
    }
    return render(request, 'accounts/order_form.html', context=context)


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


def delete_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect('accounts:home')


    context = {
        'order': order,

    }
    return render(request, 'accounts/delete.html', context=context)