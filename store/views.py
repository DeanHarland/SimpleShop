from django.shortcuts import render,get_object_or_404,redirect
from .models import Product
# Create your views here.

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


# def remove_from_cart(request,pk):
#         product = get_object_or_404(Product, pk=pk)
#         cart = request.session.get('cart', {})

#         if str(pk) in cart:
#              cart[str(pk)]['quantity'] -= 1
#         elif str(pk) in cart and cart[str(pk)]['quantity'] <= 0:
            
#         else:
#              pass
        
#         request.session['cart'] = cart

#         return redirect('cart')


def cart_view(request):
    cart = request.session.get('cart', {})
    products = []

    for key, value in cart.items():
        product = Product.objects.get(pk=key)
        product.quantity = value['quantity']
        products.append(product)

    return render(request, 'store/cart.html', {'products': products})