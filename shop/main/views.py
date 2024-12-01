from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Comment
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login

def home(request, id=None):
    categories = Category.objects.all()
    sort_by = request.GET.get('sort_by', 'added_at')  

    if id:
        category = get_object_or_404(Category, id=id)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    
    if sort_by == 'price':
        products = products.order_by('price')
    else:
        products = products.order_by('-added_at')

    return render(request, 'index.html', {
        'categories': categories,
        'products': products,
        'selected_category': category if id else None,
        'sort_by': sort_by
    })



def detail(request, id):
    product = get_object_or_404(Product, id=id)
    comments = product.comments.order_by('-created_at')[:2]
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if request.user.is_authenticated:
                comment.user = request.user  
            comment.product = product
            comment.save()
            return redirect('main:detail', id=product.id)  
    else:
        form = CommentForm()

    context = {
        'product': product,
        'comments': comments,
        'form': form
    }
    return render(request, 'product_detail.html', context)

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main:home')  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')  

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Roʻyxatdan oʻtish muvaffaqiyatli!')
            return redirect('main:home')  
        else:
           
            messages.error(request, 'Roʻyxatdan oʻtishda xatolik yuz berdi. Iltimos, ma\'lumotlarni tekshirib qaytadan urinib ko\'ring.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})



@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1
    
    request.session['cart'] = cart
    messages.success(request, "Mahsulot savatchaga qo'shildi.")
    return redirect('main:cart_view')



def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        total_price += product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': product.price * quantity
        })
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)



def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]  
    
    request.session['cart'] = cart  
    return redirect('main:cart_view')

def clear_cart(request):
    request.session['cart'] = {}  
    return redirect('main:cart_view')
