from django.shortcuts import render
from apps.payments.models import Order,OrderItem
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def order(request):
    """Display a list of all orders for the logged-in user."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  # Fetch orders for logged-in user
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """Display details of a specific order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)  # Ensure user can only view their own orders

    order_items = []
    for item in order.items.all():
        item.subtotal = item.quantity * item.price
        order_items.append(item)
    return render(request, 'orders/order_detail.html', {'order': order,'order_items': order_items,})