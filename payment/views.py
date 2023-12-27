import stripe
from django.conf import settings
from django.shortcuts import render, redirect

from .services import session_data_forming, get_order_info

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    order = get_order_info(request)
    if request.method == 'POST':
        session_data = session_data_forming(request, order)
        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)
    elif request.method == 'GET':
        return render(request, 'payment/process.html', locals())


def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
