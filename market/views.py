from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Item, Category, Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReviewForm  # You'll need to create this form
from django.conf import settings #For Stripe
import stripe #For Stripe

def market_index(request):
    """
    Displays all available items in the marketplace.
    """
    items = Item.objects.all()
    categories = Category.objects.all()
    context = {
        'items': items,
        'categories': categories,
    }
    return render(request, 'market/market_index.html', context)


def market_category(request, category_slug):
    """
    Displays items within a specific category.
    """
    category = get_object_or_404(Category, slug=category_slug)
    items = Item.objects.filter(category=category)
    categories = Category.objects.all() #For the sidebar
    context = {
        'category': category,
        'items': items,
        'categories': categories,
    }
    return render(request, 'market/market_index.html', context)  # Or you can create a separate template


def market_detail(request, item_slug):
    """
    Displays a single item in detail.  Handles reviews as well.
    """
    item = get_object_or_404(Item, slug=item_slug)
    reviews = Review.objects.filter(item=item).order_by('-created_at')
    form = ReviewForm() # Instantiate the form

    context = {
        'item': item,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'market/market_detail.html', context)

@login_required
def cart_add(request, item_slug):
    """
    Adds an item to the user's cart.  Uses session to store cart.
    """
    item = get_object_or_404(Item, slug=item_slug)
    cart = request.session.get('cart', {})  # Get cart from session, or default to {}
    if item_slug in cart:
        cart[item_slug] += 1
    else:
        cart[item_slug] = 1
    request.session['cart'] = cart
    messages.success(request, f'{item.name} added to your cart!')
    return redirect('market_index')  # Redirect to the main market page


def cart_view(request):
    """
    Displays the user's cart.
    """
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for item_slug, quantity in cart.items():
        item = get_object_or_404(Item, slug=item_slug)
        subtotal = item.price * quantity
        total += subtotal
        cart_items.append({
            'item': item,
            'quantity': quantity,
            'subtotal': subtotal,
        })
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'market/cart_view.html', context)

@login_required
def checkout(request):
    """
    Handles the checkout process.  This is where you'd integrate with a payment gateway.
    """
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect('market_index')

    cart_items = []
    total = 0
    for item_slug, quantity in cart.items():
        item = get_object_or_404(Item, slug=item_slug)
        subtotal = item.price * quantity
        total += subtotal
        cart_items.append({
            'item': item,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    context = {
        'cart_items': cart_items,
        'total': total,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY # Pass the key to the template
    }
    return render(request, 'market/checkout.html', context)  # You'll create this template

@login_required
def payment(request):
    """
    Handles the Stripe payment processing.
    """
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect('market_index')

    total = 0
    for item_slug, quantity in cart.items():
        item = get_object_or_404(Item, slug=item_slug)
        total += item.price * quantity

    stripe.api_key = settings.STRIPE_SECRET_KEY  # Set your secret key

    try:
        charge = stripe.Charge.create(
            amount=int(total * 100),  # Amount in cents
            currency='usd',
            description='Second Chance Movement Marketplace Purchase',
            source=request.POST['stripeToken'],  # Token from Stripe Checkout
            receipt_email=request.user.email
        )

        # Clear the cart from the session upon successful payment
        del request.session['cart']
        # Optionally create an Order object in your database here

        messages.success(request, 'Payment successful! Your order is being processed.')
        return redirect('order_confirmation', order_id=123) #Replace 123 with actual order id

    except stripe.error.CardError as e:
        messages.error(request, f'Error: {e.message}')
        return redirect('checkout')
    except Exception as e:
        messages.error(request, f'An error occurred: {e}')
        return redirect('checkout')

def order_confirmation(request, order_id):
    """
    Display order confirmation
    """
    context = {
        'order_id': order_id,
    }
    return render(request, 'market/order_confirmation.html', context)

@login_required
def market_review(request, item_slug):
    """
    Handles submission of reviews for items.
    """
    item = get_object_or_404(Item, slug=item_slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.user = request.user  # Set the user
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('market_detail', item_slug=item.slug)  # Redirect to the item detail page
        else:
            messages.error(request, 'There was an error submitting your review.')
            # You could re-render the form with errors, but redirecting is simpler for this example
            return redirect('market_detail', item_slug=item.slug)
    else:
        #Should not get here
        return redirect('market_detail', item_slug=item.slug)


