from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Review, Order, OrderItem, Wishlist
from .forms import RegisterForm, LoginForm

# ================== Store / Products ==================
def store(request):
    products = Product.objects.all()
    return render(request, 'store/store.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all()
    return render(request, 'store/product_detail.html', {'product': product, 'reviews': reviews})

# ================== Cart ==================
def cart_add(request, id):
    product = get_object_or_404(Product, id=id)
    qty = int(request.POST.get('qty', 1))
    cart = request.session.get('cart', {})

    if str(product.id) in cart:
        cart[str(product.id)]['quantity'] += qty
    else:
        cart[str(product.id)] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': qty,
            'image_url': product.image.url
        }

    request.session['cart'] = cart
    return redirect('cart-summary')

def cart_delete(request, id):
    cart = request.session.get('cart', {})
    cart.pop(str(id), None)
    request.session['cart'] = cart
    return redirect('cart-summary')

def cart_update(request, id):
    cart = request.session.get('cart', {})
    qty = int(request.POST.get('qty', 1))
    if str(id) in cart:
        cart[str(id)]['quantity'] = qty
    request.session['cart'] = cart
    return redirect('cart-summary')

def cart_summary(request):
    cart = request.session.get('cart', {})
    items = []

    total = 0
    for product_id, item in cart.items():
        subtotal = item['price'] * item['quantity']
        total += subtotal
        items.append({
            'id': product_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'total_price': subtotal
        })

    context = {
        'cart': items,
        'total': total
    }
    return render(request, 'store/cart.html', context)


# ================== Checkout ==================
@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty!")
        return redirect('store')

    if request.method == 'POST':
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip')
        payment_method = request.POST.get('payment_method')

        paid = False
        # Dacă metoda e card, verifici că au completat datele cardului
        if payment_method == 'card':
            card_number = request.POST.get('card_number')
            card_exp = request.POST.get('card_exp')
            card_cvc = request.POST.get('card_cvc')
            if not all([card_number, card_exp, card_cvc]):
                messages.error(request, "Please fill card details.")
                return redirect('checkout')
            paid = True  # Aici poți integra Stripe real pentru procesare

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            city=city,
            postal_code=zip_code,
            country='Romania',
            payment_method=payment_method,
            paid=paid
        )

        for id, item in cart.items():
            product = Product.objects.get(id=id)
            OrderItem.objects.create(
                order=order,
                product=product,
                price=item['price'],
                quantity=item['quantity']
            )

        request.session['cart'] = {}
        return redirect('order-success')

    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'store/checkout.html', {'cart': cart, 'total': total})


@login_required
def order_success(request):
    return render(request, 'store/order_success.html')

# ================== Authentication ==================
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})

def my_login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'store/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('store')

# ================== Dashboard ==================
@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user)
    wishlist_obj, _ = Wishlist.objects.get_or_create(user=request.user)
    wishlist_products = wishlist_obj.products.all()
    return render(request, 'store/dashboard.html', {
        'orders': orders,
        'wishlist': wishlist_products
    })

# ================== Reviews ==================
@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        rating = int(request.POST['rating'])
        comment = request.POST['comment']
        Review.objects.create(user=request.user, product=product, rating=rating, comment=comment)
        return redirect('product-detail', slug=product.slug)
    return render(request, 'store/add_review.html', {'product': product})

# ================== Wishlist ==================
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_obj, _ = Wishlist.objects.get_or_create(user=request.user)
    wishlist_obj.products.add(product)
    return redirect('dashboard')

@login_required
def wishlist_view(request):
    wishlist_obj, _ = Wishlist.objects.get_or_create(user=request.user)
    wishlist_products = wishlist_obj.products.all()
    return render(request, 'store/wishlist.html', {'wishlist': wishlist_products})


