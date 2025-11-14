import paypalrestsdk
from django.conf import settings

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})


def create_payment(order):
    """
    Creates a PayPal payment object.
    """
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/success",  # frontend success page
            "cancel_url": "http://localhost:3000/payment/cancel",   # frontend cancel page
        },
        "transactions": [{
            "item_list": {
                "items": [
                    {
                        "name": item.product.name,
                        "sku": str(item.product.id),
                        "price": f"{item.price:.2f}",
                        "currency": "USD",
                        "quantity": item.quantity
                    } for item in order.items.all()
                ]
            },
            "amount": {
                "total": f"{order.total_price:.2f}",
                "currency": "USD"
            },
            "description": f"Order #{order.id} payment"
        }]
    })
    if payment.create():
        return payment
    else:
        raise Exception(payment.error)
