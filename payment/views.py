from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from orders.models import Order
from eshop import settings
from .utils import generate_payment_id, generate_hash, get_hash_string

def process_payment(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    trans_params = {
        'key'             : settings.PAYU_MERCHANT_KEY,
        'txnid'           : generate_payment_id(),
        'amount'          : float(order.get_total_cost()),
        'firstname'       : order.first_name,
        'lastname'        : order.last_name,
        'email'           : order.email,
        'phone'           : order.phone,
        'productinfo'     : ','.join(item.product.name for item in order.items.all()),
        'surl'            : request.build_absolute_uri(
                                reverse('payment:successful')),
        'furl'            : request.build_absolute_uri(
                                reverse('payment:failed')),
        'service_provider': 'payu_paisa',
        'action'          : settings.PAYU_BASE_URL
    }
    trans_params['hash'] = generate_hash(trans_params)
    return render(request, 'payment/make_payment.html', {'params': trans_params})

@csrf_exempt
def payment_successful(request):
    return render(request, 'payment/successful.html')

@csrf_exempt
def payment_failed(request):
    return render(request, 'payment/failed.html')
