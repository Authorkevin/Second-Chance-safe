import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .forms import DonationForm
from .models import Donation
import decimal

# Initialize Stripe with your secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

def donation_form_view(request):
    """
    Handles the display of the donation form and initiates the Stripe Checkout session.
    """
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            try:
                # Save donation with 'pending' status
                donation = form.save(commit=False)
                # If user is authenticated, you can link the donation to the user
                if request.user.is_authenticated:
                    donation.user = request.user
                donation.status = 'pending'
                donation.save()

                # Store necessary info in session to retrieve after Stripe redirect
                request.session['donation_id'] = donation.id
                request.session['donor_first_name'] = donation.first_name

                # Create Stripe Checkout Session
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'One-time Donation',
                                'description': f'Donation from {donation.first_name} {donation.last_name}',
                            },
                            # Amount in cents
                            'unit_amount': int(donation.amount * decimal.Decimal('100')),
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('donate:donation_success')) + '?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=request.build_absolute_uri(reverse('donate:donation_cancel')) + '?session_id={CHECKOUT_SESSION_ID}',
                    # Pass donation ID in metadata to link Stripe session with your Donation object
                    metadata={
                        'donation_id': donation.id,
                        'donor_email': donation.email if donation.email else 'N/A',
                    },
                    # Pre-fill email if available and user is not logged in, or if you want to force it
                    customer_email=donation.email if donation.email else (request.user.email if request.user.is_authenticated and hasattr(request.user, 'email') else None),
                )
                # Store the Stripe Checkout ID on the donation object temporarily
                # It will be confirmed and permanently stored on success
                donation.stripe_checkout_id = checkout_session.id
                donation.save()

                return redirect(checkout_session.url, code=303)
            except stripe.error.StripeError as e:
                messages.error(request, f"Something went wrong with Stripe: {e}")
                # Optionally, update donation status to 'failed' here
                if 'donation' in locals() and donation.id:
                    donation.status = 'failed'
                    donation.save()
                return render(request, 'donate/donate.html', {'form': form, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {e}")
                if 'donation' in locals() and donation.id:
                    donation.status = 'failed'
                    donation.save()
                return render(request, 'donate/donate.html', {'form': form, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DonationForm()

    return render(request, 'donate/donate.html', {'form': form, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})


def donation_success_view(request):
    """
    Handles successful payment confirmation from Stripe.
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY # Ensure API key is set
    session_id = request.GET.get('session_id')
    
    # Retrieve stored donation_id and donor_first_name from session
    donation_id_from_session = request.session.get('donation_id') # Alternative if metadata fails
    donor_first_name = request.session.pop('donor_first_name', 'Friend') # Default if not found
    # It's better to clear only specific session items or be very careful with session.clear()
    request.session.pop('donation_id', None)


    if not session_id:
        messages.error(request, "Stripe session ID not found.")
        return redirect('donate:donate_form')

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        donation_id = session.metadata.get('donation_id')

        if not donation_id:
            messages.error(request, "Donation ID not found in Stripe session metadata.")
            # Try to find donation by stripe_checkout_id if it was stored earlier
            donation = Donation.objects.filter(stripe_checkout_id=session_id, status='pending').first()
            if not donation:
                 return redirect('donate:donate_form')
        else:
            donation = get_object_or_404(Donation, id=int(donation_id))


        if session.payment_status == 'paid':
            # Update donation status to 'paid'
            donation.status = 'paid'
            donation.stripe_checkout_id = session.id # Confirm and store the checkout ID
            donation.save()
            
            messages.success(request, f"Thank you for your generous donation, {donation.first_name}!")
            
            # Optional: Send a confirmation email here
            # send_donation_confirmation_email(donation)

            return render(request, 'donate/donation_thank_you.html', {'donation': donation})
        else:
            # Payment not successful
            donation.status = 'failed'
            donation.save()
            messages.error(request, "Your payment was not successful. Please try again or contact support.")
            return redirect('donate:donate_form')

    except stripe.error.StripeError as e:
        messages.error(request, f"Stripe error: {e}")
        # Potentially try to find the donation via session_id if metadata retrieval failed before error
        donation = Donation.objects.filter(stripe_checkout_id=session_id, status='pending').first()
        if donation:
            donation.status = 'failed'
            donation.save()
        return redirect('donate:donate_form')
    except Donation.DoesNotExist:
        messages.error(request, "Donation record not found. Please contact support.")
        return redirect('donate:donate_form')
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {e}")
        return redirect('donate:donate_form')


def donation_cancel_view(request):
    """
    Handles payment cancellation.
    """
    session_id = request.GET.get('session_id')
    if session_id:
        try:
            # Attempt to retrieve donation via stripe_checkout_id which was set before redirect
            donation = Donation.objects.filter(stripe_checkout_id=session_id, status='pending').first()
            if donation:
                donation.status = 'cancelled'
                donation.save()
                messages.warning(request, f"Your donation process for {donation.first_name} {donation.last_name} was cancelled.")
            else:
                messages.warning(request, "Your donation process was cancelled.")
        except Exception as e:
            # Log error e
            messages.warning(request, "Your donation process was cancelled. If you started a donation, it has not been processed.")
    else:
        messages.warning(request, "Your donation process was cancelled.")
    
    return render(request, 'donate/donation_cancel.html')


