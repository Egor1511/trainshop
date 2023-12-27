from decimal import Decimal
from typing import Optional, Tuple

from django.shortcuts import get_object_or_404
from django.urls import reverse
from orders.models import Order


def get_order_info(request) -> Optional[Order]:
    """Получает ифнормацию о зазе из сессии запроса."""
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, pk=order_id)
    return order


def session_data_forming(request, order: Optional[Order]):
    """Формирует данные сессии для платежа."""
    success_url = request.build_absolute_uri(
        reverse('payment:completed'))
    cancel_url = request.build_absolute_uri(
        reverse('payment:canceled')
    )
    session_data = {
        'mode': 'payment',
        'client_reference_id': order.id,
        'success_url': success_url,
        'cancel_url': cancel_url,
        'line_items': [],
    }
    for item in order.items.all():
        session_data['line_items'].append({
            'price_data': {
                'unit_amount': int(item.price * Decimal('100')),
                'currency': 'usd',
                'product_data': {
                    'name': item.product.name,
                },
            },
            'quantity': item.quantity,
        })
    return session_data


