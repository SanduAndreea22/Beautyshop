from django.urls import path
from . import views

urlpatterns = [
    # ===== Produse =====
    path('', views.store, name='store'),
    path('product/<slug:slug>/', views.product_detail, name='product-detail'),

    # ===== Coș =====
    path('cart/', views.cart_summary, name='cart-summary'),
    path('add/<int:id>/', views.cart_add, name='cart-add'),
    path('delete/<int:id>/', views.cart_delete, name='cart-delete'),
    path('update/<int:id>/', views.cart_update, name='cart-update'),

    # ===== Checkout & Comandă =====
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order-success'),

    # ===== Autentificare =====
    path('register/', views.register, name='register'),
    path('my-login/', views.my_login, name='my-login'),
    path('user-logout/', views.user_logout, name='user-logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # ===== Recenzii =====
    path('add-review/<int:product_id>/', views.add_review, name='add-review'),

    # ===== Wishlist =====
    path('add-wishlist/<int:product_id>/', views.add_to_wishlist, name='add-wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
]

