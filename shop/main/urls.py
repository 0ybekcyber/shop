from django.urls import path, include
from .views import home, detail, user_login, user_logout, user_register, add_to_cart, cart_view, remove_from_cart, clear_cart
from django.contrib.auth import views as auth_views

app_name = 'main'

urlpatterns = [

    path('', home, name='home'),
    path('detail/<int:id>/', detail, name='detail'),
    path('category/<int:id>/', home, name='category_filtered'),
    path('login/', user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/',user_register, name='register'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', clear_cart, name='clear_cart'),

]

