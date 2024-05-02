from order.models import Order


def return_user_order(request):
    user = request.user
    if user.is_authenticated:
        order = Order.objects.filter(user=user).order_by("-create_date").first()
    else:
        order = Order.objects.filter(session_key=request.session.session_key).order_by("-create_date").first()
    if not order:
        return None
    return order
