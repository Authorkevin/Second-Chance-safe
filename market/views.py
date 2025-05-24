from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Item, Category, Review, Order, OrderItem #Import Order and OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReviewForm  # You'll need to create this form
from django.conf import settings #For Stripe
import stripe #For Stripe
from django.core.mail import EmailMultiAlternatives, send_mail #Import send_mail
from django.template.loader import render_to_string # Import render_to_string
from django.http import JsonResponse
from .forms import PaymentForm

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
    form = PaymentForm()

    context = {
        'cart_items': cart_items,
        'total': total,
        'form': form,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY # Pass the key to the template
    }
    form = PaymentForm()
    return render(request, 'market/checkout.html', context)  # You'll create this template

@login_required
def payment(request):
    """
    Handles the creation of a Stripe Checkout Session.
    """
    cart = request.session.get('cart', {})
    form = PaymentForm(request.POST)
    if form.is_valid():
        shipping_address = form.cleaned_data['shipping_address']
        request.session['shipping_address'] = shipping_address
    # Proceed to create the Stripe checkout session and redirect

    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect('market_index')

    line_items = []
    total = 0
    for item_slug, quantity in cart.items():
        item = get_object_or_404(Item, slug=item_slug)
        total += item.price * quantity
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
                'unit_amount': int(item.price * 100),  # Amount in cents
            },
            'quantity': quantity,
        })

    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=request.user.email if request.user.is_authenticated else None,
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri(reverse('payment_success')) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('checkout')),
            metadata={'user_id': request.user.id if request.user.is_authenticated else None},
            # If you want Stripe to handle shipping address collection:
#            shipping_address_collection={'allowed_countries': ['US', 'CA']}, # Add relevant countries
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        messages.error(request, f"An error occurred during checkout: {e}")
        return redirect('checkout')

def payment_success(request):
    """
    Handles the successful payment and order creation.
    """
    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session_id = request.GET.get('session_id')

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == 'paid':
            cart = request.session.get('cart', {})
            if not cart:
                messages.error(request, "Your cart is empty!")
                return redirect('market_index')

            total = 0
            order_items_data = []
            for item_slug, quantity in cart.items():
                item = get_object_or_404(Item, slug=item_slug)
                total += item.price * quantity
                order_items_data.append({
                    'item': item,
                    'quantity': quantity,
                    'subtotal': item.price * quantity
                })

        else:
            messages.error(request, 'Payment was not successful.')
            return redirect('checkout')
        shipping_address = request.session.pop('shipping_address', None)

        if not shipping_address:
            messages.error(request, "Shipping address not found.")
            return redirect('checkout')

    # Now it's safe to use form.cleaned_data
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            first_name=request.user.first_name,
            last_name=request.user.last_name,                total_price=total,
            shipping_address=shipping_address,
            stripe_checkout_id=session.id,
        )

            # Create OrderItem instances
        order_items = []
        for item_data in order_items_data:
            order_item = OrderItem.objects.create(
                order=order,
                item=item_data['item'],
                quantity=item_data['quantity'],
                subtotal=item_data['subtotal']
            )
            order_items.append(order_item)

            # Send Order Confirmation Email
        subject = f'Order Confirmation - Order #{order.order_number}'
        text_content = render_to_string(
                'market/order_comfirmation_email.html',  # Create a plain text version
        {
            'order': order,
            'user': order.user,
            'order_items': order_items,
        }
        )
        html_content = render_to_string(
            'market/order_comfirmation_email.html',
        {
            'order': order,
            'user': order.user,
            'order_items': order_items,
        }
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [order.user.email, settings.DEFAULT_FROM_EMAIL] if order.user else [settings.DEFAULT_FROM_EMAIL]

        msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        del request.session['cart']
        messages.success(request, 'Payment successful! Your order is being processed.')
        return redirect('order_confirmation', order_id=order.order_number)
    except stripe.error.InvalidRequestError as e:
        messages.error(request, f"Invalid Stripe Session: {e}")
        return redirect('checkout')
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('market_index')
    except Exception as e:
        messages.error(request, f"An error occurred after payment: {e}")
        return redirect('checkout')

# Ensure you have the URL pattern for payment_success as mentioned before
# path('payment/success/', views.payment_success, name='payment_success'),


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

