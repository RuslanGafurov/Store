from products.models import Basket


def baskets(request) -> dict[str, list]:
    """Контекстный процессор для глобального обращения к корзине товаров"""
    user = request.user
    return {'baskets': Basket.objects.filter(user=user) if user.is_authenticated else []}
