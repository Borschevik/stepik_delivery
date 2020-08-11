"""
Utils for processing data
"""


def price_sum(bin_cart: dict) -> list:
    """
    Get count and price

    :param bin_cart:  dict with orders
    :return: list with count and price
    """
    count: int = 0
    prices: int = 0
    for entry in bin_cart.values():
        count += entry["count"]
        prices += entry["count"] * entry["price"]

    return [count, prices]
