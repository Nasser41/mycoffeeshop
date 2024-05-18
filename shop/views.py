from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})

@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/update_product.html', {'form': form})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('home')
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    cart[pk] = cart.get(pk, 0) + 1
    request.session['cart'] = cart
    return redirect('cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for pk, quantity in cart.items():
        product = get_object_or_404(Product, pk=pk)
        total_price += product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity,
        })
    return render(request, 'shop/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})
@login_required
def update_cart(request, pk):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        cart = request.session.get('cart', {})
        if quantity > 0:
            cart[pk] = quantity
        else:
            cart.pop(pk, None)
        request.session['cart'] = cart

        # Calculate the new totals
        cart_items = []
        total_price = 0
        item_total = 0
        for pk, quantity in cart.items():
            product = get_object_or_404(Product, pk=pk)
            item_total = product.price * quantity
            total_price += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': item_total,
            })

        return JsonResponse({'success': True, 'item_total': item_total, 'cart_total': total_price})
    return JsonResponse({'success': False})

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for pk, quantity in cart.items():
        product = get_object_or_404(Product, pk=pk)
        total_price += product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity,
        })
    request.session['cart'] = {}  # Clear the cart after checkout
    return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'total_price': total_price})

