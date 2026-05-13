from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Count
from .models import Product, Order, OrderItem
from django.contrib.auth.decorators import login_required


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})

    if str(pk) in cart:
        cart[str(pk)]['quantity'] += 1
    else:
        cart[str(pk)] = {'quantity': 1}
        

    request.session['cart'] = cart

    return redirect('product_list')


def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})

    if str(pk) in cart:
        del cart[str(pk)]

    request.session['cart'] = cart

    return redirect('cart')


def decrease_quantity(request,pk):
        cart = request.session.get('cart', {})
        
        if str(pk) in cart:
             cart[str(pk)]['quantity'] -= 1
             if str(pk) in cart and cart[str(pk)]['quantity'] <= 0:
                del cart[str(pk)]
         
        request.session['cart'] = cart
        return redirect('cart')

def increase_quantity(request, pk):
    cart = request.session.get('cart', {})

    if str(pk) in cart:
        cart[str(pk)]['quantity'] += 1

    request.session['cart'] = cart
    return redirect('cart')

def cart_view(request):
    cart = request.session.get('cart', {})
    products = []
    cart_total = 0
    cart_items_count = 0

    for key, value in cart.items():
        product = Product.objects.get(pk=key)
        product.quantity = value['quantity']
        product.line_total = product.price * product.quantity
        cart_total += product.line_total
        cart_items_count += product.quantity
        products.append(product)

    return render(request, 'store/cart.html', {
        'products': products,
        'cart_total': cart_total,
        'cart_items_count': cart_items_count,
    })

# @login_required
# def checkout(request):
#     cart = request.session.get('cart', {})

#     if not cart:
#         return redirect('product_list')

#     total = 0
#     order = Order.objects.create(user=request.user if request.user.is_authenticated else None,total=0)

#     for key, value in cart.items():
#         product = Product.objects.get(pk=key)
#         quantity = value['quantity']

#         total += product.price * quantity

#         OrderItem.objects.create(
#             order=order,
#             product=product,
#             quantity=quantity,
#             price=product.price
#         )

#     order.total = total
#     order.save()

#     request.session['cart'] = {}

#     return redirect('order_confirmation', order_id=order.id)

def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    items = OrderItem.objects.filter(order=order)

    return render(request, 'store/order_confirmation.html', {
        'order': order,
        'items': items
    })

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).annotate(item_count=Count('orderitem')).order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})

def payment_view(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('product_list')
    
    if request.method == 'POST':
        return redirect('process_payment')

    return  render(request, 'store/payment.html')

def process_payment(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('product_list')

    total = 0
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        total=0
    )

    for key, value in cart.items():
        product = Product.objects.get(pk=key)
        quantity = value['quantity']

        total += product.price * quantity

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

    order.total = total
    order.save()

    request.session['cart'] = {}

    return redirect('order_confirmation', order_id=order.id)