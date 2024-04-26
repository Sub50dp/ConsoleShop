from cart.models import Cart


def return_cart_for_user(request):
    user = request.user
    if user.is_authenticated:
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user)
    else:
        try:
            cart = Cart.objects.get(session_key=request.session.session_key)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(session_key=request.session.session_key)
    return cart