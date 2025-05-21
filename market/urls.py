from django.urls import path
from . import views

urlpatterns = [
    path('', views.market_index, name='market_index'),
# Category page (displays items within a specific category)
    path('category/<slug:category_slug>/', views.market_category, name='market_category'),

# Item detail page (displays a single item)
    path('item/<slug:item_slug>/', views.market_detail, name='market_detail'),

# Add to cart (handles adding an item to the user's cart)
    path('cart/add/<slug:item_slug>/', views.cart_add, name='cart_add'),

# Cart view (displays the user's cart)
    path('cart/', views.cart_view, name='cart_view'),

# Checkout (handles the checkout process)
    path('checkout/', views.checkout, name='checkout'),

# Payment processing (handles Stripe payment)
    path('payment/', views.payment, name='payment'),

# Order confirmation (displays after successful purchase)
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),

# Leave a review (handles submitting a review for an item)
    path('item/<slug:item_slug>/review/', views.market_review, name='market_review'),
]
