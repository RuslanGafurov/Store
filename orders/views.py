from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView

from common.views import TitleMixin
from orders.forms import OrderForm

stripe.api_key = settings.STRIPE_SECRET_KEY
__all__ = (
    'SuccessOrderView',
    'CancelOrderView',
    'OrderCreateView',
    'stripe_webhook_view',
)


class SuccessOrderView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'


class CancelOrderView(TemplateView):
    template_name = 'orders/cancel.html'


class OrderCreateView(TitleMixin, CreateView):
    """Отображение страницы оформления заказа"""
    template_name = 'orders/create.html'
    form_class = OrderForm
    title = 'Store - Оформление заказа'
    success_url = reverse_lazy('orders:create')

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1OE9i8Du1bbI2E0mBCJb8a9e',
                    'quantity': 1,
                },
            ],
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url=f"{settings.DOMAIN_NAME}{reverse('orders:success')}",
            cancel_url=f"{settings.DOMAIN_NAME}{reverse('orders:cancel')}",
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET_KEY
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        line_items = session.line_items
        order_id = int(session.metadata.order_id)
        # Fulfill the purchase...
        fulfill_order(line_items, order_id)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(line_items, order_id):
    print(order_id)
    print("Fulfilling order")
